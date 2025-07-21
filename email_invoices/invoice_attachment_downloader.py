import os
import re
import requests
import html
from datetime import datetime
from email.header import decode_header
from email.utils import parsedate_to_datetime
from playwright.sync_api import sync_playwright


class InvoiceAttachmentDownloader:
    def __init__(
        self,
        download_dir=os.path.abspath(
            os.path.join(os.path.dirname(__file__), "../invoices")
        ),
    ):
        # 创建输出目录

        if not os.path.exists(download_dir):
            os.makedirs(download_dir)

        self.download_dir = download_dir

    def download_invoice_attachments(self, invoice_emails):
        invoice_pdfs = []
        for invoice_email in invoice_emails:
            # 'Mon, 9 Oct 2023 17:05:39 +0800'
            invoice_email_date_str = decode_header(invoice_email[1]["Date"])[0][0]
            if isinstance(invoice_email_date_str, bytes):
                invoice_email_date_str = invoice_email_date_str.decode("utf-8", errors="ignore")
            invoice_email_date = parsedate_to_datetime(invoice_email_date_str)
            invoice_email_month = invoice_email_date.strftime("%Y/%m")
            download_dir = os.path.abspath(os.path.join(self.download_dir, invoice_email_month))
            if not os.path.exists(download_dir):
                os.makedirs(download_dir)

            # 解析邮件附件
            pdf_attachments = self._download_attachments(
                invoice_email, download_dir, invoice_email_date
            )
            if pdf_attachments:
                # 邮件包含附件，跳过解析邮件正文
                invoice_pdfs.extend(pdf_attachments)
                continue
            pdfs = self._download_url(invoice_email, download_dir, invoice_email_date)
            if pdfs:
                invoice_pdfs.extend(pdfs)

        return invoice_pdfs

    def _download_attachments(self, invoice_email, download_dir, invoice_email_date):
        pdf_attachments = []
        if invoice_email[1].is_multipart():
            for part in invoice_email[1].walk():
                if part.get("Content-Disposition") is None:
                    continue
                if part.get_filename():
                    filename, encoding = decode_header(part.get_filename())[0]
                    if isinstance(filename, bytes):
                        filename = filename.decode(encoding or "utf-8")
                    if filename.endswith(".pdf"):
                        filename = f"{invoice_email_date.strftime('%Y%m%d')}_{invoice_email[0]}_{filename}"

                        # 构建附件的绝对路径
                        filepath = os.path.join(download_dir, filename)

                        # 保存附件到本地文件
                        with open(filepath, "wb") as f:
                            f.write(part.get_payload(decode=True))

                        pdf_attachments.append([invoice_email[0], filepath])
                        print(f"已下载另存附件: {pdf_attachments[-1]}")

        return pdf_attachments

    def _download_url(self, invoice_email, download_dir, invoice_email_date):
        pdfs = []
        for part in invoice_email[1].walk():
            if part.get_content_type() == "text/html":
                html_content = part.get_payload(decode=True).decode(
                    part.get_content_charset()
                )
                break

        pattern = r'<a(?:.*)href="([^"]+)"(?:.*)>(?:发票.*下载|.*下载.*发票|.*下载.*|\1)</a>'
        matches = re.findall(pattern, html_content)
        matches = list(set(matches))
        if matches:
            for url in matches:
                url = html.unescape(url)
                headers = {
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36"
                }
                response = requests.get(url, headers=headers)
                content_type = response.headers.get("content-type")
                if content_type.startswith("application/pdf"):
                    filename = os.path.basename(response.url).split(".pdf")[0] + ".pdf"
                    # 替换文件名中的非法字符为连字符"-"线
                    filename = re.sub(r'[\\/*?:"<>|]', '-', filename)
                    filepath = os.path.join(
                        download_dir,
                        f"{invoice_email_date.strftime('%Y%m%d')}_{invoice_email[0]}_{filename}",
                    )
                    with open(filepath, "wb") as f:
                        f.write(response.content)
                    pdfs.append([invoice_email[0], filepath])

                else:
                    with sync_playwright() as playwright:
                        try:
                            browser = playwright.chromium.launch(headless=False)
                            context = browser.new_context()

                            # Open new page
                            page = context.new_page()

                            page.goto(url)

                            # Click text=下载PDF文件
                            with page.expect_download() as download_info:
                                # page.locator(':text-matches("下载PDF文件|PDF预览版下载")').click()
                                page.locator(
                                    ':text-matches(".*下载.*[Pp][Dd][Ff].*|.*[Pp][Dd][Ff].*下载.*")'
                                ).click()
                                download = download_info.value
                                filepath = os.path.join(
                                    download_dir,
                                    f"{invoice_email_date.strftime('%Y%m%d')}_{invoice_email[0]}_{download.suggested_filename}",
                                )
                                download.save_as(filepath)

                            pdfs.append([invoice_email[0], filepath])
                            context.close()
                            browser.close()

                        except Exception as e:
                            print(f"An error occurred: {e}")

                print(f"找到发票下载链接: {url}, 已下载: {pdfs[-1]}")
        else:
            pdfs.append([invoice_email[0], ""])
            print("未找到发票下载链接, 请登录邮箱下载。")

        return pdfs


# 示例用法
if __name__ == "__main__":
    # 创建 EmailClient 实例并连接到邮件服务器
    import json
    from .email_client import EmailClient

    with open("./config.json", "r") as config_file:
        config = json.load(config_file)
    email_client = EmailClient(
        server=config["email"]["server"],
        username=config["email"]["username"],
        password=config["email"]["password"],
    )
    email_client.connect()

    # 创建 invoiceDownloader 实例
    invoice_emails = email_client.get_invoice_emails()
    downloader = InvoiceAttachmentDownloader()
    invoice_pdfs = downloader.download_invoice_attachments(invoice_emails)
    for invoice_pdf in invoice_pdfs:
        if not invoice_pdf[1]:
            email_client.set_email_unread(invoice_pdf[0])

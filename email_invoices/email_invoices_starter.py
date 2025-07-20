import json
import os
from email_client import EmailClient
from invoice_attachment_downloader import InvoiceAttachmentDownloader
from email_invoices.crypto.config_crypto import ConfigCrypto

if __name__ == "__main__":
    # 使用ConfigCrypto来读取和解密配置文件
    config_path = os.path.join(os.path.dirname(__file__), "config.json")
    config_crypto = ConfigCrypto(config_path)
    config = config_crypto.decrypt_config()
    
    if config is None:
        print("配置文件解密失败，请检查密钥文件是否存在")
        exit(1)
    
    email_client = EmailClient(
        server=config["email"]["server"],
        username=config["email"]["username"],
        password=config["email"]["password"],
    )
    email_client.connect()
    invoice_emails = email_client.get_invoice_emails()

    # 创建 InvoiceAttachmentDownloader 实例
    downloader = InvoiceAttachmentDownloader()
    invoice_pdfs = downloader.download_invoice_attachments(invoice_emails)
    for invoice_pdf in invoice_pdfs:
        if not invoice_pdf[1]:
            email_client.set_email_unread(invoice_pdf[0])
            
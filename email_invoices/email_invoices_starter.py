import os
from email_client import EmailClient
from invoice_attachment_downloader import InvoiceAttachmentDownloader
from crypto.config_crypto import ConfigCrypto

if __name__ == "__main__":
    # 支持通过环境变量指定路径
    config_path = os.environ.get("AUTO_INVOICE_CONFIG", os.path.join(os.path.dirname(os.path.dirname(__file__)), "config", "config.json"))
    private_key_path = os.environ.get("AUTO_INVOICE_PRIVATE_KEY", os.path.join(os.path.dirname(os.path.dirname(__file__)), "config", "private_key.pem"))
    public_key_path = os.environ.get("AUTO_INVOICE_PUBLIC_KEY", os.path.join(os.path.dirname(os.path.dirname(__file__)), "config", "public_key.pem"))

    config_crypto = ConfigCrypto(config_path, private_key_path, public_key_path)
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
    downloader = InvoiceAttachmentDownloader()
    invoice_pdfs = downloader.download_invoice_attachments(invoice_emails)
    for invoice_pdf in invoice_pdfs:
        if not invoice_pdf[1]:
            email_client.set_email_unread(invoice_pdf[0])
            
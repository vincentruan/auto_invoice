#!/usr/bin/env python3
"""
Auto Invoice 使用示例
演示如何使用自动发票下载功能（支持加密配置文件自动解密）
"""

import os
from email_invoices.email_client import EmailClient
from email_invoices.invoice_attachment_downloader import InvoiceAttachmentDownloader
from email_invoices.crypto.config_crypto import ConfigCrypto

def main():
    """主函数 - 演示自动发票下载功能（支持加密配置文件自动解密）"""
    print("=== Auto Invoice 使用示例 ===")

    # 配置文件和密钥路径
    config_path = os.environ.get("AUTO_INVOICE_CONFIG", os.path.join("config", "config.json"))
    private_key_path = os.environ.get("AUTO_INVOICE_PRIVATE_KEY", os.path.join("config", "private_key.pem"))
    public_key_path = os.environ.get("AUTO_INVOICE_PUBLIC_KEY", os.path.join("config", "public_key.pem"))

    if not os.path.exists(config_path):
        print(f"错误: 配置文件 {config_path} 不存在")
        print("请先创建配置文件并设置邮箱信息")
        return

    try:
        # 使用ConfigCrypto自动解密配置文件
        config_crypto = ConfigCrypto(config_path, private_key_path, public_key_path)
        config = config_crypto.decrypt_config()
        if config is None:
            print("✗ 配置文件解密失败，请检查密钥文件和配置内容")
            return
        print("✓ 配置文件加载并解密成功")

        # 创建邮件客户端
        email_client = EmailClient(
            server=config["email"]["server"],
            username=config["email"]["username"],
            password=config["email"]["password"],
        )
        print("正在连接邮件服务器...")
        # 连接到邮件服务器
        if email_client.connect():
            print("✓ 邮件服务器连接成功")
            # 检查发票文件夹
            if email_client.invoice_folder_exists():
                print("✓ 发票文件夹已存在")
            else:
                print("✓ 发票文件夹已创建")
            # 获取发票邮件
            print("正在获取发票邮件...")
            invoice_emails = email_client.get_invoice_emails()
            if invoice_emails:
                print(f"✓ 找到 {len(invoice_emails)} 封发票邮件")
                # 创建下载器
                downloader = InvoiceAttachmentDownloader()
                # 下载发票附件
                print("正在下载发票附件...")
                invoice_pdfs = downloader.download_invoice_attachments(invoice_emails)
                print(f"✓ 下载完成，共处理 {len(invoice_pdfs)} 个文件")
                # 处理下载结果
                for invoice_pdf in invoice_pdfs:
                    if invoice_pdf[1]:  # 有文件路径
                        print(f"  - 已下载: {invoice_pdf[1]}")
                    else:  # 没有文件路径，标记为未读
                        print(f"  - 邮件 {invoice_pdf[0]} 无法下载，已标记为未读")
                        email_client.set_email_unread(invoice_pdf[0])
            else:
                print("✓ 没有找到新的发票邮件")
        else:
            print("✗ 邮件服务器连接失败")
            print("请检查配置文件中的邮箱信息是否正确")
    except FileNotFoundError:
        print(f"错误: 找不到配置文件 {config_path}")
    except Exception as e:
        print(f"错误: {e}")

if __name__ == "__main__":
    main() 
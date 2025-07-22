#!/usr/bin/env python3
"""
Playwright 浏览器测试脚本
验证 Chrome 浏览器是否正确安装和配置
"""

from playwright.sync_api import sync_playwright
import sys


def test_chrome_browser():
    """测试 Chrome 浏览器是否正常工作"""
    
    print("=== Playwright Chrome 浏览器测试 ===")
    
    try:
        with sync_playwright() as playwright:
            print("✓ Playwright 初始化成功")
            
            # 检查 Chrome 是否可用
            try:
                browser = playwright.chromium.launch(headless=True)
                print("✓ Chrome 浏览器启动成功")
                
                # 创建页面并访问测试网站
                page = browser.new_page()
                page.goto("https://www.google.com")
                title = page.title()
                print(f"✓ 成功访问网页，标题: {title}")
                
                # 关闭浏览器
                browser.close()
                print("✓ Chrome 浏览器测试完成")
                
                return True
                
            except Exception as e:
                print(f"✗ Chrome 浏览器测试失败: {e}")
                print("请运行: uv run playwright install chrome")
                return False
                
    except Exception as e:
        print(f"✗ Playwright 初始化失败: {e}")
        print("请检查 Playwright 是否正确安装")
        return False


def main():
    """主函数"""
    
    if test_chrome_browser():
        print("\n🎉 Playwright Chrome 配置正确！")
        print("可以正常使用自动发票下载功能。")
        sys.exit(0)
    else:
        print("\n❌ Playwright Chrome 配置有问题！")
        print("请按照以下步骤解决：")
        print("1. 运行: uv run playwright install chrome")
        print("2. 重新运行此测试脚本")
        sys.exit(1)


if __name__ == "__main__":
    main() 
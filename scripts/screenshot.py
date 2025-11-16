#!/usr/bin/env python3
import asyncio
from playwright.async_api import async_playwright
import os
from datetime import datetime
import sys

class WebpageScreenshot:
    def __init__(self):
        self.screenshot_dir = "screenshots"
        os.makedirs(self.screenshot_dir, exist_ok=True)
    
    async def take_screenshot(self, url, output_path=None):
        """截取网页截图"""
        async with async_playwright() as p:
            print("启动浏览器...")
            browser = await p.chromium.launch(
                headless=True,
                args=[
                    '--no-sandbox',
                    '--disable-setuid-sandbox',
                    '--disable-dev-shm-usage',
                    '--disable-accelerated-2d-canvas',
                    '--no-first-run',
                    '--no-zygote',
                    '--disable-gpu'
                ]
            )
            
            try:
                # 创建新页面
                page = await browser.new_page()
                
                # 设置视口大小
                await page.set_viewport_size({"width": 1920, "height": 1080})
                
                print(f"正在访问: {url}")
                # 导航到页面
                await page.goto(url, wait_until="networkidle", timeout=60000)
                
                # 等待页面完全加载
                await page.wait_for_timeout(5000)
                
                # 生成输出路径
                if not output_path:
                    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
                    output_path = os.path.join(
                        self.screenshot_dir, 
                        f"screenshot-{timestamp}.png"
                    )
                
                # 截取整个页面
                await page.screenshot(
                    path=output_path,
                    full_page=True,
                    type="jpeg",
                    quality=80
                )
                
                print(f"截图已保存: {output_path}")
                return output_path
                
            except Exception as e:
                print(f"截图过程中发生错误: {e}")
                raise e
            finally:
                await browser.close()

async def main():
    """主函数"""
    # 从环境变量获取URL，默认为GitHub
    url = os.getenv("WEBPAGE_URL", "https://github.com")
    
    screenshotter = WebpageScreenshot()
    
    try:
        output_path = await screenshotter.take_screenshot(url)
        print("截图完成!")
        return output_path
    except Exception as e:
        print(f"截图失败: {e}")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())

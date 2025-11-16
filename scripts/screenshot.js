const puppeteer = require('puppeteer');
const fs = require('fs');
const path = require('path');

async function takeScreenshot(url, outputPath) {
  console.log('Launching browser...');
  const browser = await puppeteer.launch({
    headless: true,
    args: [
      '--no-sandbox',
      '--disable-setuid-sandbox',
      '--disable-dev-shm-usage',
      '--disable-accelerated-2d-canvas',
      '--no-first-run',
      '--no-zygote',
      '--disable-gpu'
    ]
  });

  try {
    const page = await browser.newPage();
    
    // 设置视口大小
    await page.setViewport({ width: 1920, height: 1080 });
    
    console.log(`Navigating to: ${url}`);
    await page.goto(url, { 
      waitUntil: 'networkidle2',
      timeout: 30000 
    });

    // 等待页面完全加载
    await page.waitForTimeout(5000);

    // 创建输出目录
    const dir = path.dirname(outputPath);
    if (!fs.existsSync(dir)) {
      fs.mkdirSync(dir, { recursive: true });
    }

    // 截取整个页面
    await page.screenshot({ 
      path: outputPath,
      fullPage: true,
      type: 'jpeg',
      quality: 80
    });

    console.log(`Screenshot saved to: ${outputPath}`);
    
    return outputPath;
  } finally {
    await browser.close();
  }
}

// 主函数
async function main() {
  const url = process.env.WEBPAGE_URL || 'https://example.com';
  const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
  const outputPath = `screenshots/screenshot-${timestamp}.jpg`;

  try {
    await takeScreenshot(url, outputPath);
    console.log('Screenshot completed successfully');
  } catch (error) {
    console.error('Error taking screenshot:', error);
    process.exit(1);
  }
}

if (require.main === module) {
  main();
}

module.exports = takeScreenshot;

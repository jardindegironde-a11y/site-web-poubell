const { chromium } = require('playwright');
const path = require('path');

(async () => {
  const browser = await chromium.launch();
  const dir = __dirname;
  const targets = ['recto', 'verso'];
  for (const name of targets) {
    const page = await browser.newPage({
      viewport: { width: 1063, height: 1063 },
      deviceScaleFactor: 2
    });
    await page.goto('file://' + path.join(dir, name + '.html'));
    await page.waitForTimeout(300);
    const el = await page.$('#disc');
    await el.screenshot({ path: path.join(dir, name + '.png'), omitBackground: true });
    await page.close();
    console.log('rendered', name);
  }
  await browser.close();
})();

const { chromium } = require('C:/Projects/Portfolio Marketing OS/node_modules/playwright');
const path = require('path');
const fs = require('fs');

// Strip ICC / EXIF / Photoshop / Adobe / comment segments -> clean baseline JFIF (sRGB by default).
function stripMeta(src) {
  const out = [src[0], src[1]];
  let i = 2;
  while (i < src.length) {
    if (src[i] !== 0xFF) { out.push(src[i]); i++; continue; }
    const m = src[i + 1];
    if (m === 0xDA) { for (let k = i; k < src.length; k++) out.push(src[k]); break; }
    const len = src.readUInt16BE(i + 2);
    const strip = (m === 0xE1 || m === 0xE2 || m === 0xED || m === 0xEE || m === 0xFE);
    if (!strip) for (let k = i; k < i + 2 + len; k++) out.push(src[k]);
    i += 2 + len;
  }
  return Buffer.from(out);
}

async function exportJpeg(browser, hiPng, W, H, outPath) {
  const dp = await browser.newPage({ viewport: { width: W, height: H } });
  await dp.setContent('<canvas id="c"></canvas>');
  const jpg = await dp.evaluate(async ({ b64, W, H }) => {
    const img = new Image();
    img.src = 'data:image/png;base64,' + b64;
    await img.decode();
    const c = document.getElementById('c');
    c.width = W; c.height = H;
    const x = c.getContext('2d');
    x.imageSmoothingEnabled = true; x.imageSmoothingQuality = 'high';
    x.fillStyle = '#0D1321'; x.fillRect(0, 0, W, H);
    x.drawImage(img, 0, 0, W, H);
    return c.toDataURL('image/jpeg', 0.92).split(',')[1];
  }, { b64: hiPng.toString('base64'), W, H });
  await dp.close();
  const buf = stripMeta(Buffer.from(jpg, 'base64'));
  fs.writeFileSync(outPath, buf);
  console.log(path.basename(outPath), W + 'x' + H, (buf.length / 1024).toFixed(0) + 'KB',
    'ICC:', buf.indexOf(Buffer.from('ICC_PROFILE')) >= 0);
}

(async () => {
  const W = 1128, H = 191;
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: W, height: H }, deviceScaleFactor: 2 });
  const file = 'file://' + path.resolve('C:/Projects/PECWEB/banner-template.html').replace(/\\/g, '/');
  await page.goto(file, { waitUntil: 'networkidle' });
  await page.evaluate(() => document.fonts.ready);
  await page.waitForTimeout(400);
  const hi = await page.locator('.banner').screenshot(); // 2256x382 PNG buffer

  const dir = 'C:/Projects/PECWEB/assets/images/';
  await exportJpeg(browser, hi, W, H, dir + 'company-banner.jpg');        // 1x exact spec
  await exportJpeg(browser, hi, W * 2, H * 2, dir + 'company-banner-2x.jpg'); // 2x, same ratio

  await browser.close();
})();

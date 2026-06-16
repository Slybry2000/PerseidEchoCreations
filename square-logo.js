const { chromium } = require('C:/Projects/Portfolio Marketing OS/node_modules/playwright');
const path = require('path');
const fs = require('fs');

(async () => {
  const OUT = 800;          // square output px
  const FILL = 0.80;        // mark fills this fraction of the square (rest = inset for rounding)

  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: OUT, height: OUT } });
  await page.setContent('<canvas id="src"></canvas><canvas id="out"></canvas>');

  const srcPng = fs.readFileSync(path.resolve('C:/Projects/PECWEB/assets/images/PEC_Logo_Dark.png'));

  const result = await page.evaluate(async ({ b64, OUT, FILL }) => {
    const img = new Image();
    img.src = 'data:image/png;base64,' + b64;
    await img.decode();
    const W = img.naturalWidth, H = img.naturalHeight;

    const s = document.getElementById('src');
    s.width = W; s.height = H;
    const sx = s.getContext('2d');
    sx.drawImage(img, 0, 0);
    const data = sx.getImageData(0, 0, W, H).data;

    // background = top-left corner pixel
    const bg = [data[0], data[1], data[2]];
    // find bounding box of pixels that are clearly NOT background and not transparent
    let minX = W, minY = H, maxX = 0, maxY = 0, found = 0;
    const TH = 60; // colour-distance threshold
    for (let y = 0; y < H; y++) {
      for (let x = 0; x < W; x++) {
        const i = (y * W + x) * 4;
        const a = data[i + 3];
        if (a < 24) continue; // ignore transparent
        const dr = data[i] - bg[0], dg = data[i + 1] - bg[1], db = data[i + 2] - bg[2];
        if (dr * dr + dg * dg + db * db > TH * TH) {
          if (x < minX) minX = x; if (x > maxX) maxX = x;
          if (y < minY) minY = y; if (y > maxY) maxY = y;
          found++;
        }
      }
    }
    if (!found) { minX = 0; minY = 0; maxX = W - 1; maxY = H - 1; }
    const bw = maxX - minX + 1, bh = maxY - minY + 1;

    // compose square output, navy fill, mark centered at FILL scale (uniform, preserve aspect)
    const o = document.getElementById('out');
    o.width = OUT; o.height = OUT;
    const ox = o.getContext('2d');
    ox.imageSmoothingEnabled = true; ox.imageSmoothingQuality = 'high';
    // fill with the logo's OWN background navy so the crop blends seamlessly (no corner seams)
    ox.fillStyle = 'rgb(' + bg[0] + ',' + bg[1] + ',' + bg[2] + ')';
    ox.fillRect(0, 0, OUT, OUT);
    const target = OUT * FILL;
    const scale = Math.min(target / bw, target / bh);
    const dw = bw * scale, dh = bh * scale;
    const dx = (OUT - dw) / 2, dy = (OUT - dh) / 2;
    ox.drawImage(img, minX, minY, bw, bh, dx, dy, dw, dh);

    return { png: o.toDataURL('image/png').split(',')[1], bg, bw, bh, W, H };
  }, { b64: srcPng.toString('base64'), OUT, FILL });

  await browser.close();
  const buf = Buffer.from(result.png, 'base64');
  fs.writeFileSync('C:/Projects/PECWEB/assets/images/PEC_Logo_Square.png', buf);
  console.log('detected bg rgb', result.bg, '| mark bbox', result.bw + 'x' + result.bh, 'of', result.W + 'x' + result.H);
  console.log('PEC_Logo_Square.png', OUT + 'x' + OUT, (buf.length / 1024).toFixed(0) + 'KB');
})();

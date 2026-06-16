// One-off: animate the hero still into a loopable background video (Seedance 2.0 i2v). Safe to delete after.
import fs from 'node:fs';

const FAL_KEY = process.env.FAL_KEY ||
  (fs.existsSync('.env') ? fs.readFileSync('.env', 'utf8').match(/FAL_KEY=(.+)/)?.[1].trim() : null);
if (!FAL_KEY) { console.error('No FAL_KEY'); process.exit(1); }

const imgPath = 'assets/images/hero-bg-tasks.png';

// 1. Initiate Fal storage upload
const initRes = await fetch('https://rest.alpha.fal.ai/storage/upload/initiate', {
  method: 'POST',
  headers: { 'Authorization': `Key ${FAL_KEY}`, 'Content-Type': 'application/json' },
  body: JSON.stringify({ file_name: 'hero-bg-tasks.png', content_type: 'image/png' }),
});
const init = await initRes.json();
if (!init.upload_url || !init.file_url) { console.error('Upload init failed:', JSON.stringify(init).slice(0, 600)); process.exit(1); }

// 2. PUT the bytes
const putRes = await fetch(init.upload_url, {
  method: 'PUT', headers: { 'Content-Type': 'image/png' }, body: fs.readFileSync(imgPath),
});
if (!putRes.ok) { console.error('Upload PUT failed:', putRes.status, await putRes.text()); process.exit(1); }
console.log('Uploaded ->', init.file_url);

// 3. Generate image-to-video — subtle, loopable, notes stay static
const prompt = `Subtle cinematic ambient motion for a looping website hero background. Locked-off static camera — no camera movement, no zoom, no pan. The ONLY motion: thin wisps of steam rise gently and continuously from the coffee mug on the table; the warm desk lamp light softly breathes with a faint, slow flicker across the wall; a few almost-invisible dust motes drift slowly through the warm pool of light. The pinned paper notes, their handwriting, and the red AUTOMATED stamps stay completely still, sharp, and unchanged. One continuous shot. No cuts, no camera shake, no text morphing, nothing new appears or disappears. Calm, premium, quiet, dark and moody.`;

const body = {
  prompt,
  image_url: init.file_url,
  resolution: '720p',
  duration: '4',
  aspect_ratio: 'auto',
  generate_audio: false,
};
console.log('Generating (Pro 720p 4s, ~$1.20)... this can take 1-3 min.');
const genRes = await fetch('https://fal.run/bytedance/seedance-2.0/image-to-video', {
  method: 'POST',
  headers: { 'Authorization': `Key ${FAL_KEY}`, 'Content-Type': 'application/json' },
  body: JSON.stringify(body),
});
const gen = await genRes.json();
const videoUrl = gen?.video?.url;
if (!videoUrl) { console.error('No video URL in response:', JSON.stringify(gen).slice(0, 900)); process.exit(1); }
console.log('Video ready ->', videoUrl);

// 4. Download
const vbuf = Buffer.from(await (await fetch(videoUrl)).arrayBuffer());
fs.writeFileSync('assets/images/hero-tasks-loop.mp4', vbuf);
console.log('Saved: assets/images/hero-tasks-loop.mp4', (vbuf.length / 1024 / 1024).toFixed(2), 'MB');
console.log('DONE');

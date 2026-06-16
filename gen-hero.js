// One-off hero background generator (gpt-image-2 via Fal). Safe to delete after use.
import fs from 'node:fs';
import path from 'node:path';

const FAL_KEY = process.env.FAL_KEY ||
  (fs.existsSync('.env') ? fs.readFileSync('.env', 'utf8').match(/FAL_KEY=(.+)/)?.[1].trim() : null);
if (!FAL_KEY) { console.error('No FAL_KEY found'); process.exit(1); }

// Structured prompt — gpt-image-2 handles complex scenes better as JSON.
const promptObj = {
  type: "cinematic editorial photograph, wide website hero background plate",
  mood: "moody, dark, intimate, warm; lit-to-dark; quiet authority; premium",
  scene: "a dark home-office corner at night. A dark, textured charcoal plaster wall fills the frame. A black anglepoise desk lamp stands at the FAR RIGHT, switched on, throwing a soft warm tungsten pool of light across the wall. At the lower LEFT, on a small round wood side table, a steaming coffee mug and a closed leather notebook.",
  focal_left: "On the LEFT side of the wall, a small tidy cluster of about five kraft / manila paper notes is pinned up. Each note shows ONE short handwritten busy-work task in black marker, with a single bold diagonal line struck through it (crossed out), and a red rubber-stamp word 'AUTOMATED' angled across the note.",
  notes_should_read: ["Email replies", "Invoices", "Follow-ups", "Scheduling", "Reports"],
  stamp_text: "AUTOMATED",
  right_side: "the RIGHT THIRD of the frame is deliberately dark and almost empty — just the warm lamp glow fading into shadowed wall — leaving clean negative space for white headline text to be overlaid later",
  lettering: "authentic human handwriting in black marker on the notes (short, legible); the word AUTOMATED as a bold red rubber-stamp imprint, slightly rough",
  lighting: "warm tungsten key light from the right lamp; deep soft shadows on the left; cinematic chiaroscuro",
  style: "photoreal, 35mm, shallow depth of field, gentle film grain, editorial — NOT illustration, NOT cartoon",
  palette: "near-black charcoal/navy wall, warm amber lamp light, kraft-tan paper notes, a pop of red on the AUTOMATED stamps",
  composition: "wide 16:9; visual mass (notes + lamp + mug) anchored left and right edges, dark empty space toward the right-center for text",
  negative: "no gibberish text, no extra logos, no watermark, avoid clutter"
};

const body = {
  prompt: JSON.stringify(promptObj, null, 2),
  image_size: { width: 1792, height: 1024 },
  quality: "medium",
  num_images: 4,
  output_format: "png"
};

const outDir = './hero-candidates';
fs.mkdirSync(outDir, { recursive: true });

const res = await fetch('https://fal.run/openai/gpt-image-2', {
  method: 'POST',
  headers: { 'Authorization': `Key ${FAL_KEY}`, 'Content-Type': 'application/json' },
  body: JSON.stringify(body),
});
const json = await res.json();
if (!json.images?.length) { console.error('No images:', JSON.stringify(json).slice(0, 800)); process.exit(1); }

for (let i = 0; i < json.images.length; i++) {
  const fp = path.join(outDir, `hero_cand_${i + 1}.png`);
  const buf = Buffer.from(await (await fetch(json.images[i].url)).arrayBuffer());
  fs.writeFileSync(fp, buf);
  console.log('Saved:', fp);
}
console.log('DONE');

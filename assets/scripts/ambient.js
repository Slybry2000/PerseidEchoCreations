// Ambient: canvas mesh gradient (replaces/augments .bg-mesh div)
// Palette: PECWEB cyan/blue/purple. Falls back to CSS .bg-mesh when reduced-motion or no canvas.
(function () {
    'use strict';

    const reduced = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    if (reduced) return;

    const canvas = document.getElementById('pec-mesh-canvas');
    if (!canvas || !canvas.getContext) return;

    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    // PECWEB palette translated to rgba blobs. Low alpha — this lives behind everything.
    const BG = '#030818';
    const BLOBS = [
        { color: 'rgba(74, 211, 197, 0.22)' },   // cyan
        { color: 'rgba(30, 70, 141, 0.22)' },    // deep blue
        { color: 'rgba(46, 138, 133, 0.18)' },   // teal
        { color: 'rgba(86, 61, 140, 0.18)' }     // indigo
    ].map((b) => ({
        ...b,
        x: Math.random(),
        y: Math.random(),
        vx: (Math.random() - 0.5) * 0.35,
        vy: (Math.random() - 0.5) * 0.35,
        r: 0.35 + Math.random() * 0.2
    }));

    function resize() {
        const dpr = Math.min(window.devicePixelRatio || 1, 2);
        canvas.width = canvas.offsetWidth * dpr;
        canvas.height = canvas.offsetHeight * dpr;
    }
    resize();
    window.addEventListener('resize', resize);

    function draw() {
        const w = canvas.width;
        const h = canvas.height;
        ctx.fillStyle = BG;
        ctx.fillRect(0, 0, w, h);
        for (const b of BLOBS) {
            b.x += b.vx / w;
            b.y += b.vy / h;
            if (b.x < -0.2 || b.x > 1.2) b.vx *= -1;
            if (b.y < -0.2 || b.y > 1.2) b.vy *= -1;
            const grd = ctx.createRadialGradient(
                b.x * w, b.y * h, 0,
                b.x * w, b.y * h, b.r * Math.max(w, h)
            );
            grd.addColorStop(0, b.color);
            grd.addColorStop(1, 'transparent');
            ctx.globalCompositeOperation = 'lighter';
            ctx.fillStyle = grd;
            ctx.fillRect(0, 0, w, h);
            ctx.globalCompositeOperation = 'source-over';
        }
        requestAnimationFrame(draw);
    }
    draw();
})();

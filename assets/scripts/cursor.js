// Cursor: soft cyan glow trail that follows the pointer.
// Skipped on touch devices and when prefers-reduced-motion.
(function () {
    'use strict';

    const reduced = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    const isTouch = window.matchMedia && window.matchMedia('(hover: none)').matches;
    if (reduced || isTouch) return;

    const glow = document.querySelector('.pec-cursor-glow');
    if (!glow) return;

    let mx = window.innerWidth / 2;
    let my = window.innerHeight / 2;
    let gx = mx;
    let gy = my;

    document.addEventListener('pointermove', (e) => {
        mx = e.clientX;
        my = e.clientY;
    }, { passive: true });

    function tick() {
        gx += (mx - gx) * 0.12;
        gy += (my - gy) * 0.12;
        glow.style.transform = `translate3d(${gx - 250}px, ${gy - 250}px, 0)`;
        requestAnimationFrame(tick);
    }
    tick();

    // Reveal the glow once we've warmed up (avoids the initial flash at 0,0)
    requestAnimationFrame(() => glow.classList.add('is-active'));
})();

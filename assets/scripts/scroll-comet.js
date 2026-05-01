// Scroll-driven comet: flies diagonally across the full viewport
// as the user scrolls the page. Down-scroll moves it in the
// direction of travel; the tail trails behind opposite that direction.
(function () {
    'use strict';

    const reduced = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    if (reduced) return;

    const comet = document.getElementById('pec-scroll-comet');
    if (!comet) return;

    // Trajectory endpoints expressed as fractions of viewport (vw/vh).
    // Start: off-screen upper-right. End: off-screen lower-left.
    // Matches the diagonal already established by the hero SVG comet.
    const START = { x: 1.10, y: -0.10 };
    const END   = { x: -0.20, y: 1.10 };

    let vw = window.innerWidth;
    let vh = window.innerHeight;
    let scrollMax = 1;
    let progress = 0;
    let target = 0;
    let ticking = false;

    function measure() {
        vw = window.innerWidth;
        vh = window.innerHeight;
        const doc = document.documentElement;
        scrollMax = Math.max(1, (doc.scrollHeight - vh));
    }

    // Pre-compute the angle once — it's constant for a fixed trajectory.
    function computeAngle() {
        const dx = (END.x - START.x) * vw;
        const dy = (END.y - START.y) * vh;
        // Tail wrapper points right by default; rotate so the head
        // leads in (dx, dy) direction.
        return Math.atan2(dy, dx) * (180 / Math.PI);
    }

    function apply() {
        ticking = false;
        // Smooth toward target for a slightly floaty feel without
        // breaking the scroll-driven mapping.
        progress += (target - progress) * 0.18;
        const x = (START.x + (END.x - START.x) * progress) * vw;
        const y = (START.y + (END.y - START.y) * progress) * vh;
        comet.style.setProperty('--pec-comet-x', x + 'px');
        comet.style.setProperty('--pec-comet-y', y + 'px');

        // Keep RAF-ing while the eased value hasn't settled.
        if (Math.abs(target - progress) > 0.0005) {
            requestAnimationFrame(apply);
            ticking = true;
        }
    }

    function onScroll() {
        target = Math.min(1, Math.max(0, window.scrollY / scrollMax));
        if (!ticking) {
            ticking = true;
            requestAnimationFrame(apply);
        }
    }

    function onResize() {
        measure();
        comet.style.setProperty('--pec-comet-angle', computeAngle() + 'deg');
        onScroll();
    }

    measure();
    comet.style.setProperty('--pec-comet-angle', computeAngle() + 'deg');
    // Initialise progress at current scroll without easing.
    progress = target = Math.min(1, Math.max(0, window.scrollY / scrollMax));
    const x0 = (START.x + (END.x - START.x) * progress) * vw;
    const y0 = (START.y + (END.y - START.y) * progress) * vh;
    comet.style.setProperty('--pec-comet-x', x0 + 'px');
    comet.style.setProperty('--pec-comet-y', y0 + 'px');

    window.addEventListener('scroll', onScroll, { passive: true });
    window.addEventListener('resize', onResize);
})();

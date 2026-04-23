// Section transformations:
//   - odometer count-up (Apps strip)
//   - svg-draw stroke animation on scroll-in (Product + Now)
//   - one-shot glitch-effect on Contact H2 scroll-in
//   - spotlight-border cursor tracking (Support cards)
//   - zoom-parallax divider (Now)
//   - color-shift ambient hue drift across sections
//   - flip-card tap support on touch devices
(function () {
    'use strict';

    const reduced = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;

    /* ─── Odometer count-up ─── */
    function countUp(el, target, suffix, durationMs) {
        const start = performance.now();
        const startVal = 0;
        const tick = (now) => {
            const p = Math.min((now - start) / durationMs, 1);
            const eased = 1 - Math.pow(1 - p, 3);
            const val = Math.round(startVal + (target - startVal) * eased);
            el.textContent = `${val.toLocaleString()}${suffix || ''}`;
            if (p < 1) requestAnimationFrame(tick);
        };
        requestAnimationFrame(tick);
    }

    function initOdometers() {
        const targets = document.querySelectorAll('[data-pec-count]');
        if (!targets.length) return;
        const io = new IntersectionObserver((entries, obs) => {
            entries.forEach((entry) => {
                if (!entry.isIntersecting) return;
                const el = entry.target;
                const target = Number(el.dataset.pecCount) || 0;
                const suffix = el.dataset.pecCountSuffix || '';
                if (reduced) {
                    el.textContent = `${target.toLocaleString()}${suffix}`;
                } else {
                    countUp(el, target, suffix, 1500);
                }
                obs.unobserve(el);
            });
        }, { threshold: 0.4 });
        targets.forEach((el) => io.observe(el));
    }

    /* ─── SVG draw-in on scroll ─── */
    function initSvgDraws() {
        const targets = document.querySelectorAll('.pec-draw-check');
        if (!targets.length) return;
        const io = new IntersectionObserver((entries, obs) => {
            entries.forEach((entry) => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('is-drawn');
                    obs.unobserve(entry.target);
                }
            });
        }, { threshold: 0.5 });
        targets.forEach((el) => io.observe(el));
    }

    /* ─── Glitch (one-shot on Contact H2 entering view) ─── */
    function initGlitch() {
        const targets = document.querySelectorAll('.pec-glitch');
        if (!targets.length) return;
        const io = new IntersectionObserver((entries, obs) => {
            entries.forEach((entry) => {
                if (!entry.isIntersecting) return;
                const el = entry.target;
                if (!reduced) {
                    el.classList.add('is-glitching');
                    setTimeout(() => el.classList.remove('is-glitching'), 950);
                }
                obs.unobserve(el);
            });
        }, { threshold: 0.5 });
        targets.forEach((el) => io.observe(el));
    }

    /* ─── Spotlight-border cursor tracking ─── */
    function initSpotlight() {
        const targets = document.querySelectorAll('.pec-spotlight');
        targets.forEach((card) => {
            card.addEventListener('pointermove', (e) => {
                const rect = card.getBoundingClientRect();
                card.style.setProperty('--spot-x', `${e.clientX - rect.left}px`);
                card.style.setProperty('--spot-y', `${e.clientY - rect.top}px`);
            });
            card.addEventListener('pointerleave', () => {
                card.style.setProperty('--spot-x', '-300px');
                card.style.setProperty('--spot-y', '-300px');
            });
        });
    }

    /* ─── Zoom-parallax divider ─── */
    function initZoomDivider() {
        const divider = document.querySelector('.pec-zoom-divider');
        if (!divider) return;
        const word = divider.querySelector('.pec-zoom-word');
        if (!word) return;
        if (reduced) return;

        let ticking = false;
        const onScroll = () => {
            if (ticking) return;
            ticking = true;
            requestAnimationFrame(() => {
                const rect = divider.getBoundingClientRect();
                const vh = window.innerHeight;
                // Distance from viewport center, normalized to [-1, 1]
                const mid = rect.top + rect.height / 2;
                const delta = (mid - vh / 2) / vh;
                const abs = Math.min(Math.abs(delta), 1);
                const scale = 1 + (1 - abs) * 0.35;
                const opacity = 0.25 + (1 - abs) * 0.75;
                word.style.setProperty('--pec-zoom-scale', scale.toFixed(3));
                word.style.setProperty('--pec-zoom-opacity', opacity.toFixed(3));
                ticking = false;
            });
        };
        window.addEventListener('scroll', onScroll, { passive: true });
        onScroll();
    }

    /* ─── Color-shift ambient drift ─── */
    // As the user scrolls through sections, the body's --pec-hue drifts.
    // We pick per-section hue offsets so the mesh gradient lightly shifts
    // navy → teal → blue → purple → back.
    function initColorShift() {
        if (reduced) return;
        const zones = [
            { sel: '.hero', hue: '0deg' },
            { sel: '#apps', hue: '-18deg' },
            { sel: '#products', hue: '18deg' },
            { sel: '#about', hue: '42deg' },
            { sel: '#now', hue: '-32deg' },
            { sel: '#support', hue: '-10deg' },
            { sel: '#contact', hue: '0deg' }
        ].map((z) => ({ hue: z.hue, el: document.querySelector(z.sel) })).filter((z) => z.el);
        if (!zones.length) return;

        let ticking = false;
        const onScroll = () => {
            if (ticking) return;
            ticking = true;
            requestAnimationFrame(() => {
                const mid = window.innerHeight / 2;
                let active = zones[0];
                let bestDist = Infinity;
                for (const z of zones) {
                    const rect = z.el.getBoundingClientRect();
                    const center = rect.top + rect.height / 2;
                    const dist = Math.abs(center - mid);
                    if (dist < bestDist) { bestDist = dist; active = z; }
                }
                document.body.style.setProperty('--pec-hue', active.hue);
                ticking = false;
            });
        };
        window.addEventListener('scroll', onScroll, { passive: true });
        onScroll();
    }

    /* ─── Flip card tap support (touch devices) ─── */
    function initFlipCardTap() {
        const cards = document.querySelectorAll('.pec-flip-card');
        cards.forEach((card) => {
            // Allow keyboard flip on Enter/Space
            card.addEventListener('keydown', (e) => {
                if (e.key === 'Enter' || e.key === ' ') {
                    e.preventDefault();
                    card.classList.toggle('is-flipped');
                }
            });
            // Tap-to-flip on touch devices (hover doesn't fire)
            if (window.matchMedia && window.matchMedia('(hover: none)').matches) {
                card.addEventListener('click', (e) => {
                    // Don't intercept link clicks inside the card
                    if (e.target.closest('a')) return;
                    card.classList.toggle('is-flipped');
                });
            }
        });
    }

    /* ───────────────────────── boot ───────────────────────── */
    function start() {
        initOdometers();
        initSvgDraws();
        initGlitch();
        initSpotlight();
        initZoomDivider();
        initColorShift();
        initFlipCardTap();
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', start);
    } else {
        start();
    }
})();

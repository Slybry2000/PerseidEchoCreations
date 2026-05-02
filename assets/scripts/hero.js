// Hero cinema: text-mask reveal, text-scramble, typewriter, particle-button,
// dynamic-island status pill, image-trail scoped to .hero-visual.
(function () {
    'use strict';

    const reduced = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;

    /* ─────────────────────────────────────────────────────────────
       1. text-mask reveal on hero H1
       Uses GSAP ScrollTrigger to animate the fill layer's clip-path
       as the user scrolls through the first viewport. Fallback when
       GSAP is missing or reduced-motion: reveal instantly.
       ───────────────────────────────────────────────────────────── */
    function initTextMask() {
        const fill = document.querySelector('.pec-mask-fill');
        if (!fill) return;
        if (reduced || !window.gsap || !window.ScrollTrigger) {
            fill.style.clipPath = 'inset(0% 0 0 0)';
            return;
        }
        window.gsap.registerPlugin(window.ScrollTrigger);
        window.gsap.to(fill, {
            clipPath: 'inset(0% 0 0 0)',
            ease: 'none',
            scrollTrigger: {
                trigger: '.hero',
                start: 'top top',
                end: 'bottom 30%',
                scrub: 0.4
            }
        });
    }

    /* ─────────────────────────────────────────────────────────────
       2. text-scramble — applied to any element with [data-pec-scramble]
       ───────────────────────────────────────────────────────────── */
    const SCRAMBLE_CHARS = '!<>-_\\/[]{}—=+*^?#________';

    function scrambleText(el, finalText, duration) {
        const len = finalText.length;
        const start = performance.now();
        const frame = (now) => {
            const p = Math.min((now - start) / duration, 1);
            let html = '';
            let wordOpen = false;
            const openWord = () => { html += '<span class="pec-scramble-word">'; wordOpen = true; };
            const closeWord = () => { if (wordOpen) { html += '</span>'; wordOpen = false; } };
            for (let i = 0; i < len; i++) {
                const ch = finalText[i];
                if (ch === ' ') { closeWord(); html += ' '; continue; }
                if (!wordOpen) openWord();
                const threshold = (i / len) * 0.7 + 0.15;
                if (p >= threshold) {
                    html += `<span class="pec-scramble-char resolved">${ch}</span>`;
                } else {
                    const r = SCRAMBLE_CHARS[Math.floor(Math.random() * SCRAMBLE_CHARS.length)];
                    html += `<span class="pec-scramble-char scrambling">${r}</span>`;
                }
            }
            closeWord();
            el.innerHTML = html;
            if (p < 1) requestAnimationFrame(frame);
        };
        requestAnimationFrame(frame);
    }

    function initScrambles() {
        const targets = document.querySelectorAll('[data-pec-scramble]');
        targets.forEach((el) => {
            const finalText = el.dataset.pecScramble;
            if (!finalText) return;
            if (reduced) { el.textContent = finalText; return; }
            // Run when the element scrolls into view (or immediately if already visible)
            const run = () => scrambleText(el, finalText, 1100);
            const rect = el.getBoundingClientRect();
            if (rect.top < window.innerHeight && rect.bottom > 0) {
                // Small delay so it's noticeable after initial load
                setTimeout(run, 250);
            } else {
                const io = new IntersectionObserver((entries, obs) => {
                    entries.forEach((entry) => {
                        if (entry.isIntersecting) {
                            run();
                            obs.unobserve(entry.target);
                        }
                    });
                }, { threshold: 0.3 });
                io.observe(el);
            }
        });
    }

    /* ─────────────────────────────────────────────────────────────
       3. typewriter — element with [data-pec-typewriter="text"]
       On completion: reveals the next sibling with .pec-sub-rest
       ───────────────────────────────────────────────────────────── */
    function typewriter(el, text, speedMs) {
        let i = 0;
        const rest = el.parentElement && el.parentElement.querySelector('.pec-sub-rest');
        const tick = () => {
            if (i <= text.length) {
                el.textContent = text.slice(0, i);
                i++;
                setTimeout(tick, speedMs);
            } else {
                el.classList.add('is-done');
                if (rest) rest.classList.add('is-visible');
            }
        };
        tick();
    }

    function initTypewriters() {
        document.querySelectorAll('[data-pec-typewriter]').forEach((el) => {
            const text = el.dataset.pecTypewriter;
            if (!text) return;
            const rest = el.parentElement && el.parentElement.querySelector('.pec-sub-rest');
            if (reduced) {
                el.textContent = text;
                el.classList.add('is-done');
                if (rest) rest.classList.add('is-visible');
                return;
            }
            // Start typing after a short delay for initial load feel
            setTimeout(() => typewriter(el, text, 28), 400);
        });
    }

    /* ─────────────────────────────────────────────────────────────
       4. particle-button — click bursts on [data-pec-particles]
       Uses PECWEB cyan/blue/purple palette.
       ───────────────────────────────────────────────────────────── */
    const PARTICLE_COLORS = ['#4ad3c5', '#1e468d', '#2e8a85', '#f7f8fb'];

    function spawnParticles(cx, cy) {
        if (reduced) return;
        const count = 18;
        for (let i = 0; i < count; i++) {
            const p = document.createElement('div');
            p.className = 'pec-particle';
            p.style.left = `${cx}px`;
            p.style.top = `${cy}px`;
            p.style.background = PARTICLE_COLORS[i % PARTICLE_COLORS.length];
            p.style.boxShadow = `0 0 10px ${PARTICLE_COLORS[i % PARTICLE_COLORS.length]}`;
            document.body.appendChild(p);
            const angle = Math.random() * Math.PI * 2;
            const dist = 50 + Math.random() * 80;
            const dx = Math.cos(angle) * dist;
            const dy = Math.sin(angle) * dist - 30;
            // Force reflow, then animate
            // eslint-disable-next-line no-unused-expressions
            p.offsetHeight;
            p.style.transform = `translate(${dx}px, ${dy}px) scale(0.2)`;
            p.style.opacity = '0';
            setTimeout(() => p.remove(), 750);
        }
    }

    function initParticleButtons() {
        document.querySelectorAll('[data-pec-particles]').forEach((btn) => {
            btn.addEventListener('click', (e) => {
                const rect = btn.getBoundingClientRect();
                spawnParticles(rect.left + rect.width / 2, rect.top + rect.height / 2);
            });
        });
    }

    /* ─────────────────────────────────────────────────────────────
       5. dynamic-island status pill
       ───────────────────────────────────────────────────────────── */
    const ISLAND_STATES = [
        { dot: '#4ad3c5', text: 'Available for engagements' },
        { dot: '#4ad3c5', text: 'GFC live on App Store, Play, and web' },
        { dot: '#2e8a85', text: 'Deep work mode' },
        { dot: '#4ad3c5', text: 'Inbox open — Bryan@perseidechocreations.com' }
    ];

    function initIsland() {
        const island = document.getElementById('pec-island');
        if (!island) return;
        const dot = island.querySelector('.pec-island-dot');
        const text = island.querySelector('.pec-island-text');
        if (!dot || !text) return;
        let idx = 0;
        // Initialize with the first state immediately
        text.textContent = ISLAND_STATES[0].text;
        dot.style.background = ISLAND_STATES[0].dot;
        dot.style.boxShadow = `0 0 8px ${ISLAND_STATES[0].dot}`;
        if (reduced) return;

        const rotate = () => {
            idx = (idx + 1) % ISLAND_STATES.length;
            const next = ISLAND_STATES[idx];
            island.classList.add('is-morphing');
            setTimeout(() => {
                text.textContent = next.text;
                dot.style.background = next.dot;
                dot.style.boxShadow = `0 0 8px ${next.dot}`;
                island.classList.remove('is-morphing');
            }, 280);
        };
        setInterval(rotate, 5000);
    }

    /* ─────────────────────────────────────────────────────────────
       6. image-trail — cyan echo dots inside .hero-visual only
       ───────────────────────────────────────────────────────────── */
    function initEchoTrail() {
        if (reduced) return;
        const host = document.getElementById('pec-hero-visual');
        if (!host) return;
        let lastSpawn = 0;
        host.addEventListener('pointermove', (e) => {
            const now = performance.now();
            if (now - lastSpawn < 60) return; // throttle spawn rate
            lastSpawn = now;
            const dot = document.createElement('div');
            dot.className = 'pec-echo-dot';
            dot.style.left = `${e.clientX}px`;
            dot.style.top = `${e.clientY}px`;
            document.body.appendChild(dot);
            // Next frame: drift outward and fade
            requestAnimationFrame(() => {
                const drift = 20 + Math.random() * 30;
                const angle = Math.random() * Math.PI * 2;
                dot.style.transform = `translate(calc(-50% + ${Math.cos(angle) * drift}px), calc(-50% + ${Math.sin(angle) * drift}px)) scale(0.3)`;
                dot.style.opacity = '0';
            });
            setTimeout(() => dot.remove(), 950);
        }, { passive: true });
    }

    /* ───────────────────────────── boot ───────────────────────────── */
    function start() {
        initTextMask();
        initScrambles();
        initTypewriters();
        initParticleButtons();
        initIsland();
        initEchoTrail();
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', start);
    } else {
        start();
    }
})();

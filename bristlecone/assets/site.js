// Bristlecone — minimal site JS
// Subtle reveal on scroll (honoring prefers-reduced-motion) + mobile nav toggle.

(function () {
  const reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  // Reveal on intersect
  if (!reduced && 'IntersectionObserver' in window) {
    const io = new IntersectionObserver(
      (entries) => {
        for (const e of entries) {
          if (e.isIntersecting) {
            e.target.classList.add('in');
            io.unobserve(e.target);
          }
        }
      },
      { rootMargin: '0px 0px -8% 0px', threshold: 0.08 }
    );
    document.querySelectorAll('.reveal').forEach((el) => io.observe(el));
  } else {
    document.querySelectorAll('.reveal').forEach((el) => el.classList.add('in'));
  }

  // Mobile nav
  const toggle = document.querySelector('.nav-toggle');
  const nav = document.querySelector('.nav');
  if (toggle && nav) {
    toggle.addEventListener('click', () => {
      nav.classList.toggle('open');
      toggle.setAttribute('aria-expanded', nav.classList.contains('open'));
    });
  }

  // Pipeline diagram — one-shot draw when scrolled into view
  const pipelines = document.querySelectorAll('[data-draw-pipeline]');
  pipelines.forEach((svg) => {
    const lines = svg.querySelectorAll('[data-draw-line]');
    if (!lines.length) return;
    lines.forEach((line) => {
      const len = line.getTotalLength();
      line.style.strokeDasharray = len;
      line.style.strokeDashoffset = len;
    });
    if (reduced) {
      lines.forEach((line) => { line.style.strokeDashoffset = 0; });
      svg.classList.add('drawn');
      return;
    }
    if ('IntersectionObserver' in window) {
      const pipeIO = new IntersectionObserver(
        (entries) => {
          for (const e of entries) {
            if (e.isIntersecting) {
              lines.forEach((line) => {
                const delay = parseInt(line.dataset.delay || '0', 10);
                setTimeout(() => { line.style.strokeDashoffset = '0'; }, delay);
              });
              svg.classList.add('drawn');
              pipeIO.unobserve(svg);
            }
          }
        },
        { threshold: 0.4 }
      );
      pipeIO.observe(svg);
    } else {
      lines.forEach((line) => { line.style.strokeDashoffset = 0; });
      svg.classList.add('drawn');
    }
  });

})();

(function () {
    const modal = document.getElementById('pec-contact-modal');
    if (!modal) return;

    const form = document.getElementById('pec-contact-form');
    const status = document.getElementById('pec-contact-status');
    const success = document.getElementById('pec-contact-success');
    const submitBtn = form ? form.querySelector('.pec-contact-submit') : null;
    const panel = modal.querySelector('.pec-contact-panel');

    let lastFocused = null;

    function focusableElements() {
        return panel.querySelectorAll(
            'button, [href], input, textarea, select, [tabindex]:not([tabindex="-1"])'
        );
    }

    function openModal() {
        lastFocused = document.activeElement;
        modal.classList.add('is-open');
        modal.setAttribute('aria-hidden', 'false');
        document.body.classList.add('pec-contact-locked');
        // Reset state if reopened after a successful send
        if (success.classList.contains('is-visible')) {
            success.classList.remove('is-visible');
            success.setAttribute('aria-hidden', 'true');
            form.style.display = '';
            form.reset();
            status.textContent = '';
            status.classList.remove('is-error');
        }
        setTimeout(() => {
            const firstInput = form.querySelector('input[name="name"]');
            if (firstInput) firstInput.focus();
        }, 350);
    }

    function closeModal() {
        modal.classList.remove('is-open');
        modal.setAttribute('aria-hidden', 'true');
        document.body.classList.remove('pec-contact-locked');
        if (lastFocused && typeof lastFocused.focus === 'function') {
            lastFocused.focus();
        }
    }

    document.querySelectorAll('[data-pec-contact-open]').forEach((trigger) => {
        trigger.addEventListener('click', (e) => {
            e.preventDefault();
            openModal();
        });
    });

    document.querySelectorAll('[data-pec-contact-close]').forEach((trigger) => {
        trigger.addEventListener('click', (e) => {
            e.preventDefault();
            closeModal();
        });
    });

    document.addEventListener('keydown', (e) => {
        if (!modal.classList.contains('is-open')) return;
        if (e.key === 'Escape') {
            closeModal();
            return;
        }
        if (e.key === 'Tab') {
            const focusables = Array.from(focusableElements()).filter(
                (el) => !el.hasAttribute('disabled') && el.offsetParent !== null
            );
            if (!focusables.length) return;
            const first = focusables[0];
            const last = focusables[focusables.length - 1];
            if (e.shiftKey && document.activeElement === first) {
                e.preventDefault();
                last.focus();
            } else if (!e.shiftKey && document.activeElement === last) {
                e.preventDefault();
                first.focus();
            }
        }
    });

    if (!form) return;

    const TO = 'Bryan@perseidechocreations.com';

    form.addEventListener('submit', (e) => {
        e.preventDefault();

        const honey = form.querySelector('input[name="_honey"]');
        if (honey && honey.value) return;

        if (!form.checkValidity()) {
            form.reportValidity();
            return;
        }

        const data = new FormData(form);
        const name = (data.get('name') || '').toString().trim();
        const email = (data.get('email') || '').toString().trim();
        const topic = (data.get('topic') || '').toString().trim();
        const message = (data.get('message') || '').toString().trim();

        const subject = topic ? `[Perseid Echo] ${topic}` : '[Perseid Echo] New enquiry';
        const body =
            `Hi Bryan,\n\n${message}\n\n— ${name}\nReply to: ${email}\n\n` +
            `(Sent from the contact form on perseidechocreations.com)`;

        const mailto = `mailto:${TO}?subject=${encodeURIComponent(subject)}&body=${encodeURIComponent(body)}`;

        status.classList.remove('is-error');
        status.textContent = 'Opening your email app…';
        submitBtn.classList.add('is-loading');
        submitBtn.disabled = true;

        window.location.href = mailto;

        setTimeout(() => {
            submitBtn.classList.remove('is-loading');
            submitBtn.disabled = false;
            form.style.display = 'none';
            success.classList.add('is-visible');
            success.setAttribute('aria-hidden', 'false');
            status.textContent = '';
        }, 600);
    });
})();

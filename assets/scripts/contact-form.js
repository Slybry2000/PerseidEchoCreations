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

    const iframe = document.getElementById('pec-contact-iframe');
    let pending = false;
    let timeoutId = null;

    function showSuccess() {
        if (!pending) return;
        pending = false;
        clearTimeout(timeoutId);
        submitBtn.classList.remove('is-loading');
        submitBtn.disabled = false;
        form.style.display = 'none';
        success.classList.add('is-visible');
        success.setAttribute('aria-hidden', 'false');
        status.textContent = '';
    }

    function showError(msg) {
        if (!pending) return;
        pending = false;
        clearTimeout(timeoutId);
        submitBtn.classList.remove('is-loading');
        submitBtn.disabled = false;
        status.classList.add('is-error');
        status.textContent = msg || 'Something went wrong. Email Bryan@perseidechocreations.com directly.';
    }

    if (iframe) {
        iframe.addEventListener('load', () => {
            if (pending) showSuccess();
        });
    }

    form.addEventListener('submit', (e) => {
        // Honeypot — silently bail if filled
        const honey = form.querySelector('input[name="_honey"]');
        if (honey && honey.value) {
            e.preventDefault();
            return;
        }

        if (!form.checkValidity()) {
            e.preventDefault();
            form.reportValidity();
            return;
        }

        // Let the native submit fire into the hidden iframe; iframe.load shows success
        status.classList.remove('is-error');
        status.textContent = 'Sending…';
        submitBtn.classList.add('is-loading');
        submitBtn.disabled = true;
        pending = true;

        // Fallback: if the iframe never fires load within 12s, surface an error
        timeoutId = setTimeout(() => {
            showError('Send timed out. Email Bryan@perseidechocreations.com directly.');
        }, 12000);
    });
})();

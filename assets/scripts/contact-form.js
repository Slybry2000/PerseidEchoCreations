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

    form.addEventListener('submit', async (e) => {
        e.preventDefault();

        const honey = form.querySelector('input[name="_honey"]');
        if (honey && honey.value) return;

        if (!form.checkValidity()) {
            form.reportValidity();
            return;
        }

        status.classList.remove('is-error');
        status.textContent = 'Sending…';
        submitBtn.classList.add('is-loading');
        submitBtn.disabled = true;

        try {
            const payload = {};
            new FormData(form).forEach((value, key) => {
                if (key !== '_honey') payload[key] = value;
            });

            const res = await fetch(form.action, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    Accept: 'application/json'
                },
                body: JSON.stringify(payload)
            });

            const json = await res.json().catch(() => ({}));
            const ok = res.ok && (json.success === true || String(json.success).toLowerCase() === 'true');

            if (!ok) {
                const msg = (json && json.message) || `Submission failed (HTTP ${res.status})`;
                throw new Error(msg);
            }

            form.style.display = 'none';
            success.classList.add('is-visible');
            success.setAttribute('aria-hidden', 'false');
            status.textContent = '';
        } catch (err) {
            status.classList.add('is-error');
            status.textContent = err && err.message
                ? err.message
                : 'Something went wrong. Email Bryan@perseidechocreations.com directly.';
            console.error('[contact-form]', err);
        } finally {
            submitBtn.classList.remove('is-loading');
            submitBtn.disabled = false;
        }
    });
})();

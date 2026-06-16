(function () {
    const form = document.getElementById('pec-contact-form');
    if (!form) return;

    const status = document.getElementById('pec-contact-status');
    const success = document.getElementById('pec-contact-success');
    const submitBtn = form.querySelector('.pec-contact-submit');

    const EMAIL_RE = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

    const fields = [
        {
            name: 'name',
            validate: (v) =>
                v.trim().length === 0 ? 'Tell me what to call you.' : ''
        },
        {
            name: 'email',
            validate: (v) => {
                const t = v.trim();
                if (t.length === 0) return "I'll need an email to reply to.";
                if (!EMAIL_RE.test(t)) return 'That email looks off. Check the @ and the domain.';
                return '';
            }
        },
        {
            name: 'topic',
            validate: (v) =>
                v.trim().length === 0 ? 'A short label is fine. Even one word.' : ''
        },
        {
            name: 'message',
            validate: (v) =>
                v.trim().length === 0
                    ? "A sentence or two about what you're working on."
                    : ''
        }
    ];

    fields.forEach((f) => {
        const input = form.querySelector(`[name="${f.name}"]`);
        if (!input) return;
        const fieldEl = input.closest('.pec-contact-field');
        const errorEl = fieldEl ? fieldEl.querySelector('.pec-contact-error') : null;
        if (!fieldEl || !errorEl) return;

        let touched = false;

        f.run = function applyValidity() {
            const msg = f.validate(input.value);
            if (msg) {
                fieldEl.classList.add('is-invalid');
                input.setAttribute('aria-invalid', 'true');
                errorEl.textContent = msg;
                return false;
            }
            fieldEl.classList.remove('is-invalid');
            input.setAttribute('aria-invalid', 'false');
            errorEl.textContent = '';
            return true;
        };

        input.addEventListener('blur', () => {
            touched = true;
            f.run();
        });
        input.addEventListener('input', () => {
            if (touched) f.run();
        });

        f.inputEl = input;
    });

    form.addEventListener('submit', async (e) => {
        e.preventDefault();

        const honey = form.querySelector('input[name="_honey"]');
        if (honey && honey.value) return;

        let firstInvalid = null;
        let allValid = true;
        fields.forEach((f) => {
            if (!f.run) return;
            const ok = f.run();
            if (!ok) {
                allValid = false;
                if (!firstInvalid) firstInvalid = f.inputEl;
            }
        });

        if (!allValid) {
            if (firstInvalid) firstInvalid.focus();
            status.classList.remove('is-error');
            status.textContent = '';
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
            if (payload.email) payload.replyto = payload.email;

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
            success.scrollIntoView({ behavior: 'smooth', block: 'center' });
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

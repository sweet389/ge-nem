/* ---------- Gerar simulado ---------- */
function setupGeneratorForm() {
    const form = document.querySelector('#generator-form');
    const help = document.querySelector('#distribution-help');
    const totalEl = document.querySelector('#total-questions');
    const totalLabel = document.querySelector('#total-label');

    function update() {
        const day = form.querySelector('input[name="dia"]:checked')?.value;
        const mode = form.querySelector('input[name="modo"]:checked')?.value;
        const stats = mode === 'estatisticas';

        // mostra só o que pertence ao dia escolhido e desativa o resto (input hidden ainda é enviado no POST)
        form.querySelectorAll('[data-day]').forEach(block => {
            const active = block.dataset.day === day;
            block.hidden = !active;
            block.querySelectorAll('input').forEach(i => i.disabled = !active);
        });

        help.textContent = stats
            ? 'Defina o máximo de questões que o sistema pode selecionar por matéria.'
            : 'Defina exatamente quantas questões devem aparecer de cada matéria.';
        form.querySelectorAll('.unit').forEach(u => u.textContent = stats ? '(máx.)' : '(qtd.)');
        totalLabel.textContent = stats ? 'Total (até)' : 'Total';

        let total = 0;
        form.querySelectorAll('.subject-inputs:not([hidden]) input[type="number"]').forEach(i => {
            const max = Number(i.max) || 45;
            const v = Math.min(Math.max(parseInt(i.value, 10) || 0, 0), max);
            total += v;
        });
        totalEl.textContent = total;
        form.querySelector('#generate-btn').disabled = total === 0;
    }

    form.addEventListener('change', update);
    form.addEventListener('input', update);
    update();
}

/* ---------- Simulado ---------- */
function setupExam() {
    const form = document.querySelector('#exam-form');
    const panels = [...document.querySelectorAll('[data-question-panel]')];
    const buttons = [...document.querySelectorAll('.question-number')];
    const counter = document.querySelector('#question-counter');
    const progress = document.querySelector('#question-progress');
    const previous = document.querySelector('#previous-question');
    const next = document.querySelector('#next-question');
    const finish = document.querySelector('#finish-exam');
    const timer = document.querySelector('#timer');
    const elapsedInput = document.querySelector('#elapsed');

    let current = 0;
    let submitting = false;
    const startedAt = Date.now();

    function markAnswered() {
        panels.forEach((panel, index) => {
            buttons[index].classList.toggle('answered', !!panel.querySelector('input[type="radio"]:checked'));
        });
    }

    function show(index) {
        current = Math.max(0, Math.min(index, panels.length - 1));
        panels.forEach((p, i) => p.classList.toggle('hidden', i !== current));
        buttons.forEach((b, i) => b.classList.toggle('active', i === current));
        counter.textContent = `${current + 1} / ${panels.length}`;
        progress.style.width = `${((current + 1) / panels.length) * 100}%`;
        previous.disabled = current === 0;
        next.classList.toggle('hidden', current === panels.length - 1);
        finish.classList.toggle('hidden', current !== panels.length - 1);
        window.scrollTo({ top: 0, behavior: 'smooth' });
    }

    function tick() {
        const s = Math.floor((Date.now() - startedAt) / 1000);
        const h = Math.floor(s / 3600), m = Math.floor((s % 3600) / 60), sec = s % 60;
        const mm = String(m).padStart(2, '0'), ss = String(sec).padStart(2, '0');
        timer.textContent = h ? `${h}:${mm}:${ss}` : `${mm}:${ss}`;
        elapsedInput.value = s;
    }

    buttons.forEach((button, index) => button.addEventListener('click', () => show(index)));
    form.addEventListener('change', markAnswered);
    previous.addEventListener('click', () => show(current - 1));
    next.addEventListener('click', () => show(current + 1));

    /* atalhos: ← → navegam, A–E marcam a alternativa */
    document.addEventListener('keydown', e => {
        if (e.target.matches('input[type="number"], textarea, select') || e.ctrlKey || e.metaKey || e.altKey) return;
        if (e.key === 'ArrowRight') show(current + 1);
        else if (e.key === 'ArrowLeft') show(current - 1);
        else if (/^[a-eA-E]$/.test(e.key)) {
            const input = panels[current].querySelector(`input[value="${e.key.toUpperCase()}"]`);
            if (input) { input.checked = true; markAnswered(); }
        }
    });

    form.addEventListener('submit', e => {
        const blank = panels.filter(p => !p.querySelector('input:checked')).length;
        if (blank && !confirm(`Você deixou ${blank} questão(ões) em branco. Finalizar mesmo assim?`)) {
            e.preventDefault();
            return;
        }
        submitting = true;
    });

    window.addEventListener('beforeunload', e => {
        if (!submitting && form.querySelector('input:checked')) { e.preventDefault(); e.returnValue = ''; }
    });

    markAnswered();
    show(0);
    tick();
    setInterval(tick, 1000);
}

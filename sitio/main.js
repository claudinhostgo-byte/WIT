// W-IT · comportamiento del sitio (sin dependencias)
(() => {
  const $ = (sel, root = document) => root.querySelector(sel);
  const $$ = (sel, root = document) => [...root.querySelectorAll(sel)];
  const reduceMotion = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const desktop = matchMedia('(min-width: 1241px)');
  const root = (document.querySelector('link[rel="stylesheet"]').getAttribute('href') || '').replace('styles.css', '');

  // ---------- Header: transparente sobre el hero, sólido al hacer scroll
  const header = $('#header');
  const fixedSolid = header.classList.contains('is-solid-page');
  const onScroll = () => { if (!fixedSolid) header.classList.toggle('is-solid', window.scrollY > 40); };
  onScroll();
  window.addEventListener('scroll', onScroll, { passive: true });

  // ---------- Mega-menús (click, teclado y hover en escritorio)
  const megaButtons = $$('.nav-link[aria-controls^="mega-"]');
  const closeMegas = except => {
    megaButtons.forEach(b => { if (b !== except) b.setAttribute('aria-expanded', 'false'); });
    header.classList.toggle('mega-open', megaButtons.some(b => b.getAttribute('aria-expanded') === 'true') && desktop.matches);
  };
  const openMega = (btn, open) => {
    btn.setAttribute('aria-expanded', String(open));
    closeMegas(btn);
  };
  megaButtons.forEach(btn => {
    const item = btn.parentElement;
    let t;
    btn.addEventListener('click', () => openMega(btn, btn.getAttribute('aria-expanded') !== 'true'));
    item.addEventListener('mouseenter', () => { if (!desktop.matches) return; clearTimeout(t); openMega(btn, true); });
    item.addEventListener('mouseleave', () => { if (!desktop.matches) return; t = setTimeout(() => openMega(btn, false), 160); });
  });
  document.addEventListener('click', e => { if (desktop.matches && !header.contains(e.target)) closeMegas(); });
  header.addEventListener('focusout', e => { if (desktop.matches && !header.contains(e.relatedTarget)) closeMegas(); });

  // ---------- Menú móvil (cajón a pantalla completa)
  const navToggle = $('.nav-toggle');
  const setDrawer = open => {
    header.classList.toggle('nav-open', open);
    document.body.classList.toggle('nav-locked', open);
    navToggle.setAttribute('aria-expanded', String(open));
    navToggle.setAttribute('aria-label', open ? 'Cerrar menú' : 'Abrir menú');
    if (!open) closeMegas();
  };
  navToggle.addEventListener('click', () => setDrawer(!header.classList.contains('nav-open')));
  desktop.addEventListener('change', () => { setDrawer(false); closeMegas(); });

  document.addEventListener('keydown', e => {
    if (e.key !== 'Escape') return;
    const open = megaButtons.find(b => b.getAttribute('aria-expanded') === 'true');
    if (open) { closeMegas(); open.focus(); }
    else if (header.classList.contains('nav-open')) { setDrawer(false); navToggle.focus(); }
    else if (!agentePanel.hidden) { setAgente(false); fab.focus(); }
  });

  // ---------- Marquee de logos: duplica cada fila para el loop continuo
  if (!reduceMotion) {
    $$('#marquee .marquee').forEach(list => {
      [...list.children].forEach(li => {
        const c = li.cloneNode(true);
        c.setAttribute('aria-hidden', 'true');
        $('img', c).alt = '';
        list.appendChild(c);
      });
    });
  }

  // ---------- Hero: desenfoque del fondo mientras el mouse se mueve
  const hero = $('#hero');
  // Se filtra por tipo de puntero (no por "hover: hover"): en notebooks con pantalla táctil
  // esa media query responde "none" aunque se use mouse, y el efecto no se activaba.
  if (hero && !reduceMotion) {
    let still;
    hero.addEventListener('pointermove', e => {
      if (e.pointerType !== 'mouse') return;
      hero.classList.add('is-moving');
      clearTimeout(still);
      still = setTimeout(() => hero.classList.remove('is-moving'), 220);
    }, { passive: true });
    hero.addEventListener('pointerleave', () => { clearTimeout(still); hero.classList.remove('is-moving'); });
  }

  // ---------- Consola del agente (hero): escenarios ilustrativos
  const consoleEl = $('#console');
  if (consoleEl) {
    const icon = slug => `<img src="${root}assets/ms/${slug}.svg" alt="" width="24" height="24">`;
    const shield = '<svg class="step-ico" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M12 3l8 3v6c0 4.5-3.4 8.3-8 9-4.6-.7-8-4.5-8-9V6z"/><path d="M8.5 12l2.5 2.5 4.5-5"/></svg>';
    const escenarios = [
      { tab: 'Servicio', prompt: '¿Qué casos críticos vencen hoy?',
        steps: [[icon('d365-customer-service'), 'Consultando casos abiertos en Dynamics 365 Customer Service', '🔎'],
                [icon('dataverse'), 'Cruzando historial del cliente en Dataverse', '🗂️'],
                [shield, 'Aplicando permisos del usuario y política de datos', '🔐']],
        result: 'Casos priorizados por vencimiento de SLA, con borradores de respuesta listos para revisión humana.' },
      { tab: 'Finanzas', prompt: 'Prepara el cierre de septiembre',
        steps: [[icon('d365-business-central'), 'Revisando asientos pendientes en Business Central', '📒'],
                [icon('power-automate'), 'Conciliando cartolas bancarias con Power Automate', '🏦'],
                [shield, 'Registrando cada acción para auditoría', '🧾']],
        result: 'Partidas por conciliar identificadas e informe enviado al controller para aprobación.' },
      { tab: 'Ventas', prompt: '¿Qué oportunidades debo priorizar esta semana?',
        steps: [[icon('d365-sales'), 'Analizando el pipeline en Dynamics 365 Sales', '📈'],
                [icon('m365-copilot'), 'Resumiendo correos y reuniones recientes con Copilot', '✉️'],
                [shield, 'Usando solo datos que el vendedor puede ver', '🔐']],
        result: 'Oportunidades ordenadas por probabilidad, con el siguiente paso sugerido para cada una.' },
    ];
    // Canales: misma conversación, distinto look & feel
    const canales = {
      web: { sub: 'en producción', ph: 'Pregúntale al agente' },
      teams: { sub: 'Disponible', ph: 'Escribe un mensaje' },
      whatsapp: { sub: 'en línea', ph: 'Mensaje' },
      gchat: { sub: 'Activo · Espacio Operaciones', ph: 'Mensaje para Agente W-IT' },
    };
    const setCanal = c => {
      consoleEl.dataset.canal = c;
      $('[data-c="sub"]', consoleEl).textContent = canales[c].sub;
      $('[data-c="placeholder"]', consoleEl).textContent = canales[c].ph;
      $$('.canales button').forEach(b => b.setAttribute('aria-pressed', String(b.dataset.canal === c)));
    };
    $$('.canales button').forEach(b => b.addEventListener('click', () => { setCanal(b.dataset.canal); $('.canales').classList.add('used'); }));
    const bodyEl = $('.console-body', consoleEl);
    const scrollDown = () => { bodyEl.scrollTop = bodyEl.scrollHeight; };
    const hora = new Date().toLocaleTimeString('es-CL', { hour: '2-digit', minute: '2-digit', hour12: false });
    $$('[data-c="time"]', consoleEl).forEach(t => { t.textContent = hora; });
    setCanal('web');
    const tabs = $('.console-tabs', consoleEl);
    const promptEl = $('[data-c="prompt"]', consoleEl);
    const stepsEl = $('[data-c="steps"]', consoleEl);
    const resultEl = $('[data-c="result"]', consoleEl);
    let idx = 0, run = 0;
    escenarios.forEach((e, i) => {
      const b = document.createElement('button');
      b.type = 'button'; b.role = 'tab'; b.textContent = e.tab;
      b.addEventListener('click', () => play(i));
      tabs.appendChild(b);
    });
    const wait = (ms, id) => new Promise((res, rej) => setTimeout(() => (id === run ? res() : rej()), ms));
    const render = (e, full) => {
      stepsEl.innerHTML = e.steps.map(([ico, txt, emo]) => `<li class="${full ? 'in done' : ''}">${ico}<span class="emo" aria-hidden="true">${emo}</span><span>${txt}</span><span class="st" aria-hidden="true"></span></li>`).join('');
      resultEl.innerHTML = `<strong>Resultado</strong><span>${e.result}</span><span class="result-actions"><button type="button">Ver detalle</button><button type="button">Derivar a una persona</button></span>`;
      resultEl.classList.toggle('in', full);
      promptEl.textContent = full ? e.prompt : '';
    };
    async function play(i) {
      const id = ++run; idx = i;
      const e = escenarios[i];
      $$('button', tabs).forEach((b, j) => b.setAttribute('aria-selected', String(j === i)));
      bodyEl.scrollTop = 0;
      if (reduceMotion) { render(e, true); return; }
      render(e, false);
      try {
        promptEl.classList.add('typing');
        for (const ch of e.prompt) { promptEl.textContent += ch; await wait(38, id); }
        promptEl.classList.remove('typing');
        const lis = $$('li', stepsEl);
        consoleEl.classList.add('busy');
        for (const li of lis) { await wait(350, id); li.classList.add('in'); scrollDown(); await wait(1100, id); li.classList.add('done'); }
        await wait(500, id); resultEl.classList.add('in'); scrollDown();
        consoleEl.classList.remove('busy');
        await wait(4200, id);
        play((idx + 1) % escenarios.length);
      } catch (_) { consoleEl.classList.remove('busy'); /* escenario interrumpido por otro */ }
    }
    // Arranca cuando la consola es visible
    const io = new IntersectionObserver(entries => {
      if (entries[0].isIntersecting) { io.disconnect(); play(0); }
    });
    io.observe(consoleEl);
  }

  // ---------- FAQ: acordeón con una pregunta abierta a la vez
  const faqButtons = $$('#faq button');
  faqButtons.forEach(btn => btn.addEventListener('click', () => {
    const willOpen = btn.getAttribute('aria-expanded') !== 'true';
    faqButtons.forEach(b => {
      const open = b === btn && willOpen;
      b.setAttribute('aria-expanded', String(open));
      document.getElementById(b.getAttribute('aria-controls')).hidden = !open;
    });
  }));

  // ---------- Filtros de casos de éxito
  const filtros = $('#filtros');
  if (filtros) {
    const sel = { industria: '*', solucion: '*' };
    const cards = $$('#casos-grid .caso-card');
    const empty = $('.filters-empty');
    filtros.addEventListener('click', e => {
      const b = e.target.closest('button[data-filter]');
      if (!b) return;
      sel[b.dataset.filter] = b.dataset.value;
      $$(`button[data-filter="${b.dataset.filter}"]`, filtros).forEach(x => x.classList.toggle('is-on', x === b));
      let n = 0;
      cards.forEach(c => {
        const ok = (sel.industria === '*' || c.dataset.industria === sel.industria) && (sel.solucion === '*' || c.dataset.solucion === sel.solucion);
        c.hidden = !ok; if (ok) n++;
      });
      empty.hidden = n > 0;
    });
  }

  // ---------- Formulario de contacto (demostración: no envía datos)
  const form = $('#form-contacto');
  if (form) {
    form.addEventListener('submit', e => {
      e.preventDefault();
      if (!form.reportValidity()) return;
      $('.form-msg', form).hidden = false;
      console.info('[demo] Contexto oculto que viajaría al CRM:', Object.fromEntries([...form.querySelectorAll('input[type=hidden]')].map(i => [i.name, i.value])));
    });
  }

  // ---------- "Señales de que lo necesitas": el foco recorre la lista cada 3,5 s; se detiene con el mouse encima
  $$('.senales').forEach(sec => {
    const items = $$('.sen-item', sec);
    if (items.length < 2) return;
    const MS = 3500; // mismo intervalo que la barra en styles.css
    let i = 0, t, hold = false, visible = false;
    const activate = n => {
      i = (n + items.length) % items.length;
      items.forEach((el, k) => el.classList.toggle('is-on', k === i));
      const on = items[i]; on.classList.remove('is-on'); void on.offsetWidth; on.classList.add('is-on'); // reinicia la barra
    };
    const loop = () => {
      clearTimeout(t);
      t = setTimeout(() => { if (visible && !hold && document.visibilityState === 'visible') activate(i + 1); loop(); }, MS);
    };
    const resume = () => { hold = false; activate(i); loop(); };
    items.forEach((el, k) => el.addEventListener('pointerenter', () => { hold = true; if (k !== i) activate(k); }));
    sec.addEventListener('pointerenter', () => { hold = true; });
    sec.addEventListener('pointerleave', resume);
    document.addEventListener('visibilitychange', () => { if (document.visibilityState === 'visible') resume(); });
    new IntersectionObserver(([e]) => { const was = visible; visible = e.isIntersecting; if (visible && !was) resume(); }, { threshold: .3 }).observe(sec);
    if (!reduceMotion) loop();
  });

  // ---------- Metodología: línea de tiempo interactiva (una fase abierta a la vez; flechas del teclado entre fases)
  $$('[data-metodo]').forEach(m => {
    const rail = $('.mt-rail', m), steps = $$('.mt-step', m), btns = $$('.mt-btn', m), panels = $$('.mt-panel', m), count = $('.mt-count', m);
    if (btns.length < 2) return;
    let i = Math.max(0, btns.findIndex(b => b.getAttribute('aria-expanded') === 'true'));
    const show = (n, focus) => {
      i = (n + btns.length) % btns.length;
      btns.forEach((b, k) => { b.setAttribute('aria-expanded', String(k === i)); b.classList.toggle('is-on', k === i); b.classList.toggle('is-done', k < i); });
      steps.forEach((s, k) => { s.classList.toggle('is-on', k === i); s.classList.toggle('is-done', k < i); });
      panels.forEach((p, k) => { p.hidden = k !== i; });
      rail.style.setProperty('--i', i);
      if (count) count.textContent = `${i + 1} / ${btns.length}`;
      if (focus) btns[i].focus();
    };
    btns.forEach((b, k) => b.addEventListener('click', () => show(k)));
    $$('[data-mt]', m).forEach(b => b.addEventListener('click', () => show(i + (b.dataset.mt === 'next' ? 1 : -1))));
    rail.addEventListener('keydown', e => {
      if (!e.target.closest('.mt-btn')) return;
      const to = { ArrowRight: i + 1, ArrowDown: i + 1, ArrowLeft: i - 1, ArrowUp: i - 1, Home: 0, End: btns.length - 1 }[e.key];
      if (to !== undefined) { e.preventDefault(); show(to, true); }
    });
    show(i);
  });

  // ---------- Autodiagnóstico IA: 5 preguntas, resultado con nivel, plazo y próximo paso
  const diag = $('#diag-ia');
  if (diag) {
    const D = JSON.parse($('#diag-ia-data').textContent);
    const steps = $$('.diag-steps li', diag);
    const marca = n => steps.forEach((li, k) => { li.classList.toggle('is-done', k < n); li.classList.toggle('is-on', k === n); });
    const stage = $('.diag-step', diag);
    const esc = t => t.replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
    let resp = [];

    const pregunta = n => {
      const p = D.preguntas[n];
      marca(n);
      stage.innerHTML = `<span class="eyebrow">Pregunta ${n + 1} de ${D.preguntas.length}</span>
        <h2 class="h2" tabindex="-1">${esc(p.q)}</h2>
        <div class="wizard-opts diag-opts">${p.opts.map((o, k) => `<button type="button" data-k="${k}"${resp[n] === o ? ' class="is-sel"' : ''}><span class="diag-key">${'ABCD'[k]}</span>${esc(o.t)}</button>`).join('')}</div>
        ${n ? '<button type="button" class="diag-back">← Anterior</button>' : ''}`;
      $$('.wizard-opts button', stage).forEach(b => b.addEventListener('click', () => {
        resp[n] = p.opts[+b.dataset.k];
        n + 1 < D.preguntas.length ? pregunta(n + 1) : resultado();
      }));
      const back = $('.diag-back', stage);
      if (back) back.addEventListener('click', () => pregunta(n - 1));
      if (n) $('h2', stage).focus();
    };

    const resultado = () => {
      const pts = resp.reduce((a, o) => a + o.pts, 0);
      const [min, max] = resp.slice(1).reduce(([a, b], o) => [a + o.sem[0], b + o.sem[1]], resp[0].base);
      const nivel = D.niveles.find(([m]) => pts >= m);
      const brechas = resp.filter(o => o.brecha).map(o => o.brecha);
      const paso = D.rutas[resp[0].ruta];
      marca(D.preguntas.length);
      stage.innerHTML = `<span class="eyebrow">Tu resultado</span>
        <h2 class="h2" tabindex="-1">${esc(nivel[1])}</h2>
        <p class="lead">${esc(nivel[2])}</p>
        <div class="diag-kpis">
          <div><span>Plazo estimado a un primer caso en producción</span><strong>${min === max ? min : `${min} a ${max}`} semanas</strong></div>
          <div><span>Preparación</span><strong>${pts} de 10</strong></div>
        </div>
        ${brechas.length ? `<div><h3 class="diag-sub">Qué resolver primero</h3><ul class="diag-list">${brechas.slice(0, 3).map(t => `<li>${esc(t)}</li>`).join('')}</ul></div>` : ''}
        <div><h3 class="diag-sub">Próximo paso sugerido</h3><p>${esc(paso)} Algunas de estas actividades pueden tener <a href="${diag.dataset.cofin}">cofinanciamiento de Microsoft</a>.</p></div>
        <div class="diag-cta">
          <p><strong>¿Conversamos?</strong> Un especialista puede revisar estos resultados contigo y resolver tus dudas.</p>
          <div class="btn-row"><a class="btn btn-primary" href="${diag.dataset.contacto}">Conversemos</a><button type="button" class="btn btn-outline diag-reset">Volver a empezar</button></div>
        </div>`;
      try {
        sessionStorage.setItem('wit-diag', JSON.stringify({ herramienta: 'Autodiagnóstico de madurez en IA y agentes',
          resultado: `${nivel[1]} (${pts}/10), plazo estimado ${min} a ${max} semanas`,
          detalle: resp.map((o, k) => `${D.preguntas[k].q} ${o.t}`).join('\n') }));
      } catch (e) { /* sin almacenamiento: el formulario va sin contexto */ }
      $('.diag-reset', stage).addEventListener('click', () => { resp = []; pregunta(0); });
      $('h2', stage).focus();
    };

    pregunta(0);
  }

  // ---------- ¿Business Central o Finance?: perfil → preguntas del área → recomendación
  const erp = $('#diag-erp');
  if (erp) {
    const D = JSON.parse($('#diag-erp-data').textContent);
    const stepsEl = $('.diag-steps', erp);
    const stage = $('.diag-step', erp);
    const esc = t => t.replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
    let seq, resp;

    const armar = rol => {
      seq = [D.perfil, ...D.comunes, ...(rol ? D.roles[rol] : [{ tag: 'Tu área' }, { tag: 'Tu área' }, { tag: 'Tu área' }]), D.final];
      stepsEl.innerHTML = seq.map(q => `<li>${esc(q.tag)}</li>`).join('');
    };
    const marca = n => $$('li', stepsEl).forEach((li, k) => { li.classList.toggle('is-done', k < n); li.classList.toggle('is-on', k === n); });

    const pregunta = n => {
      const p = seq[n];
      marca(n);
      stage.innerHTML = `<span class="eyebrow">Pregunta ${n + 1} de ${seq.length}</span>
        <h2 class="h2" tabindex="-1">${esc(p.q)}</h2>
        <div class="wizard-opts diag-opts">${p.opts.map((o, k) => `<button type="button" data-k="${k}"${resp[n] === o ? ' class="is-sel"' : ''}><span class="diag-key">${'ABCD'[k]}</span>${esc(o.t)}</button>`).join('')}</div>
        ${n ? '<button type="button" class="diag-back">← Anterior</button>' : ''}`;
      $$('.wizard-opts button', stage).forEach(b => b.addEventListener('click', () => {
        const o = p.opts[+b.dataset.k];
        if (n === 0 && resp[0] !== o) { resp = [o]; armar(o.rol); } else resp[n] = o;
        n + 1 < seq.length ? pregunta(n + 1) : resultado();
      }));
      const back = $('.diag-back', stage);
      if (back) back.addEventListener('click', () => pregunta(n - 1));
      if (n) $('h2', stage).focus();
    };

    const resultado = () => {
      const pts = resp.reduce((a, o) => a + (o.v || 0), 0);
      const key = pts <= -3 ? 'bc' : pts >= 3 ? 'fin' : 'ambos';
      const prod = D.productos[key];
      const razones = resp.filter(o => o.por && (key === 'ambos' || (key === 'bc' ? o.v < 0 : o.v > 0)))
        .sort((a, b) => Math.abs(b.v) - Math.abs(a.v)).slice(0, 3).map(o => o.por);
      const scm = key !== 'bc' && resp.some(o => o.scm);
      const urg = resp[resp.length - 1].meses;
      const [m0, m1] = prod.meses;
      const calce = !urg ? '' : m1 <= urg ? 'Tu fecha objetivo calza con el plazo típico.'
        : m0 > urg ? 'Tu fecha objetivo es más corta que el plazo típico: conviene partir por etapas y priorizar lo esencial.'
        : 'Tu fecha objetivo es exigente: se puede lograr con un alcance acotado en la primera etapa.';
      marca(seq.length);
      stage.innerHTML = `<span class="eyebrow">Nuestra recomendación</span>
        <h2 class="h2" tabindex="-1">${esc(prod.nombre)}</h2>
        <p class="lead">${esc(prod.texto)}</p>
        <div class="diag-kpis">
          <div><span>Plazo típico de implementación</span><strong>${m0} a ${m1} meses</strong></div>
          <div><span>Perfil</span><strong class="diag-kpi-txt">${esc(resp[0].t)}</strong></div>
        </div>
        ${calce ? `<p class="diag-note">${esc(calce)}</p>` : ''}
        ${razones.length ? `<div><h3 class="diag-sub">${key === 'ambos' ? 'Lo que pesa en tu caso' : 'Por qué'}</h3><ul class="diag-list">${razones.map(t => `<li>${esc(t)}</li>`).join('')}</ul></div>` : ''}
        ${scm ? '<p class="diag-note">Por tu operación, considera sumar <strong>Dynamics 365 Supply Chain Management</strong>.</p>' : ''}
        <div><h3 class="diag-sub">Próximo paso sugerido</h3><p>Una demo sobre tus procesos reales para confirmar la elección. Conoce más en <a href="${erp.dataset.sol}">Finanzas y operaciones</a>.</p></div>
        <div class="diag-cta">
          <p><strong>¿Conversamos?</strong> Un especialista puede revisar estos resultados contigo y resolver tus dudas.</p>
          <div class="btn-row"><a class="btn btn-primary" href="${erp.dataset.contacto}">Conversemos</a><button type="button" class="btn btn-outline diag-reset">Volver a empezar</button></div>
        </div>`;
      try {
        sessionStorage.setItem('wit-diag', JSON.stringify({ herramienta: '¿Business Central o Finance?',
          resultado: `${prod.nombre}, plazo típico ${m0} a ${m1} meses${scm ? ', considerar Supply Chain Management' : ''}`,
          detalle: resp.map((o, k) => `${seq[k].q} ${o.t}`).join('\n') }));
      } catch (e) { /* sin almacenamiento: el formulario va sin contexto */ }
      $('.diag-reset', stage).addEventListener('click', () => { resp = []; armar(); pregunta(0); });
      $('h2', stage).focus();
    };

    resp = []; armar(); pregunta(0);
  }

  // ---------- Autodiagnóstico de atención y ventas: puntos para Sales (s), Customer Service (cs) y Contact Center (cc)
  const crm = $('#diag-crm');
  if (crm) {
    const D = JSON.parse($('#diag-crm-data').textContent);
    const steps = $$('.diag-steps li', crm);
    const stage = $('.diag-step', crm);
    const esc = t => t.replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
    const marca = n => steps.forEach((li, k) => { li.classList.toggle('is-done', k < n); li.classList.toggle('is-on', k === n); });
    const KEYS = ['s', 'cs', 'cc'];
    let resp = []; // por pregunta: arreglo de opciones elegidas

    const pregunta = n => {
      const p = D.preguntas[n];
      const sel = resp[n] || [];
      marca(n);
      stage.innerHTML = `<span class="eyebrow">Pregunta ${n + 1} de ${D.preguntas.length}${p.multi ? ' · Puedes marcar varias' : ''}</span>
        <h2 class="h2" tabindex="-1">${esc(p.q)}</h2>
        <div class="wizard-opts diag-opts">${p.opts.map((o, k) => `<button type="button" data-k="${k}"${p.multi ? ` aria-pressed="${sel.includes(o)}"` : ''}${sel.includes(o) ? ' class="is-sel"' : ''}><span class="diag-key">${'ABCDEF'[k]}</span>${esc(o.t)}</button>`).join('')}</div>
        <div class="diag-nav">${n ? '<button type="button" class="diag-back">← Anterior</button>' : '<span></span>'}${p.multi ? `<button type="button" class="btn btn-primary diag-next"${sel.length ? '' : ' disabled'}>Continuar</button>` : ''}</div>`;
      const sigue = () => (n + 1 < D.preguntas.length ? pregunta(n + 1) : resultado());
      $$('.wizard-opts button', stage).forEach(b => b.addEventListener('click', () => {
        const o = p.opts[+b.dataset.k];
        if (!p.multi) { resp[n] = [o]; sigue(); return; }
        const cur = resp[n] || [];
        resp[n] = cur.includes(o) ? cur.filter(x => x !== o) : [...cur, o];
        b.classList.toggle('is-sel'); b.setAttribute('aria-pressed', String(resp[n].includes(o)));
        $('.diag-next', stage).disabled = !resp[n].length;
      }));
      const next = $('.diag-next', stage);
      if (next) next.addEventListener('click', sigue);
      const back = $('.diag-back', stage);
      if (back) back.addEventListener('click', () => pregunta(n - 1));
      if (n) $('h2', stage).focus();
    };

    const resultado = () => {
      const pts = { s: 0, cs: 0, cc: 0 };
      const razones = { s: [], cs: [], cc: [] };
      const suma = o => KEYS.forEach(k => { if (o[k]) { pts[k] += o[k]; if (o[`por_${k}`]) razones[k].push([o[k], o[`por_${k}`]]); } });
      D.preguntas.forEach((p, n) => {
        (resp[n] || []).forEach(suma);
        if (p.extra && (resp[n] || []).length >= p.extra.min) suma(p.extra);
      });
      const orden = [...KEYS].sort((a, b) => pts[b] - pts[a]);
      const top = orden[0];
      const max = pts[top];
      const extras = orden.slice(1).filter(k => pts[k] >= 3 && pts[k] >= max * 0.6);
      const prod = D.productos[top];
      const por = razones[top].sort((a, b) => b[0] - a[0]).slice(0, 3).map(x => x[1]);
      const canales = (resp[1] || []).map(o => o.t);
      const ia = D.ia[String((resp[6] || [{}])[0].ia || 0)];
      const link = k => `<a href="${root}${D.productos[k].sol}">${esc(D.productos[k].sol_n)}</a>`;
      marca(D.preguntas.length);
      stage.innerHTML = `<span class="eyebrow">Por dónde partir</span>
        <h2 class="h2" tabindex="-1">${esc(prod.nombre)}</h2>
        <p class="lead">${esc(prod.texto)}</p>
        <div class="diag-kpis">
          <div><span>Canales a integrar</span><strong class="diag-kpi-txt">${canales.length ? esc(canales.join(', ')) : 'Por definir'}</strong></div>
          <div><span>Volumen mensual</span><strong class="diag-kpi-txt">${esc(((resp[2] || [{}])[0].t) || 'Por definir')}</strong></div>
        </div>
        ${por.length ? `<div><h3 class="diag-sub">Por qué</h3><ul class="diag-list">${por.map(t => `<li>${esc(t)}</li>`).join('')}</ul></div>` : ''}
        ${extras.length ? `<div><h3 class="diag-sub">También considera</h3><ul class="diag-list">${extras.map(k => `<li><strong>${esc(D.productos[k].nombre)}</strong>: ${esc(D.productos[k].texto)}</li>`).join('')}</ul><p class="diag-note">Sales, Customer Service y Contact Center comparten la misma base de clientes en Dataverse, así que puedes partir por una y sumar las otras sin migrar datos.</p></div>` : ''}
        ${ia ? `<div><h3 class="diag-sub">Cómo sumar IA</h3><p>${esc(ia)}</p></div>` : ''}
        <div><h3 class="diag-sub">Próximo paso sugerido</h3><p>Una demo con tus canales y procesos reales para confirmar el punto de partida. Conoce más en ${[top, ...extras].map(link).filter((v, i, a) => a.indexOf(v) === i).join(' y ')}.</p></div>
        <div class="diag-cta">
          <p><strong>¿Conversamos?</strong> Un especialista puede revisar estos resultados contigo y resolver tus dudas.</p>
          <div class="btn-row"><a class="btn btn-primary" href="${crm.dataset.contacto}">Conversemos</a><button type="button" class="btn btn-outline diag-reset">Volver a empezar</button></div>
        </div>`;
      try {
        sessionStorage.setItem('wit-diag', JSON.stringify({ herramienta: 'Autodiagnóstico de atención y ventas',
          resultado: `${prod.nombre}${extras.length ? ` + ${extras.map(k => D.productos[k].nombre).join(' + ')}` : ''}`,
          interno: `puntos: Sales ${pts.s}, Customer Service ${pts.cs}, Contact Center ${pts.cc}`,
          detalle: D.preguntas.map((p, n) => `${p.q} ${(resp[n] || []).map(o => o.t).join(', ')}`).join('\n') }));
      } catch (e) { /* sin almacenamiento: el formulario va sin contexto */ }
      $('.diag-reset', stage).addEventListener('click', () => { resp = []; pregunta(0); });
      $('h2', stage).focus();
    };

    pregunta(0);
  }

  // ---------- Enlaces externos sin salir del sitio
  // Mapas: ventana modal con Google Maps embebido (se carga solo al hacer clic).
  // Resto de sitios externos (Microsoft, WITEDUCA, etc.): no permiten mostrarse dentro de otra página,
  // así que se abren en una ventana emergente del navegador; si el navegador la bloquea, en una pestaña nueva.
  const modal = document.createElement('dialog');
  modal.className = 'wit-modal';
  modal.innerHTML = `<div class="wit-modal-head"><strong></strong><button type="button" class="wit-modal-close" aria-label="Cerrar">×</button></div>
    <div class="wit-modal-body"></div><div class="wit-modal-foot"></div>`;
  document.body.appendChild(modal);
  const cerrar = () => { modal.close(); $('.wit-modal-body', modal).innerHTML = ''; };
  $('.wit-modal-close', modal).addEventListener('click', cerrar);
  modal.addEventListener('click', e => { if (e.target === modal) cerrar(); });
  modal.addEventListener('close', () => { $('.wit-modal-body', modal).innerHTML = ''; });

  const ventana = url => {
    const w = Math.min(1180, screen.availWidth - 80), h = Math.min(820, screen.availHeight - 80);
    const x = Math.round(window.screenX + (window.outerWidth - w) / 2), y = Math.round(window.screenY + (window.outerHeight - h) / 2);
    return window.open(url, 'wit-externo', `popup=yes,width=${w},height=${h},left=${Math.max(0, x)},top=${Math.max(0, y)}`);
  };

  document.addEventListener('click', e => {
    const a = e.target.closest('a[href]');
    if (!a || e.defaultPrevented || e.button !== 0 || e.metaKey || e.ctrlKey || e.shiftKey || e.altKey) return;
    if (a.dataset.mapa) {
      e.preventDefault();
      $('.wit-modal-head strong', modal).textContent = a.dataset.mapaTitulo || 'Ubicación';
      $('.wit-modal-body', modal).innerHTML = `<iframe title="Mapa: ${a.dataset.mapa.replace(/"/g, '&quot;')}" loading="lazy" referrerpolicy="no-referrer-when-downgrade"
        src="https://www.google.com/maps?q=${encodeURIComponent(a.dataset.mapa)}&output=embed"></iframe>`;
      $('.wit-modal-foot', modal).innerHTML = `<span>${a.dataset.mapa.replace(/</g, '&lt;')}</span><a class="link-strong" href="${a.href}" data-externo>Abrir en Google Maps ↗</a>`;
      modal.showModal();
      return;
    }
    const url = new URL(a.href, location.href);
    if (!/^https?:$/.test(url.protocol) || url.origin === location.origin) return;
    if (ventana(url.href)) e.preventDefault(); // bloqueada: sigue el target="_blank" del enlace
  });

  // ---------- Origen del contacto (para el CRM): desde qué página y botón se llegó, diagnóstico y UTM
  const store = {
    get: k => { try { return JSON.parse(sessionStorage.getItem(k) || 'null'); } catch (e) { return null; } },
    set: (k, v) => { try { sessionStorage.setItem(k, JSON.stringify(v)); } catch (e) { /* sin almacenamiento */ } },
  };
  // UTM de la primera página de la visita
  const utm = [...new URLSearchParams(location.search)].filter(([k]) => k.startsWith('utm_'));
  if (utm.length && !store.get('wit-utm')) store.set('wit-utm', utm.map(([k, v]) => `${k}=${v}`).join('&'));
  // Último enlace hacia Contacto que se usó en el sitio
  document.addEventListener('click', e => {
    const a = e.target.closest('a[href]');
    if (!a || !/(^|\/)contacto\/?(#.*)?$/.test(new URL(a.href, location.href).pathname)) return;
    const sec = a.closest('section[id], section[aria-label], header, footer');
    store.set('wit-origen', {
      pagina: location.pathname,
      cta: `${a.textContent.trim().replace(/\s+/g, ' ').slice(0, 80)}${sec ? ` · ${sec.id || sec.getAttribute('aria-label') || sec.tagName.toLowerCase()}` : ''}`,
    });
  });
  // En Contacto: completa los campos ocultos
  if (form) {
    const set = (n, v) => { if (v) form.elements[n].value = v; };
    const origen = store.get('wit-origen');
    const ref = document.referrer && new URL(document.referrer).origin === location.origin ? new URL(document.referrer).pathname : '';
    set('origen_pagina', origen ? origen.pagina : ref || (document.referrer ? document.referrer : 'directo'));
    set('origen_cta', origen && origen.cta);
    const diag = store.get('wit-diag');
    if (diag) {
      set('diagnostico_herramienta', diag.herramienta);
      set('diagnostico_resultado', diag.interno ? `${diag.resultado} (${diag.interno})` : diag.resultado);
      set('diagnostico_detalle', diag.detalle);
      // La persona ve lo que ya respondió dentro de su mensaje: escribe arriba y bajo "--" va el autodiagnóstico
      const msg = form.elements.mensaje;
      if (!msg.value.trim()) {
        msg.value = ['', '', '--', `${diag.herramienta}`, `Resultado: ${diag.resultado}`, '',
          ...diag.detalle.split('\n').map(l => `· ${l}`)].join('\n');
        msg.rows = 10;
        msg.setSelectionRange(0, 0);
        msg.scrollTop = 0;
        $('.msg-ctx', form).hidden = false;
      }
    }
    set('utm', store.get('wit-utm'));
  }

  // ---------- Agente flotante
  const fab = $('.agente-fab');
  const agentePanel = $('#agente-panel');
  const setAgente = open => {
    agentePanel.hidden = !open;
    fab.setAttribute('aria-expanded', String(open));
    fab.setAttribute('aria-label', open ? 'Cerrar agente W-IT' : 'Abrir agente W-IT');
  };
  fab.addEventListener('click', () => { setAgente(agentePanel.hidden); fab.classList.add('used'); });

  $$('[data-open-agente]').forEach(a => a.addEventListener('click', e => {
    e.preventDefault();
    setAgente(true);
    $('button', agentePanel).focus();
  }));
})();

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
  if (hero && matchMedia('(hover: hover)').matches && !reduceMotion) {
    let still;
    hero.addEventListener('mousemove', () => {
      hero.classList.add('is-moving');
      clearTimeout(still);
      still = setTimeout(() => hero.classList.remove('is-moving'), 220);
    }, { passive: true });
    hero.addEventListener('mouseleave', () => { clearTimeout(still); hero.classList.remove('is-moving'); });
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

  // ---------- Cuenta regresiva Ley 21.719 (se oculta al vencer)
  const cd = $('#countdown');
  if (cd) {
    const target = new Date(cd.dataset.target).getTime();
    const pad = n => String(n).padStart(2, '0');
    const tick = () => {
      const diff = target - Date.now();
      if (diff <= 0) { cd.classList.add('is-expired'); return false; }
      $('[data-unit="d"]', cd).textContent = Math.floor(diff / 864e5);
      $('[data-unit="h"]', cd).textContent = pad(Math.floor(diff / 36e5) % 24);
      $('[data-unit="m"]', cd).textContent = pad(Math.floor(diff / 6e4) % 60);
      return true;
    };
    if (tick()) { const t = setInterval(() => { if (!tick()) clearInterval(t); }, 30000); }
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
    });
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

  // Sonido de los golpes en la pantalla (sintetizado con Web Audio; el navegador solo permite audio tras una interacción)
  let audio = null, audioOk = false;
  const enableAudio = () => { audioOk = true; };
  ['pointerdown', 'keydown', 'touchstart'].forEach(ev => document.addEventListener(ev, enableAudio, { once: true, passive: true }));
  const knock = t => {
    const ctx = audio || (audio = new (window.AudioContext || window.webkitAudioContext)());
    const at = ctx.currentTime + t;
    // golpe seco: seno grave que cae rápido + ráfaga corta de ruido (el "toc" en el vidrio)
    const osc = ctx.createOscillator(), g = ctx.createGain();
    osc.type = 'sine'; osc.frequency.setValueAtTime(320, at); osc.frequency.exponentialRampToValueAtTime(110, at + .07);
    g.gain.setValueAtTime(.0001, at); g.gain.exponentialRampToValueAtTime(.5, at + .004); g.gain.exponentialRampToValueAtTime(.0001, at + .11);
    osc.connect(g).connect(ctx.destination); osc.start(at); osc.stop(at + .12);
    const len = Math.floor(ctx.sampleRate * .03), buf = ctx.createBuffer(1, len, ctx.sampleRate), d = buf.getChannelData(0);
    for (let i = 0; i < len; i++) d[i] = (Math.random() * 2 - 1) * (1 - i / len);
    const n = ctx.createBufferSource(), f = ctx.createBiquadFilter(), ng = ctx.createGain();
    n.buffer = buf; f.type = 'bandpass'; f.frequency.value = 1800; f.Q.value = .8;
    ng.gain.setValueAtTime(.35, at); ng.gain.exponentialRampToValueAtTime(.0001, at + .03);
    n.connect(f).connect(ng).connect(ctx.destination); n.start(at);
  };
  const clipEl = $('.clip', fab);
  const onKnock = e => {
    if (e.animationName !== 'clip-knock' || !audioOk || fab.classList.contains('used') || document.visibilityState !== 'visible') return;
    [0.72, 1.17, 1.62].forEach(t => knock(t)); // sincronizado con los tres toques de la animación (8 %, 13 % y 18 % de 9 s)
  };
  if (clipEl) { clipEl.addEventListener('animationstart', onKnock); clipEl.addEventListener('animationiteration', onKnock); }
  $$('[data-open-agente]').forEach(a => a.addEventListener('click', e => {
    e.preventDefault();
    setAgente(true);
    $('button', agentePanel).focus();
  }));
})();

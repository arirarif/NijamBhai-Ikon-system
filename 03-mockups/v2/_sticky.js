/* _sticky.js — Draggable sticky notes with localStorage log */
(function () {
  const STORE_KEY = 'ikon-sticky-log';
  const COLORS = ['sn-yellow','sn-blue','sn-green','sn-pink','sn-purple'];
  const COLOR_DOTS = ['c-yellow','c-blue','c-green','c-pink','c-purple'];
  const COLOR_LABELS = ['yellow','blue','green','pink','purple'];
  let noteCount = 0;
  let logOpen = false;

  /* ── Launcher button ── */
  const fab = document.createElement('button');
  fab.id = 'sticky-launcher';
  fab.title = 'Add sticky note';
  fab.innerHTML = '📌<span class="sl-badge" id="sticky-badge" style="display:none">0</span>';
  document.body.appendChild(fab);

  /* ── Log panel ── */
  const logPanel = document.createElement('div');
  logPanel.id = 'sticky-log';
  logPanel.innerHTML = `
    <div class="sl-log-header">
      <span class="sl-log-title">📋 Saved Notes</span>
      <button class="sl-log-clear" id="sl-clear-btn">Clear all</button>
    </div>
    <div id="sl-log-body"></div>`;
  document.body.appendChild(logPanel);

  fab.addEventListener('click', (e) => {
    // right-click opens log, left-click creates note
    spawnNote();
  });
  fab.addEventListener('contextmenu', (e) => {
    e.preventDefault();
    toggleLog();
  });
  document.getElementById('sl-clear-btn').addEventListener('click', () => {
    localStorage.removeItem(STORE_KEY);
    renderLog();
    updateBadge();
  });

  function toggleLog() {
    logOpen = !logOpen;
    logPanel.classList.toggle('open', logOpen);
    renderLog();
  }

  /* ── Spawn note ── */
  function spawnNote(opts = {}) {
    noteCount++;
    const colorIdx = opts.colorIdx !== undefined ? opts.colorIdx : (noteCount - 1) % COLORS.length;
    const x = opts.x || (80 + (noteCount * 30) % 400);
    const y = opts.y || (80 + (noteCount * 24) % 280);

    const note = document.createElement('div');
    note.className = 'sticky-note ' + COLORS[colorIdx];
    note.style.left = x + 'px';
    note.style.top  = y + 'px';
    note.dataset.colorIdx = colorIdx;

    note.innerHTML = buildNoteHTML(colorIdx, opts.text || '');
    document.body.appendChild(note);

    /* drag */
    const header = note.querySelector('.sn-header');
    makeDraggable(note, header);

    /* color dots */
    note.querySelectorAll('.sn-color-dot').forEach((dot, i) => {
      if (i === colorIdx) dot.classList.add('active');
      dot.addEventListener('click', (e) => {
        e.stopPropagation();
        note.className = 'sticky-note ' + COLORS[i];
        note.dataset.colorIdx = i;
        note.querySelectorAll('.sn-color-dot').forEach(d => d.classList.remove('active'));
        dot.classList.add('active');
      });
    });

    /* close */
    note.querySelector('.sn-close').addEventListener('click', () => {
      note.style.transform = 'scale(.85)';
      note.style.opacity = '0';
      note.style.transition = 'all .18s';
      setTimeout(() => note.remove(), 200);
    });

    /* pin (show on top) */
    note.querySelector('.sn-pin-btn').addEventListener('click', () => {
      const pinBtn = note.querySelector('.sn-pin-btn');
      const isPinned = pinBtn.classList.toggle('pinned');
      note.style.zIndex = isPinned ? '9999' : '8500';
    });

    /* save to log */
    note.querySelector('.sn-save-btn').addEventListener('click', () => {
      const text = note.querySelector('.sn-textarea').value.trim();
      if (!text) return;
      saveToLog(text, colorIdx);
      const btn = note.querySelector('.sn-save-btn');
      btn.textContent = '✓ Saved';
      btn.classList.add('saved');
      setTimeout(() => { btn.textContent = 'Save to log'; btn.classList.remove('saved'); }, 1800);
    });

    /* live timestamp */
    note.querySelector('.sn-timestamp').textContent = 'Just now · ' + getPageLabel();
  }

  function buildNoteHTML(colorIdx, text) {
    const dotsHTML = COLOR_DOTS.map((c, i) =>
      `<span class="sn-color-dot ${c}${i===colorIdx?' active':''}"></span>`
    ).join('');
    return `
      <div class="sn-header">
        <span class="sn-drag-dots">⠿⠿</span>
        <div class="sn-colors">${dotsHTML}</div>
        <button class="sn-close" title="Close">✕</button>
      </div>
      <div class="sn-body">
        <textarea class="sn-textarea" placeholder="Type your note here…" rows="5">${text}</textarea>
      </div>
      <div class="sn-footer">
        <span class="sn-timestamp"></span>
        <button class="sn-pin-btn" title="Pin on top">📌</button>
        <button class="sn-save-btn">Save to log</button>
      </div>`;
  }

  /* ── Drag logic ── */
  function makeDraggable(el, handle) {
    let startX, startY, startL, startT;
    handle.addEventListener('mousedown', (e) => {
      if (e.target.classList.contains('sn-close') || e.target.classList.contains('sn-color-dot')) return;
      e.preventDefault();
      startX = e.clientX; startY = e.clientY;
      startL = parseInt(el.style.left) || 0;
      startT = parseInt(el.style.top)  || 0;
      el.style.zIndex = '9100';
      el.style.transition = 'box-shadow .1s';

      function onMove(e) {
        el.style.left = (startL + e.clientX - startX) + 'px';
        el.style.top  = (startT + e.clientY - startY) + 'px';
      }
      function onUp() {
        if (!el.querySelector('.sn-pin-btn').classList.contains('pinned'))
          el.style.zIndex = '8500';
        window.removeEventListener('mousemove', onMove);
        window.removeEventListener('mouseup', onUp);
      }
      window.addEventListener('mousemove', onMove);
      window.addEventListener('mouseup', onUp);
    });
  }

  /* ── Log ── */
  function saveToLog(text, colorIdx) {
    const notes = getLog();
    notes.unshift({ text, colorIdx, page: getPageLabel(), time: new Date().toLocaleString() });
    localStorage.setItem(STORE_KEY, JSON.stringify(notes));
    updateBadge();
    if (logOpen) renderLog();
  }

  function getLog() {
    try { return JSON.parse(localStorage.getItem(STORE_KEY) || '[]'); }
    catch(e) { return []; }
  }

  function renderLog() {
    const body = document.getElementById('sl-log-body');
    const notes = getLog();
    if (!notes.length) {
      body.innerHTML = '<div class="sl-log-empty">No saved notes yet.<br>Write a note and hit "Save to log".</div>';
      return;
    }
    body.innerHTML = notes.map((n, i) =>
      `<div class="sl-log-item">
        <div class="sli-text">${escapeHTML(n.text)}</div>
        <div class="sli-meta">${n.page} · ${n.time}</div>
      </div>`
    ).join('');
  }

  function updateBadge() {
    const count = getLog().length;
    const badge = document.getElementById('sticky-badge');
    if (count > 0) { badge.textContent = count; badge.style.display = 'flex'; }
    else badge.style.display = 'none';
  }

  function getPageLabel() {
    const title = document.title || window.location.pathname;
    return title.replace(' — IKON', '').trim();
  }

  function escapeHTML(s) {
    return s.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');
  }

  updateBadge();
})();

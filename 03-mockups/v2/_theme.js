/**
 * IKON GAS — Theme Toggle
 * Injects a Dark / Light switcher button into every page's sidebar footer.
 * Persists selection to localStorage.
 */
(function () {
  var STORAGE_KEY = 'ikon-theme';

  // Apply theme immediately (before paint) to avoid flash
  var saved = localStorage.getItem(STORAGE_KEY) || 'dark';
  document.body.setAttribute('data-theme', saved);

  function applyTheme(theme) {
    document.body.setAttribute('data-theme', theme);
    localStorage.setItem(STORAGE_KEY, theme);
    updateBtnLabel(theme);
  }

  function updateBtnLabel(theme) {
    var btn = document.getElementById('ikon-theme-btn');
    if (!btn) return;
    if (theme === 'light') {
      btn.innerHTML = '<span class="ttb-icon">&#127769;</span> Switch to Dark Mode';
    } else {
      btn.innerHTML = '<span class="ttb-icon">&#9728;</span> Switch to Light Mode';
    }
  }

  function injectButton() {
    var footer = document.querySelector('.sidebar-footer');
    if (!footer) return;

    var btn = document.createElement('button');
    btn.id = 'ikon-theme-btn';
    btn.className = 'theme-toggle-btn';
    btn.onclick = function () {
      var current = document.body.getAttribute('data-theme') || 'dark';
      applyTheme(current === 'dark' ? 'light' : 'dark');
    };

    // Insert right above the sidebar footer
    footer.parentNode.insertBefore(btn, footer);
    updateBtnLabel(document.body.getAttribute('data-theme'));
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', injectButton);
  } else {
    injectButton();
  }
})();

/* ─────────────────────────────────────────────────────────────
   Mobile Sidebar Toggle
   Injects a hamburger button into the topbar + handles overlay.
   ───────────────────────────────────────────────────────────── */
(function () {
  function injectHamburger() {
    var topbar = document.getElementById('topbar');
    if (!topbar || document.getElementById('mob-menu-btn')) return;

    // Create hamburger button
    var btn = document.createElement('button');
    btn.id = 'mob-menu-btn';
    btn.className = 'mob-menu-btn';
    btn.setAttribute('aria-label', 'Open navigation');
    btn.innerHTML = '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><line x1="3" y1="6" x2="21" y2="6"/><line x1="3" y1="12" x2="21" y2="12"/><line x1="3" y1="18" x2="21" y2="18"/></svg>';
    topbar.insertBefore(btn, topbar.firstChild);

    // Create overlay
    var overlay = document.createElement('div');
    overlay.id = 'sidebar-overlay';
    document.body.appendChild(overlay);

    // Toggle sidebar open/close
    btn.addEventListener('click', function () {
      document.body.classList.toggle('sidebar-open');
    });

    // Close on overlay click
    overlay.addEventListener('click', function () {
      document.body.classList.remove('sidebar-open');
    });

    // Close sidebar when a nav link is clicked (mobile nav)
    var sidebar = document.getElementById('sidebar');
    if (sidebar) {
      sidebar.addEventListener('click', function (e) {
        if (e.target.closest('.nav-item') && window.innerWidth <= 900) {
          document.body.classList.remove('sidebar-open');
        }
      });
    }

    // Close sidebar on Escape key
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape') {
        document.body.classList.remove('sidebar-open');
      }
    });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', injectHamburger);
  } else {
    injectHamburger();
  }
})();

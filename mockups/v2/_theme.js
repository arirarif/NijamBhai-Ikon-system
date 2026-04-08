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

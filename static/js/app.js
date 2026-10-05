/* ============================================================
   PolarOps — app.js
   Theme toggle, mobile menu, scroll reveal, stat counters
   ============================================================ */

// ---------- Theme ----------
const html = document.documentElement;
const THEME_KEY = 'polarops-theme';

function applyTheme(theme) {
  if (theme === 'dark') {
    html.classList.add('dark');
  } else {
    html.classList.remove('dark');
  }
}

function toggleTheme() {
  const isDark = html.classList.contains('dark');
  const next = isDark ? 'light' : 'dark';
  localStorage.setItem(THEME_KEY, next);
  applyTheme(next);
}

// Apply saved or default theme on load
applyTheme(localStorage.getItem(THEME_KEY) || 'light');

// Wire all theme toggle buttons
document.addEventListener('DOMContentLoaded', () => {
  document.querySelectorAll('[data-theme-toggle]').forEach(btn => {
    btn.addEventListener('click', toggleTheme);
  });

  // ---------- Mobile Menu ----------
  const mobileBtn = document.getElementById('mobile-menu-btn');
  const mobileMenu = document.getElementById('mobile-menu');
  if (mobileBtn && mobileMenu) {
    mobileBtn.addEventListener('click', () => {
      mobileMenu.classList.toggle('hidden');
    });
  }

  // ---------- Scroll Reveal ----------
  const observer = new IntersectionObserver((entries) => {
    entries.forEach(e => {
      if (e.isIntersecting) {
        e.target.classList.add('visible');
        observer.unobserve(e.target);
      }
    });
  }, { threshold: 0.15 });

  document.querySelectorAll('.reveal').forEach(el => observer.observe(el));

  // ---------- Stat Counter ----------
  function animateCount(el) {
    const target = parseInt(el.dataset.target, 10);
    const duration = 1800;
    const start = performance.now();
    const update = (now) => {
      const progress = Math.min((now - start) / duration, 1);
      const ease = 1 - Math.pow(1 - progress, 3); // ease-out-cubic
      el.textContent = Math.floor(ease * target);
      if (progress < 1) requestAnimationFrame(update);
      else el.textContent = target;
    };
    requestAnimationFrame(update);
  }

  const statObserver = new IntersectionObserver((entries) => {
    entries.forEach(e => {
      if (e.isIntersecting) {
        animateCount(e.target);
        statObserver.unobserve(e.target);
      }
    });
  }, { threshold: 0.5 });

  document.querySelectorAll('[data-target]').forEach(el => statObserver.observe(el));

  // ---------- Navbar scroll shadow ----------
  const navbar = document.getElementById('main-navbar');
  if (navbar) {
    window.addEventListener('scroll', () => {
      if (window.scrollY > 10) {
        navbar.classList.add('shadow-sm');
      } else {
        navbar.classList.remove('shadow-sm');
      }
    }, { passive: true });
  }

  // ---------- Delete confirmation ----------
  document.querySelectorAll('[data-confirm]').forEach(btn => {
    btn.addEventListener('click', e => {
      if (!confirm(btn.dataset.confirm || 'Are you sure?')) {
        e.preventDefault();
      }
    });
  });
});

// Light mode alternates photos by the visitor's local date: library on even days, desk on odd.
// Runs before first paint so the header, hero and footer never flicker between them.
const LIGHT_PHOTO = (() => {
  const d = new Date();
  const day = Math.floor(Date.UTC(d.getFullYear(), d.getMonth(), d.getDate()) / 864e5);
  return day % 2 === 0 ? 'library' : 'desk';
})();
document.documentElement.dataset.lightPhoto = LIGHT_PHOTO;

// Contributors/feedback are hidden by CSS and shown only on content pages
// (not on the home page, section overviews, categories or tags).
const OVERVIEW_PATHS = ['/', '/cs-fundamentals/', '/c/', '/java/', '/lab/', '/blog/', '/projects/', '/languages/', '/about/'];

document.addEventListener('DOMContentLoaded', () => {
  const path = window.location.pathname;

  const isOverviewPage = OVERVIEW_PATHS.includes(path)
    || path.endsWith('/index.html')
    || path.includes('categories')
    || path.includes('tags');
  document.body.classList.toggle('show-contrib-feedback', !isOverviewPage);

  if (document.getElementById('hero-title')) initHero();

  injectFooterResources();
});

// "Back to top": starts slow and picks up speed toward the top, instead of the browser's near-instant
// smooth scroll. Longer pages take a little longer (0.6 to 1.1 s). Skipped for reduced motion.
document.addEventListener('click', e => {
  if (!e.target.closest('.md-top')) return;
  if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;
  e.preventDefault();
  e.stopImmediatePropagation();

  const start = window.scrollY;
  const duration = Math.min(1100, Math.max(600, start * 0.25));
  const ease = t => t * t * t;
  const root = document.documentElement;
  const previous = root.style.scrollBehavior;
  root.style.scrollBehavior = 'auto';
  let t0;
  const step = now => {
    t0 ??= now;
    const t = Math.min(1, (now - t0) / duration);
    window.scrollTo(0, start * (1 - ease(t)));
    if (t < 1) requestAnimationFrame(step);
    else root.style.scrollBehavior = previous;
  };
  requestAnimationFrame(step);
}, true);

// Edit this list to add or remove footer links.
const FOOTER_COLUMNS = [
  {
    title: 'C Language',
    links: [
      { label: 'The C Programming Language (K&R)', href: 'https://www.informit.com/store/c-programming-language-9780133086225' },
      { label: 'Le langage C (K&R, FR)', href: 'https://www.dunod.com/sciences-techniques/langage-c-norme-ansi-0' },
      { label: "Beej's Guide to C", href: 'https://beej.us/guide/bgc/html/split-wide/' },
      { label: 'C Programming: A Modern Approach', href: 'http://knking.com/books/c2/' },
      { label: 'Robert C. Seacord', href: 'https://clark.center/users/Rcseacord' },
    ],
  },
  {
    title: 'Computer Science',
    links: [
      { label: 'CS Primer', href: 'https://csprimer.com/courses/' },
      { label: 'Teach Yourself CS', href: 'https://teachyourselfcs.com/' },
      { label: 'CS50 on edX', href: 'https://www.edx.org/cs50' },
    ],
  },
  {
    title: 'Codelogium',
    links: [
      { label: 'Blog', href: '/blog/' },
      { label: 'Lab', href: '/lab/' },
      { label: 'Projects', href: '/projects/' },
    ],
  },
];

function injectFooterResources() {
  const footer = document.querySelector('.md-footer');
  if (!footer) return;

  const section = document.createElement('div');
  section.className = 'footer-resources md-grid';
  section.innerHTML = `
    <div class="footer-brand">
      <span class="footer-brand__name">Codelogium</span>
      <p class="footer-brand__line">Unlearn • Relearn • Keep learning</p>
    </div>
    ${FOOTER_COLUMNS.map(col => `
      <nav class="footer-col" aria-label="${col.title}">
        <h2 class="footer-col__title">${col.title}</h2>
        <ul>
          ${[...col.links].sort((a, b) => a.label.length - b.label.length).map(l => {
            const external = l.href.startsWith('http');
            return `<li><a href="${l.href}"${external ? ' target="_blank" rel="noopener"' : ''}>${l.label}</a></li>`;
          }).join('')}
        </ul>
      </nav>
    `).join('')}
  `;
  footer.prepend(section);
}

// The hero markup is rendered by overrides/main.html (home page only), so it shows without waiting for this script.
function initHero() {
  document.querySelector('#hero-title [href="#hero-scroll"]').addEventListener('click', e => {
    e.preventDefault();
    document.getElementById('whats-inside')?.scrollIntoView({ behavior: 'smooth' });
  });

  // Wait two frames so the theme has laid out the viewport.
  requestAnimationFrame(() => requestAnimationFrame(() => {
    initHeroCanvas(document.getElementById('hero-canvas'));
  }));
}

function initHeroCanvas(canvas) {
  if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;

  const ctx = canvas.getContext('2d');
  const GLYPHS = [
    'O(n log n)', 'O(1)', 'O(n²)', 'O(2ⁿ)',
    '∑', '∫', '∂', '∞', '∅', 'λ', '∀x', '∈', 'φ', 'π',
    'fn()', '{}', '[]', '=>', '::', 'async', 'type',
    '01', '10', 'n!', 'log₂n', '√2',
    'SELECT', 'while', 'class', 'import', 'return',
    '≤', '≥', '≠', '≡', '⊕', '2ⁿ', 'n·log n', '∇'
  ];
  // Where glyphs rise from: the laptop screen in each mode's photo, as a fraction of the photo.
  // Update these when changing --book-image. Only the aspect ratio of w/h matters.
  const PHOTOS = {
    library: { w: 2560, h: 1435, x: 0.74, y: 0.62 },
    desk:    { w: 2000, h: 1125, x: 0.8,  y: 0.5 },
    dark:    { w: 2560, h: 1707, x: 0.9,  y: 0.6 },
  };

  // Map a point on the photo to the screen, the same way `background-size: cover` crops it.
  // The horizontal crop comes from the CSS (--book-x); the vertical one is always 60%.
  const computeOrigin = () => {
    const p = PHOTOS[document.body.dataset.mdColorScheme === 'slate' ? 'dark' : LIGHT_PHOTO];
    const POS = { x: parseFloat(getComputedStyle(document.body).getPropertyValue('--book-x')) / 100, y: 0.6 };
    const scale = Math.max(canvas.width / p.w, canvas.height / p.h);
    const dw = p.w * scale, dh = p.h * scale;
    // Keep the glyphs on screen, and start them above the title so they never rise through it.
    const clamp = v => Math.min(0.85, Math.max(0.15, v));
    // #hero-title fills the screen with its text at the bottom, so measure the text itself.
    const titleText = document.querySelector('#hero-title > :first-child');
    const titleTop = (titleText.getBoundingClientRect().top + window.scrollY - 24) / canvas.height;
    return {
      x: clamp(((canvas.width - dw) * POS.x + p.x * dw) / canvas.width),
      y: Math.min(clamp(((canvas.height - dh) * POS.y + p.y * dh) / canvas.height), titleTop),
    };
  };
  // Layout reads are costly per glyph, so the origin is measured only when the layout or theme changes.
  let originCache = null;
  const origin = () => originCache || (originCache = computeOrigin());
  const invalidateOrigin = () => { originCache = null; };
  new MutationObserver(invalidateOrigin).observe(document.body, { attributes: true, attributeFilter: ['data-md-color-scheme'] });
  document.fonts?.ready.then(invalidateOrigin);
  // 70 glyphs on a 1440×900 screen, scaled by screen area so phones aren't crowded.
  const glyphCount = () => Math.round(Math.min(70, Math.max(24, canvas.width * canvas.height / 18500)));
  // Horizontal spread around the origin, with a floor so narrow screens don't get a thin column.
  const spreadWidth = () => Math.max(canvas.width * 0.16, 110);
  const BURST_SIZE = 12;

  class Glyph {
    constructor() { this.reset(true); }

    reset(scatter) {
      const o = origin();
      const side = Math.random() < 0.5 ? -1 : 1;
      const spread = Math.random();
      this.x = canvas.width * o.x + side * spread * spreadWidth() * (0.2 + Math.random() * 0.8);
      this.y = canvas.height * o.y - spread * canvas.height * 0.05 + (Math.random() - 0.5) * 6;
      this.vx = side * spread * 0.28 + (Math.random() - 0.5) * 0.15;
      this.vy = -(0.28 + Math.random() * 0.62);

      this.text = GLYPHS[Math.floor(Math.random() * GLYPHS.length)];
      this.size = 8 + Math.random() * 9;
      this.maxOpacity = 0.18 + Math.random() * 0.5;
      this.opacity = 0;
      this.maxLife = 200 + Math.random() * 340;
      this.life = scatter ? Math.floor(Math.random() * this.maxLife) : 0;
      this.bright = Math.random() > 0.5;
      this.burst = false;
    }

    update() {
      this.life++;
      this.x += this.vx;
      this.y += this.vy;

      const fadeIn = 30, fadeOut = 50;
      if (this.life < fadeIn) {
        this.opacity = (this.life / fadeIn) * this.maxOpacity;
      } else if (this.life > this.maxLife - fadeOut) {
        this.opacity = ((this.maxLife - this.life) / fadeOut) * this.maxOpacity;
      } else {
        this.opacity = this.maxOpacity;
      }
    }

    get done() { return this.life >= this.maxLife; }

    draw() {
      ctx.globalAlpha = Math.max(0, this.opacity);
      ctx.font = `${this.size}px "JetBrains Mono", "Courier New", monospace`;
      ctx.fillStyle = this.bright ? '#4ade80' : '#22c55e';
      ctx.shadowBlur = this.bright ? 10 : 5;
      ctx.fillText(this.text, this.x, this.y);
    }
  }

  let glyphs = [];
  let lastWidth = 0;

  function resize() {
    // Phones fire resize as the address bar slides during scroll; only a width change needs a rebuild.
    if (window.innerWidth === lastWidth) return;
    lastWidth = window.innerWidth;
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
    invalidateOrigin();
    glyphs = Array.from({ length: glyphCount() }, () => new Glyph());
  }

  let resizeTimer;
  const onResize = () => {
    clearTimeout(resizeTimer);
    resizeTimer = setTimeout(resize, 150);
  };

  // The content panel covers the hero once scrolled a screen down; stop drawing until it's back.
  let frame = 0;
  const heroVisible = () => window.scrollY < window.innerHeight;
  const start = () => { if (!frame && heroVisible()) frame = requestAnimationFrame(animate); };
  window.addEventListener('scroll', start, { passive: true });

  function animate() {
    if (!heroVisible()) {
      frame = 0;
      return;
    }
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    ctx.shadowColor = '#22c55e';
    // Ambient glyphs recycle; burst glyphs are removed when they fade out.
    glyphs = glyphs.filter(g => {
      g.update();
      if (g.done) {
        if (g.burst) return false;
        g.reset(false);
      }
      g.draw();
      return true;
    });
    frame = requestAnimationFrame(animate);
  }

  document.addEventListener('click', e => {
    if (e.target.closest('a, button')) return;
    if (window.scrollY > window.innerHeight * 0.5) return;
    for (let i = 0; i < BURST_SIZE; i++) {
      const g = new Glyph();
      const angle = (Math.PI * 2 * i / BURST_SIZE) + (Math.random() - 0.5) * 0.5;
      const speed = 0.6 + Math.random();
      g.x = e.clientX + (Math.random() - 0.5) * 10;
      g.y = e.clientY + window.scrollY + (Math.random() - 0.5) * 10;
      g.vx = Math.cos(angle) * speed;
      g.vy = Math.sin(angle) * speed - 0.35;
      g.life = 0;
      g.maxOpacity = 0.5 + Math.random() * 0.45;
      g.bright = true;
      g.burst = true;
      glyphs.push(g);
    }
  });

  window.addEventListener('resize', onResize);
  resize();
  start();
}

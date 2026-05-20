# MandrellCFO — mandrellscfo.com

Marketing site for **Mandrell's CFO Services** — family-owned operational
accounting and fractional CFO firm in Gainesville, Florida.

Static HTML/CSS/JS — no framework, no build step.

## Stack
- Plain HTML + CSS + JS
- Fonts: Fraunces (display) · DM Sans (body) · JetBrains Mono (eyebrows)
- Palette: white background, forest-green accent `#1f3d2b`, warm bronze
  `#c89b54`, ledger-cream panel `#f6f3ec`
- Intake form: [Formsubmit.co](https://formsubmit.co) AJAX endpoint →
  `cfo@mandrells.com` (the first real submission must be confirmed via the
  email Formsubmit sends to that inbox before the form goes live)

## Structure
```
public_html/
├── index.html          # Home — hero, services, engagement, industries, firm, team, CTA
├── intake.html         # Secure intake form (Formsubmit.co backend)
├── styles.css          # All styles, linked as styles.css?v=N for cache-busting
├── script.js           # Nav menu toggle, reveal animations, form handling
├── assets/team/        # Staff headshots (512x768 sourced from mandrellscfo.com)
└── team/               # 10 individual bio pages, one per team member
    ├── christina.html  ├── shane.html       ├── brielle.html
    ├── sarah.html      ├── ashley.html      ├── lisa.html
    ├── destiny.html    ├── kaylee.html      ├── lashaune.html
    └── johnathan.html
```

Each `team/*.html` page is name + floated headshot + verbatim bio text from
mandrellscfo.com/about-us. Bios link from the team grid on the home page and
from the founders cards in the hero + The Firm section.

## Working on the site

### Editing
Open the files directly — no install, no compile. Preview locally with:
```sh
open index.html
```

### CSS cache busting
The stylesheet is linked everywhere as `styles.css?v=N`. **After any CSS
edit**, bump the version across all HTML files so browsers fetch the fresh
copy instead of a cached one:
```sh
# Replace 9 → 10 (or whatever the next version is)
for f in index.html intake.html team/*.html; do
  sed -i '' 's|styles.css?v=9|styles.css?v=10|g' "$f"
done
```

### Adding a team member
1. Drop a headshot into `assets/team/firstname.webp` (4:5 ratio, ≥512×768)
2. Copy any existing `team/firstname.html` as a template; update the title,
   meta description, `<img>`, `<h1>` name, prose paragraphs, and prev/next
   links to keep the chain intact
3. Add a `<a class="team-member" href="team/firstname.html">…</a>` card in
   the team grid on `index.html`

## Contact (in-app)
- Phone: **(352) 248-0518**
- Email: **cfo@mandrells.com**
- Office: 235 South Main St, Suite W201, Gainesville, FL 32601
- Social: Facebook + X (`mandrellscfo` on both)

## Deployment
- **Repo**: [github.com/eolsen33/mandrellscfo-site](https://github.com/eolsen33/mandrellscfo-site)
- **Host**: Hostinger, GIT auto-deploy from `main`. Repo root **is**
  `public_html/`, so anything pushed to `main` is served live.
- **Demo URL**: `https://mandrellscfo.ericolsen.studio`
- **Production target**: `https://mandrellscfo.com`

Push to ship:
```sh
git add -A
git commit -m "your message"
git push origin main
```

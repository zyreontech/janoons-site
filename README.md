# janoons.com — static site

Built from `../Janoon Design Guide.html` (brand & web guide v1.0). Pages are generated: edit `build.py` (copy + structure) or `styles.css`, then run `python3 build.py`. The v1 (plainer) layout is kept in `../site-v1/`. No framework, no jQuery.

## Files

| Path | Purpose |
|---|---|
| `index.html` | Home |
| `services.html` | Six services, full detail |
| `government.html` | MBE certifications, agency clients, NAICS/NIGP code tables |
| `contact.html` | Inquiry form (validated client-side, posts to `/thanks.html`) |
| `thanks.html` | Form success page (`noindex`) |
| `404.html` | Not-found page |
| `gov.html` | Meta-refresh redirect for the legacy URL (also in `_redirects`) |
| `styles.css` | All styling; tokens are CSS custom properties in `:root` |
| `fonts.css`, `fonts/` | Self-hosted latin woff2: Newsreader 500 (+italic), Public Sans 400/500/600/700, IBM Plex Mono 400/500 — 249 KB total, SIL OFL |
| `script.js` | Mobile nav toggle, form validation + submission |
| `logo/` | Mark, wordmark, favicon (SVG), 512 px icon, 1200×630 OG image |
| `sitemap.xml`, `robots.txt` | Crawl basics |
| `_redirects`, `_headers`, `netlify.toml` | Netlify config (301 for `/gov.html`, security + cache headers) |

## Deploy

**Netlify (zero-config):** drag the `site/` folder onto app.netlify.com, or `netlify deploy --prod --dir=.`. Netlify Forms picks up the contact form automatically (`data-netlify="true"`); submissions appear under Site → Forms, and you can set an email notification there.

**Any other static host (Firebase, S3/CloudFront, Hostinger, cPanel):** upload everything as-is. Then do two things:

1. Point the form somewhere. In `contact.html` change `action="/thanks.html"` to your endpoint — e.g. Formspree (`https://formspree.io/f/<id>`) or FormSubmit (`https://formsubmit.co/info@janoons.com`). `script.js` POSTs to whatever `action` is and shows the inline success state on 2xx; if the fetch fails it falls back to a normal form POST.
2. Replicate `_redirects` (`/gov.html → /government.html` 301) in the host's own config; the meta-refresh in `gov.html` covers you until then.

Absolute paths (`/styles.css`, `/logo/...`) assume the site is served from the domain root.

## Editing

- Copy lives in the HTML; nav + footer are duplicated per page (5 pages — search-and-replace is fine).
- Colours, type, spacing: top of `styles.css`.
- Logo geometry: `../logo/build-logos.py` regenerates every SVG; copy the outputs into `logo/`.
- Keep one `<h1>` per page and the eyebrow → h1/h2 → lede order; the design depends on it.

## Launch checklist

- [ ] Confirm the *junoon* reading of the name with the owner (it informs the coral "spark" in the mark)
- [ ] Confirm the trimmed testimonial and named agency clients may be published
- [ ] Set the form notification email (Netlify) or endpoint (other hosts)
- [ ] Add real photography only if available — the design is intentionally image-free
- [ ] After DNS cutover, submit `https://janoons.com/sitemap.xml` in Google Search Console

## Run locally

```sh
cd site && python3 serve.py        # → http://localhost:8799
```

`serve.py` (stdlib only) mirrors the hosting behaviour: 301 for `/gov.html`, real 404 status with `404.html`, and the contact form POST is accepted, logged to `_submissions.log`, and redirected to `/thanks.html`. Edit files and reload — nothing is cached.

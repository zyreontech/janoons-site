#!/usr/bin/env python3
"""Generate every page of janoons.com from shared templates. Run: python3 build.py (in site/)."""
import os, datetime
OUT = os.path.dirname(os.path.abspath(__file__))

MARK = '''<svg class="mark" viewBox="0 0 100 100" aria-hidden="true"><rect class="spark" x="14" y="14" width="16" height="16"/><path d="M36 14 H86 V62 A28 28 0 0 1 30 62 V54 H46 V62 A12 12 0 0 0 70 62 V30 H36 Z" fill="currentColor"/></svg>'''
WORDMARK_DEFS = '''<svg width="0" height="0" style="position:absolute" aria-hidden="true"><defs>
<clipPath id="cJ"><rect width="68" height="100"/></clipPath><clipPath id="cA"><rect width="84" height="100"/></clipPath><clipPath id="cN"><rect width="84" height="100"/></clipPath><clipPath id="cO"><rect width="100" height="100"/></clipPath>
<g id="gJ" clip-path="url(#cJ)"><path d="M60 -10 V66 A26 26 0 0 1 8 66 V58"/></g>
<g id="gA" clip-path="url(#cA)"><path d="M4.5 112 L42 2 L79.5 112" stroke-linejoin="miter" stroke-miterlimit="8"/><path d="M18 64 H66"/></g>
<g id="gN" clip-path="url(#cN)"><path d="M8 112 V0 L76 100 V-12" stroke-linejoin="miter" stroke-miterlimit="8"/></g>
<g id="gO" clip-path="url(#cO)"><circle cx="50" cy="50" r="42"/></g>
<g id="wordmark" fill="none" stroke="currentColor" stroke-width="16"><use href="#gJ" x="0"/><use href="#gA" x="96"/><use href="#gN" x="208"/><use href="#gO" x="320"/><use href="#gO" x="448"/><use href="#gN" x="576"/></g>
</defs></svg>'''
ARR = '<span class="arr" aria-hidden="true">&rarr;</span>'
LOCKUP = f'<a class="lockup" href="/" aria-label="Janoon Inc. — home">{MARK}<svg class="wm" viewBox="0 0 660 100" aria-hidden="true"><use href="#wordmark"/></svg></a>'
NAV_ITEMS = [("/services.html","Services"),("/government.html","Government"),("/contact.html","Contact")]

def nav(current, dark=True):
    links = "".join(f'<li><a href="{h}"{" aria-current=\"page\"" if current==h else ""}>{l}</a></li>' for h,l in NAV_ITEMS)
    return f'''<header class="site-header{' dark' if dark else ''}"><div class="wrap"><nav class="nav" aria-label="Primary">
  {LOCKUP}
  <button class="menu-btn" type="button" aria-expanded="false" aria-controls="nav-links"><i></i>Menu</button>
  <div class="right" id="nav-links"><ul>{links}</ul><a class="btn btn-primary" href="/contact.html">Send an inquiry {ARR}</a></div>
</nav></div></header>'''

FOOTER = f'''<footer class="site-footer on-dark"><div class="wrap">
  <div class="top">
    <div>{LOCKUP}<p>Complete IT solutions for businesses and public agencies in New York. We focus on your technology so you can focus on your work.</p></div>
    <div><h4>Company</h4><ul><li><a href="/services.html">Services</a></li><li><a href="/government.html">Government contracts</a></li><li><a href="/contact.html">Contact</a></li></ul></div>
    <div><h4>Reach us</h4><ul><li><a href="tel:+19292693761">+1 (929) 269-3761</a></li><li><a href="mailto:info@janoons.com">info@janoons.com</a></li><li>New York, NY</li></ul></div>
  </div>
  <div class="bottom"><span>&copy; Janoon Inc. {datetime.date.today().year}</span><span>MBE certified &mdash; New York City &middot; New York State &middot; Port Authority of NY &amp; NJ</span></div>
</div></footer>'''

JSONLD = '''<script type="application/ld+json">{"@context":"https://schema.org","@type":"LocalBusiness","name":"Janoon Inc.","url":"https://janoons.com/","logo":"https://janoons.com/logo/janoon-icon-512.png","image":"https://janoons.com/logo/janoon-og-image.png","telephone":"+1-929-269-3761","email":"info@janoons.com","address":{"@type":"PostalAddress","addressLocality":"New York","addressRegion":"NY","addressCountry":"US"},"description":"IT services firm in New York: web and software development, network and desktop support, data management, cloud services, Citrix virtualization, and professional staffing. MBE certified by New York City, New York State, and the Port Authority of NY & NJ."}</script>'''

def head(title, desc, path, noindex=False):
    c = f"https://janoons.com{path}"
    return f'''<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title><meta name="description" content="{desc}">{'<meta name="robots" content="noindex">' if noindex else ''}
<link rel="canonical" href="{c}">
<meta property="og:type" content="website"><meta property="og:title" content="{title}"><meta property="og:description" content="{desc}"><meta property="og:url" content="{c}"><meta property="og:image" content="https://janoons.com/logo/janoon-og-image.png"><meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#061535">
<link rel="icon" href="/logo/favicon.svg" type="image/svg+xml"><link rel="apple-touch-icon" href="/logo/janoon-icon-512.png">
<link rel="preload" href="/fonts/SchibstedGrotesk-800-normal.woff2" as="font" type="font/woff2" crossorigin><link rel="preload" href="/fonts/PublicSans-400-normal.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="/fonts.css"><link rel="stylesheet" href="/styles.css">
{JSONLD}'''

def page(title, desc, path, current, body, noindex=False):
    return f'''<!doctype html>
<html lang="en">
<head>
{head(title, desc, path, noindex)}
</head>
<body>
<a class="skip-link" href="#main">Skip to content</a>
{WORDMARK_DEFS}
{nav(current)}
<main id="main">
{body}
</main>
{FOOTER}
<script src="/script.js"></script>
</body>
</html>
'''

SERVICES = [
  ("web","Web design &amp; software","Custom web design and proprietary software with ongoing updates and maintenance &mdash; front end, back end, and a mobile-friendly interface.",["Web design &amp; maintenance","Dashboards &amp; automation","App development"]),
  ("network","Desktop support &amp; network setup","Workstations, servers, switches, wireless, and firewalls installed and supported, with migrations from old to new versions and post-migration support.",["Hardware &amp; software installation","Windows, Teams, Microsoft 365","Database migrations","Mobile setup"]),
  ("data","Data management","We collect, organize, protect, and store data so your organization can analyze it and forecast with confidence.",["CRM","Marketing technology","Data warehouse &amp; analytics"]),
  ("cloud","Cloud services","Complete cloud set-up for application hosting, data and website hosting, and scaling on Amazon AWS or Microsoft Azure.",["EC2, S3, RDS, CloudFront","Azure migration &amp; .NET","Azure consulting"]),
  ("citrix","Citrix","Securely delivered Windows applications and virtual desktops &mdash; a cost-effective virtual workspace with every resource your users need.",["App virtualization &amp; VDI","NetScaler","Provisioning &amp; MCS","App layering, WEM"]),
  ("staffing","Professional staffing","Candidates matched to your role anywhere in the United States, by recruiters focused on the industries we serve.",["Accounting &amp; finance","Healthcare","IT","HR","Legal","Real estate"]),
]
GO = '<span class="go" aria-hidden="true">&rarr;</span>'

def svc_cards():
    out=[]
    for i,(slug,name,desc,caps) in enumerate(SERVICES, start=1):
        feat = ' feature' if i==1 else (' wide' if i==len(SERVICES) else '')
        chips = "".join(f"<span>{c}</span>" for c in caps)
        if feat == ' wide':
            out.append(f'<a class="svc{feat} rv" data-d="{min(i,5)}" href="/services.html#{slug}">{GO}<span class="n">0{i}</span><span class="body"><h3>{name}</h3><p>{desc}</p></span><span class="caps">{chips}</span></a>')
        else:
            out.append(f'<a class="svc{feat} rv" data-d="{min(i,5)}" href="/services.html#{slug}">{GO}<span class="n">0{i}</span><h3>{name}</h3><p>{desc}</p><span class="caps">{chips}</span></a>')
    return "\n".join(out)

CLIENTS = [("Metropolitan Transportation Authority","New York"),("NYC Health + Hospitals","New York"),("Nassau County","New York"),("City of Tacoma","Washington")]
MARQUEE_ITEMS = ["MTA","NYC Health + Hospitals","Nassau County","City of Tacoma","Healthfirst","New York Life","Steward Health Care","Greater New York Chamber of Commerce","Xinix Media"]

def marquee():
    items = "".join(f"<span>{x}</span>" for x in MARQUEE_ITEMS)
    return f'<div class="marquee" aria-label="Clients"><div class="track"><span class="lbl">Trusted by</span>{items}<span class="lbl">Trusted by</span>{items}</div></div>'

def gov_band():
    cl = "".join(f"<li>{n}<small>{w}</small></li>" for n,w in CLIENTS)
    return f'''<section class="gov on-dark section"><div class="wrap">
  <div class="rv"><p class="eyebrow">Government contracts</p><h2>Certified, and already on agency rosters.</h2>
    <p>Janoon Inc. is a Minority Business Enterprise with NAICS and NIGP codes on file &mdash; ready for public-sector procurement.</p>
    <ul class="certs"><li>MBE &middot; New York City</li><li>MBE &middot; New York State</li><li>MBE &middot; Port Authority NY &amp; NJ</li></ul>
    <div class="btn-row"><a class="btn btn-primary" href="/government.html">View codes &amp; certifications {ARR}</a></div></div>
  <ul class="clients rv" data-d="2">{cl}</ul>
</div></section>'''

QUOTE = '''<section class="quote section"><div class="wrap rv">
  <p class="eyebrow">What clients say</p>
  <blockquote>We have chosen his organization to redesign our website. Working with Danish and his team has been amazing &mdash; professional, timely and thorough.</blockquote>
  <cite><span class="av" aria-hidden="true">HN</span><span><b>Helana Natt</b>Executive Director, Greater New York Chamber of Commerce</span></cite>
</div></section>'''

def cta(title="Tell us what you&rsquo;re working on.", text="We&rsquo;ll scope the work, match it to the right service, and get back to you within one business day."):
    return f'''<section class="cta section"><div class="wrap"><div class="box on-dark rv">
  <div><p class="eyebrow">Get started</p><h2>{title}</h2><p>{text}</p><div class="btn-row"><a class="btn btn-primary" href="/contact.html">Send an inquiry {ARR}</a></div></div>
  <div class="side">
    <a href="tel:+19292693761"><span><small>Call</small>+1 (929) 269-3761</span>{ARR}</a>
    <a href="mailto:info@janoons.com"><span><small>E-mail</small>info@janoons.com</span>{ARR}</a>
    <a href="/government.html"><span><small>Agencies</small>Certifications &amp; codes</span>{ARR}</a>
  </div>
</div></div></section>'''

# ───────── HOME ─────────
home = f'''<section class="hero on-dark"><div class="wrap">
  <div>
    <p class="eyebrow rv">IT services &middot; New York, NY</p>
    <h1 class="rv" data-d="1">Complete IT solutions, so you can focus on <span class="serif-em">growing</span> your business.</h1>
    <p class="lead rv" data-d="2">Software, infrastructure, cloud, and staffing for businesses and public agencies. We focus on your technology while you focus on your work.</p>
    <div class="btn-row rv" data-d="3"><a class="btn btn-coral" href="/contact.html">Send an inquiry {ARR}</a><a class="btn btn-secondary" href="/services.html">Explore services</a></div>
    <div class="trust rv" data-d="4"><div><b>6</b>Service lines</div><div><b>3</b>MBE certifications</div><div><b>NY</b>Headquartered</div></div>
  </div>
  <aside class="cred rv" data-d="2" aria-label="Credentials">
    <span class="tag"><i></i>MBE certified</span>
    <h2>Trusted by New York&rsquo;s public agencies.</h2>
    <dl>
      <div><dt>Certified</dt><dd>New York City &middot; New York State &middot; Port Authority of NY &amp; NJ</dd></div>
      <div><dt>Clients</dt><dd>MTA, NYC Health + Hospitals, Nassau County, City of Tacoma</dd></div>
      <div><dt>Contact</dt><dd><a href="tel:+19292693761">+1 (929) 269-3761</a><br><a href="mailto:info@janoons.com">info@janoons.com</a></dd></div>
    </dl>
  </aside>
</div></section>
{marquee()}
<section class="section"><div class="wrap">
  <div class="sec-head"><div class="rv"><p class="eyebrow">What we do</p><h2>Six services. One accountable partner.</h2></div><p class="rv" data-d="1">Everything your organization needs from IT &mdash; built, installed, migrated, and supported by the same team.</p></div>
  <div class="svc-grid">{svc_cards()}</div>
</div></section>
{gov_band()}
{QUOTE}
{cta()}'''

# ───────── SERVICES ─────────
DETAIL = [
 ("web","Web design &amp; software solution","A customized web design and proprietary software solution with updates and maintenance, including web graphic design and user interface (UI) design. A complete delivery of front-end and back-end solution with a mobile-friendly interface.",
  [("What we deliver",["Custom web design, updates, maintenance &amp; edits","Graphics and video editing","Dashboards, proprietary software, automation &amp; app development"])]),
 ("network","Desktop support &amp; network setup/support","Installation of workstations, servers, network switches, software, wireless setup, and firewalls to provide and support a fully functioning IT infrastructure. Any migration from an old to a new version comes with post-migration support.",
  [("What we deliver",["Hardware &amp; software installation (workstations, servers, switches, printers)","Windows, Microsoft Teams, Microsoft 365","Database migrations","Mobile setup &amp; support (Android/iPhone)"])]),
 ("data","Data management","We provide a data management solution for organizations to analyze data. We collect, organize, protect, and store data so clients can forecast with confidence.",
  [("What we deliver",["Customer Relationship Management (CRM)","Marketing technology","Data warehouse and analytics tools"])]),
 ("cloud","Cloud based services","A complete cloud set-up for your business to utilize application hosting, data hosting, website hosting, or application scaling, on the platform that fits your infrastructure.",
  [("Amazon AWS",["Elastic Compute Cloud (EC2)","Simple Storage Service (S3)","Elastic MapReduce","CloudFront","SimpleDB","Relational Database Service (RDS)"]),
   ("Microsoft Azure",["Azure development and app modernization","Azure migration service","Microsoft Cloud .NET development","Microsoft Azure consulting services"])]),
 ("citrix","Citrix","A software-as-a-service to securely deliver Windows applications and virtual desktops &mdash; a virtual computer with all the necessary resources delivered to users remotely, as a cost-effective business solution.",
  [("What we deliver",["Application virtualization &amp; VDI solution","Enterprise mobility management","NetScaler","Provisioning services, machine creation services","App layering, workspace environment management services"])]),
 ("staffing","Professional staffing","We provide our clients with suitable candidates best fit for the proposed position anywhere in the United States. Our staffing specialists have over five years of recruitment experience, focused on the industries below.",
  [("Industries",["Accounting &amp; Finance","Healthcare","Information Technology (IT)","Human Resources (HR)","Financial Services","Legal","Real Estate","Program/Project Management"])]),
]
toc = "".join(f'<a href="#{s}"><span class="n">0{i}</span>{n}</a>' for i,(s,n,_,_) in enumerate(DETAIL,1))
blocks=[]
for i,(s,n,d,groups) in enumerate(DETAIL,1):
    g = "".join(f"<h4>{t}</h4><ul>{''.join(f'<li>{x}</li>' for x in items)}</ul>" for t,items in groups)
    blocks.append(f'<article class="dsvc rv" id="{s}"><span class="n">0{i}</span><h2>{n}</h2><p>{d}</p>{g}</article>')
services = f'''<section class="page-head on-dark"><div class="wrap">
  <div><p class="eyebrow rv">What we do</p><h1 class="rv" data-d="1">Services</h1><p class="rv" data-d="2">Complete IT solutions, so you can focus on growing your business while we focus on your technology.</p></div>
  <div class="facts rv" data-d="3"><div><b>6</b><span>Service lines</span></div><div><b>1</b><span>Accountable team</span></div><div><b>US</b><span>Nationwide staffing</span></div></div>
</div></section>
<section class="section"><div class="wrap detail"><nav class="toc" aria-label="Services">{toc}</nav><div>{"".join(blocks)}</div></div></section>
{cta("Ready to start?","Tell us what you&rsquo;re working on and we&rsquo;ll match it to the right service above.")}'''

# ───────── GOVERNMENT ─────────
naics=[("541511","Custom computer programming services"),("541512","Computer software consulting services"),("541519","Disaster recovery services"),("561320","Contract staffing services"),("561330","Co-employment staffing"),("611420","Software application training"),("238210","Computer &amp; network installation, cabling, security systems")]
nigp=[("915-96","Web page design, management and maintenance services"),("915-76","Telephone services: installation, moves, changes, adds, programming, removal, training"),("918-30","Computer software consulting, mainframe &amp; mid-range services"),("918-32","Computer software consulting, PC/server"),("918-35","Computer system integration consulting"),("918-71","Management consulting"),("918-96","Telecommunication, networking"),("920-05","Application, infrastructure, hosting, and cloud computing services"),("920-27","E-commerce software development"),("920-31","Installation of computers, peripherals, and related equipment"),("920-46","Software updating services"),("920-66","System/network/database administration"),("920-91","Training, computer based"),("958-23","Computer management services")]
def table(rows, cap):
    r="".join(f'<tr><td class="code">{c}</td><td>{d}</td></tr>' for c,d in rows)
    return f'<table class="codes"><caption class="sr-only" style="position:absolute;left:-9999px">{cap}</caption><thead><tr><th>Code</th><th>Description</th></tr></thead><tbody>{r}</tbody></table>'
government = f'''<section class="page-head on-dark"><div class="wrap">
  <div><p class="eyebrow rv">Government contracts</p><h1 class="rv" data-d="1">Government projects</h1><p class="rv" data-d="2">Janoon Inc. is a Minority Business Enterprise certified by New York City, New York State, and the Port Authority of NY &amp; NJ, with extensive experience on public-sector projects.</p></div>
  <div class="facts rv" data-d="3"><div><b>3</b><span>MBE certifications</span></div><div><b>7</b><span>NAICS codes</span></div><div><b>14</b><span>NIGP codes</span></div></div>
</div></section>
<section class="section"><div class="wrap gov-body">
  <div class="side">
    <div class="card rv"><h3>Certifications</h3><ul><li>MBE &mdash; New York City</li><li>MBE &mdash; New York State</li><li>MBE &mdash; Port Authority of NY &amp; NJ</li></ul></div>
    <div class="card rv" data-d="1"><h3>Agency clients</h3><ul>{"".join(f"<li>{n}</li>" for n,_ in CLIENTS)}</ul></div>
    <div class="card rv" data-d="2"><h3>Procurement contact</h3><p style="margin:0 0 14px;font-size:15px;color:var(--ink-600)">Send your RFP or scope and we&rsquo;ll respond with certifications, references, and a point of contact.</p><a class="btn btn-primary" href="/contact.html" style="width:100%">Send an inquiry {ARR}</a></div>
  </div>
  <div><div class="rv"><h2>NAICS codes</h2>{table(naics,"NAICS codes")}</div><div class="rv"><h2>NIGP codes</h2>{table(nigp,"NIGP codes")}</div></div>
</div></section>'''

# ───────── CONTACT ─────────
contact = f'''<section class="page-head on-dark"><div class="wrap">
  <div><p class="eyebrow rv">Contact</p><h1 class="rv" data-d="1">Send your inquiry.</h1><p class="rv" data-d="2">We&rsquo;ll read it and get back to you &mdash; usually within one business day.</p></div>
</div></section>
<section class="section"><div class="wrap contact-grid">
  <div class="form-card rv">
    <div class="form-success" id="form-success" tabindex="-1"><h3 style="margin-bottom:8px">Thank you for contacting us.</h3><p style="margin:0">We have received your message and will be in touch soon.</p></div>
    <form id="contact-form" name="contact" method="POST" action="/thanks.html" data-netlify="true" netlify-honeypot="company" novalidate>
      <input type="hidden" name="form-name" value="contact">
      <p class="hp" aria-hidden="true"><label>Company <input name="company" tabindex="-1" autocomplete="off"></label></p>
      <div class="field"><label for="name">Name</label><input id="name" name="name" type="text" autocomplete="name" required><p class="help">Required.</p></div>
      <div class="field"><label for="email">E-mail</label><input id="email" name="email" type="email" autocomplete="email" required><p class="help">Required &mdash; we&rsquo;ll reply here.</p></div>
      <div class="field full"><label for="subject">Subject</label><input id="subject" name="subject" type="text" required><p class="help">Enter a subject so we can route your inquiry.</p></div>
      <div class="field full"><label for="message">Message</label><textarea id="message" name="message" rows="5" required></textarea><p class="help">Required.</p></div>
      <div class="full"><button class="btn btn-primary" type="submit">Send message {ARR}</button></div>
      <p class="full form-fail" id="form-fail" tabindex="-1" hidden>We couldn&rsquo;t send your message just now. Please try again, or e-mail <a href="mailto:info@janoons.com">info@janoons.com</a> or call <a href="tel:+19292693761">+1 (929) 269-3761</a>.</p>
    </form>
  </div>
  <dl class="details rv" data-d="1">
    <a class="card" href="tel:+19292693761"><span><small>Phone</small>+1 (929) 269-3761</span>{ARR}</a>
    <a class="card" href="mailto:info@janoons.com"><span><small>E-mail</small>info@janoons.com</span>{ARR}</a>
    <div class="card"><span><small>Office</small>New York, NY</span></div>
    <div class="card"><span><small>Certified</small>MBE &mdash; NYC, NYS, Port Authority of NY &amp; NJ</span></div>
  </dl>
</div></section>'''

thanks = f'''<section class="page-head on-dark"><div class="wrap"><div><p class="eyebrow">Contact</p><h1>Thank you for contacting us.</h1><p>We have received your message and will be in touch soon &mdash; usually within one business day. If it&rsquo;s urgent, call <a href="tel:+19292693761" style="color:#fff">+1 (929) 269-3761</a>.</p><div class="btn-row" style="margin-top:28px"><a class="btn btn-primary" href="/">Back to homepage {ARR}</a><a class="btn btn-secondary" href="/services.html">See our services</a></div></div></div></section>'''
notfound = f'''<section class="page-head on-dark"><div class="wrap"><div><p class="eyebrow">404</p><h1>That page doesn&rsquo;t exist.</h1><p>Try the homepage, or get in touch directly.</p><div class="btn-row" style="margin-top:28px"><a class="btn btn-primary" href="/">Go to homepage {ARR}</a><a class="btn btn-secondary" href="/contact.html">Contact us</a></div></div></div></section>'''

PAGES = {
 "index.html": page("Janoon Inc. — Complete IT Solutions, New York, NY","Janoon Inc. is an MBE-certified IT firm in New York providing web and software development, network support, data management, cloud, Citrix, and professional staffing.","/","/",home),
 "services.html": page("Services — Janoon Inc.","Web design and software, network and desktop support, data management, cloud services, Citrix, and professional staffing from Janoon Inc., New York, NY.","/services.html","/services.html",services),
 "government.html": page("Government Projects — Janoon Inc.","Janoon Inc. is a Minority Business Enterprise (MBE) certified by New York City, New York State, and the Port Authority of NY & NJ, with NAICS and NIGP codes on file.","/government.html","/government.html",government),
 "contact.html": page("Contact — Janoon Inc.","Send Janoon Inc. an inquiry: +1 (929) 269-3761, info@janoons.com. New York, NY.","/contact.html","/contact.html",contact),
 "thanks.html": page("Thank you — Janoon Inc.","Your inquiry has been received.","/thanks.html","",thanks,noindex=True),
 "404.html": page("Page not found — Janoon Inc.","This page could not be found.","/404.html","",notfound,noindex=True),
}
for name, html in PAGES.items():
    with open(os.path.join(OUT,name),"w") as f: f.write(html)
print("wrote", ", ".join(PAGES))

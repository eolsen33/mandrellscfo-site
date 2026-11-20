#!/usr/bin/env python3
"""Build services/<slug>.html, one page per homepage service.

Run from the repo root:  python3 tools/build_services.py
The shell (head, nav, contact band, footer) is taken from team/lisa.html so the
service pages stay in step with the rest of the site. Copy below is drawn from
what the homepage already says; keep it that way.
"""
import html, json, os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = "https://mandrellscfo.com"
WHO = ("We work with owner-operated, service-based businesses from start-up to $30M in revenue, "
       "particularly in the trades, where margins live in the details. Our team of ten works from "
       "235 South Main Street in Gainesville, Florida, and serves clients across the state.")

SERVICES = [
 dict(slug="fractional-cfo", name="Fractional CFO", h1=("Fractional", "CFO services."),
  title="Fractional CFO Services in Gainesville, FL | Mandrell's CFO",
  desc="Fractional CFO services from a family-owned accounting firm in Gainesville, FL: budgeting and forecasting, KPI dashboards, and quarterly strategic reviews.",
  lead="CFO-level leadership for your business, without a full-time CFO on payroll.",
  included=["Custom budgeting and forecasting", "Financial roadmaps", "Business KPI dashboards",
            "Department-level efficiency analysis", "Contract and banking negotiation",
            "Control reviews that catch leaks before they cost you"],
  how=["A typical engagement includes a quarterly strategic review with the CFO: a controls and risk check, a rolling 13-week cash forecast, and budget versus actual in plain language.",
       "Christina Mandrell, our CFO, brings more than 21 years of corporate accounting leadership. Because the same firm runs your day-to-day accounting, the strategic conversation starts from numbers we already know."]),
 dict(slug="bookkeeping-financial-reporting", name="Bookkeeping & Financial Reporting", h1=("Bookkeeping &", "financial reporting."),
  title="Bookkeeping & Financial Reporting, Gainesville | Mandrell's CFO",
  desc="Bookkeeping and financial reporting from an accounting firm in Gainesville, FL: reconciliations, AR, AP, general ledger, job costing, and a clean monthly close.",
  lead="Multiple service levels, from a monthly close to a full outsourced accounting department.",
  included=["Bank and credit-card reconciliations", "Accounts receivable", "Accounts payable",
            "General ledger", "Job costing", "Financial reporting you can read"],
  how=["Day to day and week to week we keep the flow of the business moving: AR billing and collections, AP entry, approvals and payments, deposits and classifications.",
       "Each month the picture comes into focus: bank and credit-card reconciliations, journal entries and accruals, and financial statements you can read. At year-end we package everything your CPA needs to file."]),
 dict(slug="payroll-processing", name="Payroll Processing", h1=("Payroll", "processing."),
  title="Payroll Processing in Gainesville, FL | Mandrell's CFO Services",
  desc="Payroll processing from an accounting firm in Gainesville, FL: timely, accurate pay, multi-state where required, tax deposits, returns, and garnishments.",
  lead="Timely, accurate pay. Your team gets paid; you get the records.",
  included=["Payroll runs on a set cadence", "Multi-state payroll where required", "Payroll tax deposits",
            "Payroll tax returns", "Specialized handling of garnishments", "1099 and W-2 reconciliation at year-end"],
  how=["Payroll runs on cadence alongside the rest of your weekly accounting, so pay, tax deposits and the general ledger stay in step with one another.",
       "Payroll tax returns are filed on schedule, and at year-end we reconcile 1099s and W-2s as part of the package we hand your CPA."]),
 dict(slug="human-resources", name="Human Resources", h1=("Human", "resources."),
  title="Human Resources Support in Gainesville, FL | Mandrell's CFO",
  desc="Human resources support from an accounting firm in Gainesville, FL: recruiting, onboarding, compliance, benefits administration, and staff development.",
  lead="The people side of the back office, handled by the same team that runs your books.",
  included=["Recruiting", "Onboarding", "Regulatory compliance", "Benefits administration",
            "Organizational culture", "Advising leadership on performance management and staff development"],
  how=["We handle recruiting, onboarding, regulatory compliance and benefits administration, and we advise leadership on performance management and staff development.",
       "Because HR sits next to payroll and accounting in one firm, a new hire, a benefits change or a pay adjustment is handled once and reflected everywhere it needs to be."]),
 dict(slug="controller-services-audits", name="Controller Services & Audits", h1=("Controller services", "& audits."),
  title="Controller Services & Audits in Gainesville, FL | Mandrell's CFO",
  desc="Controller services from an accounting firm in Gainesville, FL: dedicated oversight and periodic internal reviews of policies, procedures, and systems.",
  lead="Dedicated controller oversight, with periodic internal reviews against industry best practices.",
  included=["Dedicated controller oversight", "Internal reviews of policies, procedures and systems",
            "Approval processes and spending controls", "Segregation of duties", "Documentation standards",
            "Control changes that mitigate loss and reduce exposure"],
  how=["A controller reviews the work a clerk enters, which gives you multiple levels of oversight and real segregation of duties instead of concentrating financial access in one or two employees.",
       "Each quarter includes a controls and risk check. Where a review finds a gap, we recommend the control changes that reduce errors, leakage and fraud exposure."]),
 dict(slug="sales-payroll-tax", name="Sales & Payroll Tax", h1=("Sales &", "payroll tax."),
  title="Sales & Payroll Tax Filing in Gainesville, FL | Mandrell's CFO",
  desc="Sales, use, and payroll tax returns from an accounting firm in Gainesville, FL. Florida and multi-jurisdiction, filed accurately, on time, and audit-ready.",
  lead="Sales, use, and payroll tax returns: submitted accurately, on time, and audit-ready.",
  included=["Sales tax returns", "Use tax returns", "Payroll tax returns",
            "Monthly, quarterly, annual or semi-weekly filing", "Florida and multi-jurisdiction",
            "Records kept audit-ready"],
  how=["Sales tax preparation and filing is part of the monthly close, so the return is built from books that have already been reconciled.",
       "We file on whatever schedule your business is on, whether monthly, quarterly, annual or semi-weekly, in Florida and across multiple jurisdictions."]),
 dict(slug="cash-flow-forecasting", name="Cash Flow Forecasting", h1=("Cash flow", "forecasting."),
  title="Cash Flow Forecasting in Gainesville, FL | Mandrell's CFO",
  desc="Cash flow forecasting from an accounting firm in Gainesville, FL: rolling forecasts, budget creation, collection-cycle analysis, and vendor payment timing.",
  lead="Rolling forecasts and close monitoring, so cash works for you, not against you.",
  included=["Rolling cash flow forecasts", "Budget creation", "Financial monitoring",
            "Collection-cycle analysis", "Vendor payment timing", "A rolling 13-week cash forecast each quarter"],
  how=["We monitor cash requirements, anticipated shortages, working capital needs and future cash positions, so a tight month is something you see coming.",
       "We also look at the timing behind the numbers: receivables, payables, purchasing, billing and collections, and everything else that moves cash."]),
 dict(slug="staff-training-development", name="Staff Training & Development", h1=("Staff training", "& development."),
  title="Accounting Staff Training in Gainesville, FL | Mandrell's CFO",
  desc="Accounting and HR training for your in-house team from a family-owned accounting firm in Gainesville, FL. Internal advancement, not dependence.",
  lead="Comprehensive training in accounting and HR for your in-house team. Internal advancement, not dependence.",
  included=["Accounting training for in-house staff", "HR training for in-house staff",
            "Oversight of your existing personnel", "Support that supplements your team",
            "Processes and procedures your staff can run", "A plan for internal advancement"],
  how=["Rather than simply replacing an internal accounting department, we can manage, supplement, train and provide oversight to your existing personnel.",
       "The goal is a team that can stand on its own. We leave you stronger than we found you."]),
]

FOOT = {"Fractional CFO": "fractional-cfo", "Bookkeeping": "bookkeeping-financial-reporting",
        "Payroll": "payroll-processing", "Human Resources": "human-resources",
        "Audits & Controls": "controller-services-audits", "Audits &amp; Controls": "controller-services-audits",
        "Sales Tax": "sales-payroll-tax"}


def footer_links(doc, prefix):
    def rep(m):
        slug = FOOT.get(m.group(2))
        return f'<li><a href="{prefix}{slug}.html">{m.group(2)}</a></li>' if slug else m.group(0)
    return re.sub(r'<li><a href="([^"]*#services|[^"]*services/[a-z-]+\.html|[a-z-]+\.html)">([^<]+)</a></li>', rep, doc)


def build():
    shell = open(os.path.join(ROOT, "team", "lisa.html"), encoding="utf-8").read()
    head_end = shell.index("</head>")
    main_a = shell.index('<section class="section bio-top">')
    main_b = shell.index('<section class="cta-band">')
    for s in SERVICES:
        assert 30 <= len(s["title"]) <= 65, (s["slug"], "title", len(s["title"]))
        assert 70 <= len(s["desc"]) <= 160, (s["slug"], "desc", len(s["desc"]))
    for i, s in enumerate(SERVICES):
        url = f"{SITE}/services/{s['slug']}.html"
        e = html.escape
        head = shell[:head_end]
        head = re.sub(r"<title>.*?</title>", f"<title>{e(s['title'], quote=False)}</title>", head, flags=re.S)
        head = re.sub(r'<meta name="description" content="[^"]*" />', f'<meta name="description" content="{e(s["desc"])}" />', head)
        head = re.sub(r'(<link rel="canonical" href=")[^"]*', r"\g<1>" + url, head)
        head = re.sub(r'(<meta property="og:url" content=")[^"]*', r"\g<1>" + url, head)
        for k, v in (("og:title", s["title"]), ("og:description", s["desc"]), ("twitter:title", s["title"]), ("twitter:description", s["desc"])):
            attr = "property" if k.startswith("og") else "name"
            head = re.sub(rf'(<meta {attr}="{k}" content=")[^"]*', lambda m, v=v: m.group(1) + e(v), head)
        ld = [{"@context": "https://schema.org", "@type": "Service", "name": s["name"], "serviceType": s["name"],
               "description": s["desc"], "url": url,
               "provider": {"@type": "AccountingService", "name": "Mandrell's CFO Services", "url": SITE + "/",
                            "telephone": "+1-352-248-0518",
                            "address": {"@type": "PostalAddress", "streetAddress": "235 South Main St, Suite W201",
                                        "addressLocality": "Gainesville", "addressRegion": "FL", "postalCode": "32601",
                                        "addressCountry": "US"}},
               "areaServed": [{"@type": "City", "name": "Gainesville"}, {"@type": "State", "name": "Florida"}]},
              {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
                  {"@type": "ListItem", "position": 1, "name": "Home", "item": SITE + "/"},
                  {"@type": "ListItem", "position": 2, "name": "Services", "item": SITE + "/#services"},
                  {"@type": "ListItem", "position": 3, "name": s["name"], "item": url}]}]
        head += '<script type="application/ld+json">\n' + json.dumps(ld, indent=1, ensure_ascii=False) + "\n</script>\n"
        prev, nxt = SERVICES[i - 1], SERVICES[(i + 1) % len(SERVICES)]
        inc = "\n".join(f"          <li>{e(x, quote=False)}</li>" for x in s["included"])
        how = "\n".join(f"        <p>{e(x, quote=False)}</p>" for x in s["how"])
        main = f'''<section class="section bio-top svc-page">
  <div class="wrap">
    <a href="../index.html#services" class="back-link">← All services</a>

    <div class="svc-eyebrow">Service {i + 1:02d} of {len(SERVICES):02d} · Accounting firm in Gainesville, Florida</div>
    <h1 class="bio-name reveal">{e(s["h1"][0], quote=False)}<br/><em>{e(s["h1"][1], quote=False)}</em></h1>
    <p class="svc-lead reveal">{e(s["lead"], quote=False)}</p>

    <div class="svc-grid">
      <div class="svc-main reveal">
        <h2 class="svc-h">How it works</h2>
{how}
        <h2 class="svc-h">Who it's for</h2>
        <p>{e(WHO, quote=False)}</p>
      </div>
      <aside class="svc-aside reveal" aria-label="What's included">
        <h2 class="svc-h">What's included</h2>
        <ul>
{inc}
        </ul>
        <a class="btn btn-primary" href="../intake.html">Request an intake <span class="arrow">→</span></a>
      </aside>
    </div>

    <div class="bio-next">
      <a href="{prev['slug']}.html">← Previous · <span class="next-name">{e(prev['name'], quote=False)}</span></a>
      <a href="{nxt['slug']}.html">Next · <span class="next-name">{e(nxt['name'], quote=False)}</span> →</a>
    </div>
  </div>
</section>

'''
        doc = head + shell[head_end:main_a] + main + shell[main_b:]
        doc = footer_links(doc, "")
        open(os.path.join(ROOT, "services", s["slug"] + ".html"), "w", encoding="utf-8").write(doc)
        print("built services/" + s["slug"] + ".html")


if __name__ == "__main__":
    build()

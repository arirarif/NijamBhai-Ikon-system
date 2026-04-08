import os
BASE = r'c:\Users\arira\Desktop\NijamVhai\mockups\v2'

SIDEBAR = open(os.path.join(BASE,'_write_01_02.py')).read().split('SIDEBAR = """')[1].split('"""')[0]

def sidebar(active):
    keys = dict(d='',c='',o='',n='',s='',p='',l='',ch='')
    keys[active] = 'active'
    return SIDEBAR.format(**keys)

# ─── 07 LC TRACKER ───────────────────────────────────────────────────────
lc_tracker = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>LC Tracker — IKON GAS</title>
<link rel="stylesheet" href="_shared.css">
</head>
<body>
""" + sidebar('l') + """
<div id="main">
  <div id="topbar">
    <div class="topbar-title">LC Tracker</div>
    <div class="topbar-sep"></div>
    <div class="topbar-sub">Letter of Credit &amp; Payment Tracking</div>
    <div class="topbar-right">
      <button class="btn btn-primary btn-sm">+ Register LC</button>
    </div>
  </div>
  <div id="content">

    <!-- LC Summary KPIs -->
    <div class="kpi-row" style="display:grid;grid-template-columns:repeat(4,1fr);gap:12px;margin-bottom:20px">
      <div class="stat-card">
        <div class="sc-top"><div class="sc-label">Active LCs</div><div class="sc-icon" style="background:var(--accent-bg);color:var(--accent)">&#9965;</div></div>
        <div class="sc-value">4</div>
        <div class="sc-trend up">&#8593; 1 new this month</div>
      </div>
      <div class="stat-card">
        <div class="sc-top"><div class="sc-label">Total LC Value</div><div class="sc-icon" style="background:var(--green-bg);color:var(--green)">&#2547;</div></div>
        <div class="sc-value" style="font-size:18px">&#2547; 34,20,000</div>
        <div class="sc-trend up">across 4 LCs</div>
      </div>
      <div class="stat-card">
        <div class="sc-top"><div class="sc-label">Maturing in &lt;30 days</div><div class="sc-icon" style="background:var(--orange-bg);color:var(--orange)">&#8987;</div></div>
        <div class="sc-value" style="color:var(--orange)">2</div>
        <div class="sc-trend down">&#9888; Action needed</div>
      </div>
      <div class="stat-card">
        <div class="sc-top"><div class="sc-label">Matured (Paid)</div><div class="sc-icon" style="background:var(--green-bg);color:var(--green)">&#10003;</div></div>
        <div class="sc-value">7</div>
        <div class="sc-trend up">this fiscal year</div>
      </div>
    </div>

    <!-- LC LIST -->
    <div class="card" style="margin-bottom:20px">
      <div class="card-header">
        <span class="ctitle">All LC Records</span>
        <div style="display:flex;gap:8px">
          <input class="form-input" style="width:220px;height:30px;font-size:12px" placeholder="Search LC number or company...">
          <select class="form-select" style="width:140px;height:30px;font-size:12px">
            <option>All Status</option>
            <option>Docs Pending</option>
            <option>Docs Submitted</option>
            <option>Maturing Soon</option>
            <option>Matured / Paid</option>
          </select>
        </div>
      </div>
      <div class="card-body" style="padding:0">
        <table class="data-table">
          <thead>
            <tr><th>LC Number</th><th>PI Ref</th><th>Company</th><th>LC Value</th><th>Issue Date</th><th>Maturity Date</th><th>Days Left</th><th>Status</th><th></th></tr>
          </thead>
          <tbody>
            <tr>
              <td><span class="mono" style="color:var(--accent)">LC-2026-009</span></td>
              <td><span class="mono">PI-2026/05</span></td>
              <td>Bay Group</td>
              <td style="color:var(--green);font-weight:600">&#2547; 2,10,000</td>
              <td>8 Apr 2026</td>
              <td style="color:var(--text2)">7 Jul 2026</td>
              <td><span class="badge approved" style="font-size:10px">90 days</span></td>
              <td><span class="badge waiting">Docs Pending</span></td>
              <td><button class="btn btn-ghost btn-xs">View</button></td>
            </tr>
            <tr>
              <td><span class="mono" style="color:var(--accent)">LC-2026-008</span></td>
              <td><span class="mono">PI-2026/04</span></td>
              <td>KDS Accessories</td>
              <td style="color:var(--green);font-weight:600">&#2547; 88,500</td>
              <td>2 Apr 2026</td>
              <td style="color:var(--orange)">1 Jul 2026</td>
              <td><span class="badge at-risk" style="font-size:10px">84 days</span></td>
              <td><span class="badge approved">Docs Submitted</span></td>
              <td><button class="btn btn-ghost btn-xs">View</button></td>
            </tr>
            <tr>
              <td><span class="mono" style="color:var(--accent)">LC-2026-005</span></td>
              <td><span class="mono">PI-2026/03</span></td>
              <td>Noman Group</td>
              <td style="color:var(--green);font-weight:600">&#2547; 3,40,000</td>
              <td>20 Mar 2026</td>
              <td style="color:var(--red)">18 Jun 2026</td>
              <td><span class="badge urgent" style="font-size:10px">71 days</span></td>
              <td><span class="badge approved">Docs Submitted</span></td>
              <td><button class="btn btn-ghost btn-xs">View</button></td>
            </tr>
            <tr>
              <td><span class="mono" style="color:var(--accent)">LC-2026-001</span></td>
              <td><span class="mono">PI-2025/12</span></td>
              <td>Grameen Check</td>
              <td style="color:var(--green);font-weight:600">&#2547; 1,80,000</td>
              <td>12 Jan 2026</td>
              <td style="color:var(--text3)">12 Apr 2026</td>
              <td><span class="badge approved" style="font-size:10px;background:var(--green-bg);border-color:var(--green-border);color:var(--green)">Matured</span></td>
              <td><span class="badge approved">Paid</span></td>
              <td><button class="btn btn-ghost btn-xs">View</button></td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- LC DETAIL: LC-2026-009 -->
    <div style="font-size:11px;color:var(--text3);margin-bottom:10px">Showing detail for <strong style="color:var(--text2)">LC-2026-009</strong> &mdash; Bay Group</div>
    <div class="two-col">
      <div>
        <div class="card">
          <div class="card-header">
            <span class="ctitle">LC Details — LC-2026-009</span>
            <span class="badge waiting">Docs Pending</span>
          </div>
          <div class="card-body">
            <div class="info-grid info-grid-wide">
              <div class="info-item"><div class="label">LC Number</div><div class="value mono" style="color:var(--accent)">LC-2026-009</div></div>
              <div class="info-item"><div class="label">PI Reference</div><div class="value mono">PI-2026/05</div></div>
              <div class="info-item"><div class="label">Buyer Company</div><div class="value">Bay Group</div></div>
              <div class="info-item"><div class="label">LC Value</div><div class="value" style="color:var(--green)">&#2547; 2,10,000</div></div>
              <div class="info-item"><div class="label">Issuing Bank</div><div class="value">Islami Bank Bangladesh, Mirpur</div></div>
              <div class="info-item"><div class="label">Our Bank</div><div class="value">Community Bank Ltd, Uttara</div></div>
              <div class="info-item"><div class="label">Swift Code</div><div class="value mono">COYMBDDD</div></div>
              <div class="info-item"><div class="label">A/C Number</div><div class="value mono">0100310654101</div></div>
              <div class="info-item"><div class="label">LC Issue Date</div><div class="value">8 Apr 2026</div></div>
              <div class="info-item"><div class="label">Maturity Date</div><div class="value" style="color:var(--text2)">7 Jul 2026</div></div>
              <div class="info-item"><div class="label">Payment Terms</div><div class="value">90 days at sight</div></div>
              <div class="info-item"><div class="label">Country of Origin</div><div class="value">Bangladesh</div></div>
            </div>
          </div>
        </div>

        <!-- Amendments -->
        <div class="card" style="margin-top:16px">
          <div class="card-header">
            <span class="ctitle">LC Amendments</span>
            <button class="btn btn-outline btn-xs">+ Add Amendment</button>
          </div>
          <div class="card-body">
            <div style="font-size:12px;color:var(--text3);padding:16px 0">No amendments recorded for this LC.</div>
            <div style="font-size:11px;color:var(--text3)">Amendments occur when buyer requests changes to LC terms (value, date, description). Track each one here with date and reason.</div>
          </div>
        </div>
      </div>

      <!-- Right: doc checklist + countdown -->
      <div>
        <div class="card">
          <div class="card-header"><span class="ctitle">Maturity Countdown</span></div>
          <div class="card-body">
            <div class="maturity-countdown mc-90">
              <div class="mc-days">90</div>
              <div class="mc-label">days until maturity</div>
              <div class="mc-date">7 Jul 2026</div>
              <div class="mc-sub">Issue date: 8 Apr 2026</div>
            </div>
            <div style="margin-top:14px">
              <div style="height:8px;background:var(--bg4);border-radius:4px;overflow:hidden">
                <div style="width:0%;height:100%;background:var(--green);border-radius:4px;transition:width .3s"></div>
              </div>
              <div style="display:flex;justify-content:space-between;margin-top:4px;font-size:10px;color:var(--text3)">
                <span>0 days elapsed</span><span>90 days total</span>
              </div>
            </div>
          </div>
        </div>

        <div class="card" style="margin-top:16px">
          <div class="card-header">
            <span class="ctitle">Document Checklist</span>
            <span class="badge correction" style="font-size:10px">5 of 10 done</span>
          </div>
          <div class="card-body" style="display:flex;flex-direction:column;gap:6px">
            <div class="chk done"><div class="chk-icon">&#10003;</div><div><div class="chk-title">Commercial Invoice / PI</div><div class="chk-sub">PI-2026/05 &middot; uploaded</div></div></div>
            <div class="chk done"><div class="chk-icon">&#10003;</div><div><div class="chk-title">Packing List</div><div class="chk-sub">Signed &amp; uploaded</div></div></div>
            <div class="chk done"><div class="chk-icon">&#10003;</div><div><div class="chk-title">Delivery Challan</div><div class="chk-sub">DC-2026-041 &middot; uploaded</div></div></div>
            <div class="chk done"><div class="chk-icon">&#10003;</div><div><div class="chk-title">Sample Approval Record</div><div class="chk-sub">R1 approved</div></div></div>
            <div class="chk done"><div class="chk-icon">&#10003;</div><div><div class="chk-title">Insurance Certificate</div><div class="chk-sub">Uploaded</div></div></div>
            <div class="chk warn"><div class="chk-icon">!</div><div><div class="chk-title">Bill of Lading</div><div class="chk-sub">Pending from freight agent</div></div></div>
            <div class="chk err"><div class="chk-icon">&#10007;</div><div><div class="chk-title">Certificate of Origin</div><div class="chk-sub">Not submitted — required for Bangladesh export</div></div></div>
            <div class="chk err"><div class="chk-icon">&#10007;</div><div><div class="chk-title">Beneficiary's Certificate</div><div class="chk-sub">Not yet prepared</div></div></div>
            <div class="chk err"><div class="chk-icon">&#10007;</div><div><div class="chk-title">Inspection Certificate</div><div class="chk-sub">Awaiting 3rd-party QC agency</div></div></div>
            <div class="chk err"><div class="chk-icon">&#10007;</div><div><div class="chk-title">Bank Forwarding Letter</div><div class="chk-sub">Not submitted to Community Bank</div></div></div>
          </div>
        </div>
      </div>
    </div>

  </div>
</div>
</body></html>"""

# ─── 08 CHALLAN ──────────────────────────────────────────────────────────
challan = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>Delivery Challan — IKON GAS</title>
<link rel="stylesheet" href="_shared.css">
</head>
<body>
""" + sidebar('ch') + """
<div id="main">
  <div id="topbar">
    <div class="topbar-title">Delivery Challan</div>
    <div class="topbar-sep"></div>
    <div class="topbar-sub">Issue &amp; track delivery challans</div>
    <div class="topbar-right">
      <button class="btn btn-primary btn-sm">+ Issue Challan</button>
    </div>
  </div>
  <div id="content">

    <!-- Challan LIST -->
    <div class="card" style="margin-bottom:20px">
      <div class="card-header">
        <span class="ctitle">All Delivery Challans</span>
        <div style="display:flex;gap:8px">
          <input class="form-input" style="width:220px;height:30px;font-size:12px" placeholder="Search challan or order ref...">
          <select class="form-select" style="width:130px;height:30px;font-size:12px">
            <option>All Status</option>
            <option>Issued</option>
            <option>Delivered</option>
            <option>Returned</option>
          </select>
        </div>
      </div>
      <div class="card-body" style="padding:0">
        <table class="data-table">
          <thead>
            <tr><th>Challan No.</th><th>Order Ref</th><th>Company</th><th>Items / Qty</th><th>Delivery Date</th><th>Vehicle</th><th>Status</th><th>Linked PI</th><th></th></tr>
          </thead>
          <tbody>
            <tr>
              <td><span class="mono" style="color:var(--accent)">DC-2026-041</span></td>
              <td><span class="mono">BG-2026-041</span></td>
              <td>Bay Group</td>
              <td>Button &middot; 1,50,000 pcs</td>
              <td>7 Apr 2026</td>
              <td>Dhaka Metro GA-7711</td>
              <td><span class="badge approved">Delivered</span></td>
              <td><span class="mono" style="color:var(--accent)">PI-2026/05</span></td>
              <td><button class="btn btn-ghost btn-xs">View</button></td>
            </tr>
            <tr>
              <td><span class="mono" style="color:var(--accent)">DC-2026-039</span></td>
              <td><span class="mono">KD-2026-039</span></td>
              <td>KDS Accessories</td>
              <td>Zipper Pull &middot; 80,000 pcs</td>
              <td>1 Apr 2026</td>
              <td>Hired Van</td>
              <td><span class="badge approved">Delivered</span></td>
              <td><span class="mono" style="color:var(--accent)">PI-2026/04</span></td>
              <td><button class="btn btn-ghost btn-xs">View</button></td>
            </tr>
            <tr>
              <td><span class="mono" style="color:var(--accent)">DC-2026-033</span></td>
              <td><span class="mono">NM-2026-033</span></td>
              <td>Noman Group</td>
              <td>Button &middot; 2,00,000 pcs</td>
              <td>9 Apr 2026</td>
              <td>Dhaka Metro GA-1234</td>
              <td><span class="badge at-risk">Scheduled</span></td>
              <td><span class="mono" style="color:var(--accent)">PI-2026/03</span></td>
              <td><button class="btn btn-ghost btn-xs">View</button></td>
            </tr>
            <tr>
              <td><span class="mono" style="color:var(--accent)">DC-2026-012</span></td>
              <td><span class="mono">GC-2025-088</span></td>
              <td>Grameen Check</td>
              <td>Woven Label &middot; 50,000 pcs</td>
              <td>10 Jan 2026</td>
              <td>Sundarban Courier</td>
              <td><span class="badge approved">Delivered</span></td>
              <td><span class="mono" style="color:var(--text3)">PI-2025/12</span></td>
              <td><button class="btn btn-ghost btn-xs">View</button></td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- CHALLAN PRINT PREVIEW -->
    <div style="font-size:11px;color:var(--text3);margin-bottom:10px;text-align:right">
      Print preview: DC-2026-041 &mdash; <button class="btn btn-ghost btn-xs" onclick="window.print()">&#128424; Print</button>
    </div>
    <div class="pi-doc">
      <div class="pi-header">
        <div class="pi-brand">
          <div class="pi-company">IKON GARMENTS ACCESSORIES</div>
          <div style="font-size:13px;font-weight:700;color:#222;margin-top:4px">DELIVERY CHALLAN</div>
          <div class="pi-addr">House 18, Road 10, Sector 09, Uttara, Dhaka-1230, Bangladesh</div>
          <div class="pi-addr">Tel: +8801730214607 &nbsp;|&nbsp; Email: ikongas@gmail.com</div>
        </div>
        <div class="pi-meta">
          <div class="pi-num">DC-2026-041</div>
          <div style="font-size:11px;margin-top:6px"><strong>Date:</strong> 7 April 2026</div>
          <div style="font-size:11px"><strong>Order Ref:</strong> BG-2026-041</div>
          <div style="font-size:11px"><strong>PI Ref:</strong> PI-2026/05</div>
        </div>
      </div>
      <div class="pi-parties">
        <div class="pi-buyer">
          <div class="pi-blabel">DELIVER TO</div>
          <div class="pi-bname">Bay Group</div>
          <div class="pi-baddr">Plot 45, Block A, Ashulia, Savar, Dhaka</div>
          <div class="pi-baddr">Attn: Rashida Begum — Senior Merchandiser</div>
          <div class="pi-baddr">Tel: +88 01812-445566</div>
        </div>
        <div class="pi-buyer">
          <div class="pi-blabel">TRANSPORT DETAILS</div>
          <div class="pi-baddr"><strong>Vehicle No:</strong> Dhaka Metro GA-7711</div>
          <div class="pi-baddr"><strong>Driver:</strong> Md. Karim, +88 01911-223344</div>
          <div class="pi-baddr"><strong>Dispatch Time:</strong> 7 Apr 2026, 9:00 AM</div>
          <div class="pi-baddr"><strong>Route:</strong> Uttara &rarr; Ashulia</div>
        </div>
      </div>
      <table class="pi-table">
        <thead>
          <tr><th>SL</th><th>Description of Goods</th><th>Style / Ref</th><th>Carton</th><th>Qty (pcs)</th><th>Unit</th><th>Remarks</th></tr>
        </thead>
        <tbody>
          <tr>
            <td>01</td>
            <td>4-Hole Polyester Button, 18L, Black<br><small>Pantone 19-0303 TPX</small></td>
            <td class="mono">MT-301</td>
            <td>15 ctns</td>
            <td style="text-align:right;font-weight:600">1,50,000</td>
            <td>pcs</td>
            <td>&#10003; Approved sample</td>
          </tr>
        </tbody>
        <tfoot>
          <tr class="pi-total-row">
            <td colspan="4" style="text-align:right;font-weight:700;padding:8px 12px">Total Cartons: 15</td>
            <td style="text-align:right;font-weight:800;padding:8px 12px">1,50,000</td>
            <td colspan="2" style="padding:8px 12px">pcs</td>
          </tr>
        </tfoot>
      </table>
      <div class="pi-words">Goods dispatched in good condition. Buyer to verify on receipt.</div>
      <div class="pi-terms">
        <div class="pi-terms-title">Delivery Terms</div>
        <ol>
          <li>Buyer must inspect goods within 24 hours of delivery and report any discrepancy.</li>
          <li>No return accepted after 3 days unless quality issue proven with documentation.</li>
          <li>Carton count verified by driver before dispatch.</li>
        </ol>
      </div>
      <div class="pi-sign">
        <div class="pi-sign-box">
          <div class="pi-sign-line"></div>
          <div class="pi-sign-name">Dispatched By</div>
          <div class="pi-sign-role">IKON Garments Accessories</div>
        </div>
        <div class="pi-sign-box">
          <div class="pi-sign-line"></div>
          <div class="pi-sign-name">Driver Signature</div>
          <div class="pi-sign-role">Vehicle: GA-7711</div>
        </div>
        <div class="pi-sign-box">
          <div class="pi-sign-line"></div>
          <div class="pi-sign-name">Received By</div>
          <div class="pi-sign-role">Bay Group — Signature &amp; Stamp</div>
        </div>
      </div>
    </div>
  </div>
</div>
</body></html>"""

files = {
    '07-lc-tracker.html': lc_tracker,
    '08-challan.html': challan,
}

for fname, content in files.items():
    path = os.path.join(BASE, fname)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f'Written: {fname}')

print('DONE batch 4')

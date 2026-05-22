import os
BASE = r'c:\Users\arira\Desktop\NijamVhai\mockups\v2'

SIDEBAR = open(os.path.join(BASE,'_write_01_02.py')).read().split('SIDEBAR = """')[1].split('"""')[0]

def sidebar(active):
    keys = dict(d='',c='',o='',n='',s='',p='',l='',ch='')
    keys[active] = 'active'
    return SIDEBAR.format(**keys)

# ─── 05 SAMPLE REVISION ──────────────────────────────────────────────────
sample_revision = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>Sample &amp; Revisions — IKON GAS</title>
<link rel="stylesheet" href="_shared.css">
</head>
<body>
""" + sidebar('s') + """
<div id="main">
  <div id="topbar">
    <div class="topbar-title">Sample &amp; Revisions</div>
    <div class="topbar-sep"></div>
    <div class="topbar-sub">F-2026-038 &mdash; Button &mdash; Noman Group</div>
    <div class="topbar-right">
      <button class="btn btn-green btn-sm">Mark Sample Approved</button>
      <button class="btn btn-primary btn-sm">+ Log New Revision</button>
    </div>
  </div>
  <div id="content">

    <div class="breadcrumb">
      <a href="01-dashboard.html">Dashboard</a><span class="sep">/</span>
      <a href="03-order-detail.html">F-2026-038</a><span class="sep">/</span>
      <span class="current">Sample Revisions</span>
    </div>

    <!-- Context bar -->
    <div class="ctx-bar">
      <div class="ctx-items">
        <div class="ctx-item"><span class="ctx-label">Order</span><span class="ctx-val" style="color:var(--accent)">F-2026-038</span></div>
        <div class="ctx-sep">&middot;</div>
        <div class="ctx-item"><span class="ctx-label">Product</span><span class="ctx-val">Button (18L, Polyester, Black)</span></div>
        <div class="ctx-sep">&middot;</div>
        <div class="ctx-item"><span class="ctx-label">Company</span><span class="ctx-val">Noman Group</span></div>
        <div class="ctx-sep">&middot;</div>
        <div class="ctx-item"><span class="ctx-label">Merchandiser</span><span class="ctx-val">Faruq Hossain</span></div>
        <div class="ctx-sep">&middot;</div>
        <div class="ctx-item"><span class="ctx-label">Stage</span><span class="badge correction" style="font-size:10px">Correction Needed</span></div>
        <div class="ctx-sep">&middot;</div>
        <div class="ctx-item"><span class="ctx-label">Total Revisions</span><span class="ctx-val" style="color:var(--red)">2 rounds done &mdash; 1 pending</span></div>
      </div>
    </div>

    <!-- Revision stage bar -->
    <div class="stage-wrap">
      <div class="stage-bar">
        <div class="stage done"><span class="snum">R1</span>Sent &amp; Corrected</div>
        <div class="stage current"><span class="snum">R2</span>Sent &mdash; Awaiting Reply</div>
        <div class="stage"><span class="snum">?</span>Next Round</div>
        <div class="stage"><span class="snum">&#10003;</span>Approved</div>
      </div>
    </div>

    <div class="two-col">
      <div>

        <!-- R1 -->
        <div class="revision-item">
          <div class="revision-header">
            <span class="rno">R1 &mdash; Revision 1</span>
            <span class="badge correction" style="margin-left:auto;font-size:10px">Correction</span>
            <span style="font-size:11px;color:var(--text3);margin-left:10px">5 Apr 2026</span>
          </div>
          <div class="revision-body">
            <div class="rev-grid">
              <div class="rev-item"><div class="rlabel">Source</div><div class="rvalue">In-house (IKON)</div></div>
              <div class="rev-item"><div class="rlabel">Sample Made</div><div class="rvalue">5 Apr 2026</div></div>
              <div class="rev-item"><div class="rlabel">Sent to Buyer</div><div class="rvalue">6 Apr 2026</div></div>
              <div class="rev-item"><div class="rlabel">Cost</div><div class="rvalue">&#2547; 0 (in-house)</div></div>
              <div class="rev-item"><div class="rlabel">Result</div><div class="rvalue" style="color:var(--red)">Correction Required</div></div>
              <div class="rev-item"><div class="rlabel">Turn-around</div><div class="rvalue">1 day</div></div>
            </div>
            <div class="feedback-box">
              <div class="flabel">Buyer Feedback (from Faruq Hossain)</div>
              <div class="ftext">"Button diameter is 14L but we need 18L exactly. Please re-make and match Pantone 19-0303. Also check the hole spacing — too narrow. Resubmit ASAP as production deadline is 25 Apr."</div>
            </div>
            <div style="margin-top:12px">
              <div class="rlabel" style="margin-bottom:6px">Quality Checklist — R1</div>
              <div style="display:flex;gap:8px;flex-wrap:wrap">
                <span class="badge waiting" style="font-size:10px">&#10007; Size (14L vs 18L)</span>
                <span class="badge waiting" style="font-size:10px">&#10007; Hole Spacing</span>
                <span class="badge approved" style="font-size:10px">&#10003; Material (Polyester)</span>
                <span class="badge approved" style="font-size:10px">&#10003; Attachment Type (Flat)</span>
                <span class="badge correction" style="font-size:10px">~ Color (close, not exact)</span>
              </div>
            </div>
          </div>
        </div>

        <!-- R2 -->
        <div class="revision-item active-rev">
          <div class="revision-header">
            <span class="rno">R2 &mdash; Revision 2 (Current)</span>
            <span class="badge at-risk" style="margin-left:auto;font-size:10px">Awaiting Reply</span>
            <span style="font-size:11px;color:var(--text3);margin-left:10px">7 Apr 2026</span>
          </div>
          <div class="revision-body">
            <div class="rev-grid">
              <div class="rev-item"><div class="rlabel">Source</div><div class="rvalue">Outsourced &mdash; Mirpur</div></div>
              <div class="rev-item"><div class="rlabel">Vendor</div><div class="rvalue">Al-Amin Button, Mirpur-10</div></div>
              <div class="rev-item"><div class="rlabel">Sample Made</div><div class="rvalue">7 Apr 2026</div></div>
              <div class="rev-item"><div class="rlabel">Sent to Buyer</div><div class="rvalue">8 Apr 2026</div></div>
              <div class="rev-item"><div class="rlabel">Cost</div><div class="rvalue" style="color:var(--orange)">&#2547; 1,200</div></div>
              <div class="rev-item"><div class="rlabel">Courier</div><div class="rvalue">Sundarban Courier</div></div>
            </div>
            <div class="feedback-box internal">
              <div class="flabel">Internal Note</div>
              <div class="ftext">18L corrected. Hole spacing now 1.2mm as spec. Pantone 19-0303 — color match looks correct under daylight. Sent via Sundarban courier to Faruq bhai's office, Mirpur. Tracking: SD-2026-04489. Waiting callback by 10 Apr.</div>
            </div>
            <div style="margin-top:12px">
              <div class="rlabel" style="margin-bottom:6px">Quality Checklist — R2</div>
              <div style="display:flex;gap:8px;flex-wrap:wrap">
                <span class="badge approved" style="font-size:10px">&#10003; Size (18L)</span>
                <span class="badge approved" style="font-size:10px">&#10003; Hole Spacing (1.2mm)</span>
                <span class="badge approved" style="font-size:10px">&#10003; Material (Polyester)</span>
                <span class="badge approved" style="font-size:10px">&#10003; Attachment Type</span>
                <span class="badge approved" style="font-size:10px">&#10003; Color Match</span>
              </div>
            </div>
            <div class="rev-actions" style="margin-top:14px">
              <button class="btn btn-green">&#10003; Mark Approved &rarr; Start Bulk</button>
              <button class="btn btn-red btn-sm">Log Another Correction</button>
              <button class="btn btn-ghost btn-sm">Edit this revision</button>
            </div>
          </div>
        </div>

        <!-- Log new revision form -->
        <div class="card" style="margin-top:4px">
          <div class="card-header"><span class="ctitle">Log New Revision (R3)</span></div>
          <div class="card-body">
            <div class="form-row">
              <div class="form-group">
                <label class="form-label">Result <span class="req">*</span></label>
                <div class="radio-cards" style="grid-template-columns:1fr 1fr">
                  <label class="radio-card selected">
                    <input type="radio" name="rev_result" value="correction" checked>
                    <div class="rc-title" style="color:var(--orange)">Correction</div>
                    <div class="rc-sub">Buyer needs changes</div>
                  </label>
                  <label class="radio-card">
                    <input type="radio" name="rev_result" value="approved">
                    <div class="rc-title" style="color:var(--green)">Approved</div>
                    <div class="rc-sub">Sample accepted</div>
                  </label>
                </div>
              </div>
              <div class="form-group">
                <label class="form-label">Sample Source</label>
                <select class="form-select">
                  <option>In-house (IKON)</option>
                  <option>Outsource — Mirpur</option>
                  <option>Outsource — Gilistan</option>
                </select>
              </div>
            </div>
            <div class="form-row">
              <div class="form-group">
                <label class="form-label">Date Sent to Buyer</label>
                <input class="form-input" type="date" value="2026-04-08">
              </div>
              <div class="form-group">
                <label class="form-label">Revision Cost (&#2547;)</label>
                <input class="form-input" type="number" placeholder="0">
              </div>
            </div>
            <div class="form-group">
              <label class="form-label">Buyer Feedback / Correction Notes</label>
              <textarea class="form-textarea" rows="2" placeholder="What did the buyer say? What needs fixing?"></textarea>
            </div>
            <div class="form-group">
              <label class="form-label">Internal Notes</label>
              <textarea class="form-textarea" rows="2" placeholder="Notes for your team..."></textarea>
            </div>
            <div class="form-footer" style="padding:0">
              <button class="btn btn-primary">Save Revision</button>
              <button class="btn btn-ghost btn-sm">Cancel</button>
            </div>
          </div>
        </div>

      </div>

      <!-- Right Panel -->
      <div>
        <div class="card">
          <div class="card-header"><span class="ctitle">Revision Summary</span></div>
          <div class="card-body">
            <div class="info-grid" style="grid-template-columns:1fr 1fr">
              <div class="info-item"><div class="label">Total Rounds</div><div class="value" style="color:var(--orange);font-size:18px;font-weight:700">2</div></div>
              <div class="info-item"><div class="label">Status</div><div class="value"><span class="badge at-risk" style="font-size:10px">Awaiting</span></div></div>
              <div class="info-item"><div class="label">Days Since R1</div><div class="value" style="color:var(--red)">3 days</div></div>
              <div class="info-item"><div class="label">Revision Cost</div><div class="value" style="color:var(--orange)">&#2547; 1,200</div></div>
              <div class="info-item"><div class="label">In-house Rounds</div><div class="value">1</div></div>
              <div class="info-item"><div class="label">Outsourced Rounds</div><div class="value">1</div></div>
            </div>
            <hr class="divider">
            <div class="rlabel" style="margin-bottom:8px">Deadline Pressure</div>
            <div style="font-size:12px;color:var(--red);font-weight:600;margin-bottom:4px">&#9888; Expected delivery: 25 Apr 2026</div>
            <div style="font-size:11px;color:var(--text3)">17 days remaining including bulk production time. Approval needed ASAP to start bulk.</div>
          </div>
        </div>
        <div class="card" style="margin-top:16px">
          <div class="card-header"><span class="ctitle">Quick Links</span></div>
          <div class="card-body" style="display:flex;flex-direction:column;gap:8px">
            <a href="03-order-detail.html" class="btn btn-outline" style="justify-content:flex-start">&#128203; Back to Order Detail</a>
            <a href="06-pi.html" class="btn btn-outline" style="justify-content:flex-start;opacity:.5;pointer-events:none">&#128196; Create PI (after approval)</a>
            <a href="08-challan.html" class="btn btn-outline" style="justify-content:flex-start;opacity:.5;pointer-events:none">&#128230; Issue Challan (after bulk)</a>
          </div>
        </div>
      </div>
    </div>

  </div>
</div>
</body></html>"""

# ─── 06 PI ───────────────────────────────────────────────────────────────
pi = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>Proforma Invoice — IKON GAS</title>
<link rel="stylesheet" href="_shared.css">
</head>
<body>
""" + sidebar('p') + """
<div id="main">
  <div id="topbar">
    <div class="topbar-title">Proforma Invoice</div>
    <div class="topbar-sep"></div>
    <div class="topbar-sub">3 issued &middot; 1 draft</div>
    <div class="topbar-right">
      <button class="btn btn-primary btn-sm">+ Create PI</button>
    </div>
  </div>
  <div id="content">

    <!-- PI LIST -->
    <div class="card" style="margin-bottom:20px">
      <div class="card-header">
        <span class="ctitle">All Proforma Invoices</span>
        <div style="display:flex;gap:8px">
          <input class="form-input" style="width:200px;height:30px;font-size:12px" placeholder="Search PI number or company...">
          <select class="form-select" style="width:130px;height:30px;font-size:12px">
            <option>All Status</option>
            <option>Draft</option>
            <option>Issued</option>
            <option>Accepted</option>
            <option>LC Opened</option>
          </select>
        </div>
      </div>
      <div class="card-body" style="padding:0">
        <table class="data-table">
          <thead>
            <tr><th>PI Number</th><th>Order Ref</th><th>Buyer Company</th><th>Value (&#2547;)</th><th>Issue Date</th><th>Delivery</th><th>Status</th><th>Action</th></tr>
          </thead>
          <tbody>
            <tr>
              <td><span class="mono" style="color:var(--accent)">PI-2026/05</span></td>
              <td><span class="mono">BG-2026-041</span></td>
              <td>Bay Group</td>
              <td style="color:var(--green);font-weight:600">&#2547; 2,10,000</td>
              <td>7 Apr 2026</td>
              <td>30 Apr 2026</td>
              <td><span class="badge approved">LC Opened</span></td>
              <td><button class="btn btn-ghost btn-xs">View</button></td>
            </tr>
            <tr>
              <td><span class="mono" style="color:var(--accent)">PI-2026/04</span></td>
              <td><span class="mono">KD-2026-039</span></td>
              <td>KDS Accessories</td>
              <td style="color:var(--green);font-weight:600">&#2547; 88,500</td>
              <td>2 Apr 2026</td>
              <td>20 Apr 2026</td>
              <td><span class="badge at-risk">Accepted</span></td>
              <td><button class="btn btn-ghost btn-xs">View</button></td>
            </tr>
            <tr>
              <td><span class="mono" style="color:var(--accent)">PI-2026/03</span></td>
              <td><span class="mono">NM-2026-033</span></td>
              <td>Noman Group</td>
              <td style="color:var(--green);font-weight:600">&#2547; 3,40,000</td>
              <td>18 Mar 2026</td>
              <td>10 Apr 2026</td>
              <td><span class="badge approved">LC Opened</span></td>
              <td><button class="btn btn-ghost btn-xs">View</button></td>
            </tr>
            <tr style="opacity:.6">
              <td><span class="mono" style="color:var(--text3)">PI-2026/06 (Draft)</span></td>
              <td><span class="mono">F-2026-038</span></td>
              <td>Noman Group</td>
              <td style="color:var(--text3)">TBD</td>
              <td style="color:var(--text3)">Not issued</td>
              <td style="color:var(--text3)">&mdash;</td>
              <td><span class="badge waiting">Draft</span></td>
              <td><button class="btn btn-outline btn-xs">Edit</button></td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- PRINT PREVIEW -->
    <div style="font-size:11px;color:var(--text3);margin-bottom:10px;text-align:right">
      Below: PI-2026/03 print preview &mdash; <button class="btn btn-ghost btn-xs" onclick="window.print()">&#128424; Print</button>
    </div>
    <div class="pi-doc">
      <div class="pi-header">
        <div class="pi-brand">
          <div class="pi-company">IKON GARMENTS ACCESSORIES</div>
          <div class="pi-addr">House 18, Road 10, Sector 09, Uttara, Dhaka-1230, Bangladesh</div>
          <div class="pi-addr">Tel: +8801730214607 &nbsp;|&nbsp; Email: ikongas@gmail.com</div>
          <div class="pi-addr">BIN/VAT: 003543528-0102</div>
          <div class="pi-addr">Bank: Community Bank Ltd, Uttara &nbsp;|&nbsp; Swift: COYMBDDD &nbsp;|&nbsp; A/C: 0100310654101</div>
        </div>
        <div class="pi-meta">
          <div><strong>PROFORMA INVOICE</strong></div>
          <div class="pi-num">PI-2026/03</div>
          <div style="font-size:11px;margin-top:6px"><strong>Date:</strong> 18 March 2026</div>
        </div>
      </div>
      <div class="pi-parties">
        <div class="pi-buyer">
          <div class="pi-blabel">BUYER / CONSIGNEE</div>
          <div class="pi-bname">Noman Group</div>
          <div class="pi-baddr">Plot 12, Block B, Mirpur DOHS, Dhaka-1216</div>
          <div class="pi-baddr">Attn: Tariq — Senior Merchandiser</div>
          <div class="pi-baddr">Tel: +88 01711-334455</div>
        </div>
        <div class="pi-buyer">
          <div class="pi-blabel">DELIVERY DETAILS</div>
          <div class="pi-baddr"><strong>Order Ref:</strong> NM-2026-033</div>
          <div class="pi-baddr"><strong>Delivery Date:</strong> 10 April 2026</div>
          <div class="pi-baddr"><strong>Payment Terms:</strong> 90-Day LC at sight</div>
          <div class="pi-baddr"><strong>Country of Origin:</strong> Bangladesh</div>
          <div class="pi-baddr"><strong>Currency:</strong> BDT</div>
        </div>
      </div>
      <table class="pi-table">
        <thead>
          <tr><th>SL</th><th>Description of Goods</th><th>Style / Ref</th><th>Qty (pcs)</th><th>Unit Price</th><th>Amount (&#2547;)</th></tr>
        </thead>
        <tbody>
          <tr>
            <td>01</td>
            <td>4-Hole Polyester Button, 18L, Black<br><small>Pantone 19-0303 TPX &middot; Hole dia 1.2mm</small></td>
            <td class="mono">MT-301</td>
            <td style="text-align:right">2,00,000</td>
            <td style="text-align:right">&#2547; 1.70</td>
            <td style="text-align:right;font-weight:600">&#2547; 3,40,000</td>
          </tr>
          <tr>
            <td>02</td>
            <td>Woven Label, 40mm, Heat Seal Back<br><small>Brand: Noman &middot; Thread: White on Black</small></td>
            <td class="mono">LBL-WV-09</td>
            <td style="text-align:right">50,000</td>
            <td style="text-align:right">—</td>
            <td style="text-align:right;font-weight:600">Included</td>
          </tr>
        </tbody>
        <tfoot>
          <tr><td colspan="5" style="text-align:right;font-weight:600;padding:8px 12px">Sub-Total</td><td style="text-align:right;font-weight:700;padding:8px 12px">&#2547; 3,40,000</td></tr>
          <tr><td colspan="5" style="text-align:right;font-weight:600;padding:4px 12px">VAT (0% — Export)</td><td style="text-align:right;padding:4px 12px">&#2547; 0</td></tr>
          <tr class="pi-total-row"><td colspan="5" style="text-align:right;font-weight:700;padding:8px 12px;font-size:14px">TOTAL</td><td style="text-align:right;font-weight:800;padding:8px 12px;font-size:14px">&#2547; 3,40,000</td></tr>
        </tfoot>
      </table>
      <div class="pi-words">Amount in Words: <em>Bangladeshi Taka Three Lakh Forty Thousand Only</em></div>
      <div class="pi-terms">
        <div class="pi-terms-title">Terms &amp; Conditions</div>
        <ol>
          <li>Payment by irrevocable LC at 90 days sight, in favour of IKON Garments Accessories.</li>
          <li>Goods remain property of seller until full payment received.</li>
          <li>Partial shipment: not allowed unless agreed in writing.</li>
          <li>Inspection at buyer's facility accepted within 3 days of delivery.</li>
          <li>Disputes to be settled under Bangladesh jurisdiction.</li>
        </ol>
      </div>
      <div class="pi-sign">
        <div class="pi-sign-box">
          <div class="pi-sign-line"></div>
          <div class="pi-sign-name">Prepared By</div>
          <div class="pi-sign-role">IKON Garments Accessories</div>
        </div>
        <div class="pi-sign-box">
          <div class="pi-sign-line"></div>
          <div class="pi-sign-name">Authorized By</div>
          <div class="pi-sign-role">Muhammad Nezam Uddin</div>
        </div>
        <div class="pi-sign-box">
          <div class="pi-sign-line"></div>
          <div class="pi-sign-name">Buyer Acknowledgment</div>
          <div class="pi-sign-role">Noman Group</div>
        </div>
      </div>
    </div>

  </div>
</div>
</body></html>"""

files = {
    '05-sample-revision.html': sample_revision,
    '06-pi.html': pi,
}

for fname, content in files.items():
    path = os.path.join(BASE, fname)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f'Written: {fname}')

print('DONE batch 3')

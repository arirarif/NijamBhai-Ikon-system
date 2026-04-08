import os
BASE = r'c:\Users\arira\Desktop\NijamVhai\mockups\v2'

SIDEBAR = open(os.path.join(BASE,'_write_01_02.py')).read().split('SIDEBAR = """')[1].split('"""')[0]

def sidebar(active):
    keys = dict(d='',c='',o='',n='',s='',p='',l='',ch='')
    keys[active] = 'active'
    return SIDEBAR.format(**keys)

# ─── 03 ORDER DETAIL ─────────────────────────────────────────────────────
order_detail = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>Order Detail — IKON GAS</title>
<link rel="stylesheet" href="_shared.css">
</head>
<body>
""" + sidebar('o') + """
<div id="main">
  <div id="topbar">
    <div class="topbar-title">Order Detail</div>
    <div class="topbar-sep"></div>
    <div class="topbar-sub">F-2026-038 &middot; Noman Group</div>
    <div class="topbar-right">
      <a href="05-sample-revision.html" class="btn btn-outline btn-sm">View Revisions</a>
      <button class="btn btn-primary btn-sm">Update Stage</button>
    </div>
  </div>
  <div id="content">

    <div class="breadcrumb">
      <a href="01-dashboard.html">Dashboard</a><span class="sep">/</span>
      <a href="03-order-detail.html">All Orders</a><span class="sep">/</span>
      <span class="current">F-2026-038</span>
    </div>

    <!-- ORDER HERO -->
    <div class="order-hero">
      <h1>F-2026-038</h1>
      <div class="sub">
        <span class="badge correction">Correction Needed</span>
        <span class="oh-sep">&middot;</span>
        <span>Button</span>
        <span class="oh-sep">&middot;</span>
        <span style="color:var(--accent);font-weight:600">Noman Group</span>
        <span class="oh-sep">&middot;</span>
        <span>Faruq Hossain</span>
        <span class="oh-sep">&middot;</span>
        <span style="color:var(--text3)">Created 3 Apr 2026</span>
      </div>
      <div class="actions">
        <a href="05-sample-revision.html" class="btn btn-outline btn-sm">Review Sample</a>
        <button class="btn btn-green btn-sm">Move to Bulk</button>
        <button class="btn btn-outline btn-sm">Edit Order</button>
        <button class="btn btn-ghost btn-sm">Print</button>
      </div>
    </div>

    <!-- PIPELINE STAGE BAR -->
    <div class="stage-wrap">
      <div class="stage-bar">
        <div class="stage done"><span class="snum">01</span>Order Created</div>
        <div class="stage done"><span class="snum">02</span>Sample Making</div>
        <div class="stage current"><span class="snum">03</span>Sample Revision</div>
        <div class="stage"><span class="snum">04</span>Approved</div>
        <div class="stage"><span class="snum">05</span>Bulk Production</div>
        <div class="stage"><span class="snum">06</span>QC &amp; Packing</div>
        <div class="stage"><span class="snum">07</span>Delivery Challan</div>
        <div class="stage"><span class="snum">08</span>PI Issued</div>
        <div class="stage"><span class="snum">09</span>LC &amp; Payment</div>
      </div>
    </div>

    <div class="two-col">
      <div>

        <!-- ORDER INFO -->
        <div class="card">
          <div class="card-header">
            <span class="ctitle">Order Information</span>
            <span class="badge at-risk">3 revisions</span>
          </div>
          <div class="card-body">
            <div class="info-grid info-grid-wide">
              <div class="info-item"><div class="label">Order ID</div><div class="value mono" style="color:var(--accent)">F-2026-038</div></div>
              <div class="info-item"><div class="label">Product Type</div><div class="value">Button</div></div>
              <div class="info-item"><div class="label">Quantity</div><div class="value">1,50,000 pcs</div></div>
              <div class="info-item"><div class="label">Unit Price</div><div class="value">&#2547; 0.85 / pc</div></div>
              <div class="info-item"><div class="label">Est. Total Value</div><div class="value" style="color:var(--green)">&#2547; 1,27,500</div></div>
              <div class="info-item"><div class="label">Priority</div><div class="value"><span class="badge urgent" style="font-size:10px">Rush</span></div></div>
              <div class="info-item"><div class="label">Season / Collection</div><div class="value">SS2026</div></div>
              <div class="info-item"><div class="label">Expected Delivery</div><div class="value" style="color:var(--orange)">25 Apr 2026</div></div>
              <div class="info-item"><div class="label">Days Since Update</div><div class="value" style="color:var(--red)">6 days <span style="font-size:11px;color:var(--red)">(OVERDUE)</span></div></div>
              <div class="info-item"><div class="label">Sample Source</div><div class="value">In-house</div></div>
              <div class="info-item"><div class="label">Company</div><div class="value" style="color:var(--accent)">Noman Group</div></div>
              <div class="info-item"><div class="label">Merchandiser</div><div class="value">Faruq Hossain</div></div>
            </div>
            <div class="desc-card">
              <div class="label">Product Description / Spec</div>
              <div class="value">4-hole polyester button, 18L, black. Color ref: Pantone 19-0303 TPX. Hole diameter 1.2mm. Must match buyer's approved swatch (attached in R1). No burrs, sharp edges. Shank type &mdash; flat attachment.</div>
            </div>
          </div>
        </div>

        <!-- TECH PACK / SPEC SHEET -->
        <div class="card">
          <div class="card-header">
            <span class="ctitle">Tech Pack / Spec Sheet</span>
            <button class="btn btn-outline btn-xs">+ Upload</button>
          </div>
          <div class="card-body">
            <div style="display:flex;flex-direction:column;gap:8px">
              <div style="display:flex;align-items:center;gap:12px;padding:10px 12px;background:var(--bg3);border:1px solid var(--border);border-radius:var(--radius-sm)">
                <span style="font-size:20px">&#128196;</span>
                <div style="flex:1">
                  <div style="font-size:13px;font-weight:600">TechPack_F2026-038_v2.pdf</div>
                  <div style="font-size:11px;color:var(--text3)">Uploaded 3 Apr 2026 &middot; 2.4 MB</div>
                </div>
                <button class="btn btn-ghost btn-xs">&#128065; View</button>
                <button class="btn btn-ghost btn-xs">&#11015; Download</button>
              </div>
              <div style="display:flex;align-items:center;gap:12px;padding:10px 12px;background:var(--bg3);border:1px solid var(--border);border-radius:var(--radius-sm)">
                <span style="font-size:20px">&#128247;</span>
                <div style="flex:1">
                  <div style="font-size:13px;font-weight:600">BuyerSwatch_reference.jpg</div>
                  <div style="font-size:11px;color:var(--text3)">Uploaded 3 Apr 2026 &middot; 840 KB</div>
                </div>
                <button class="btn btn-ghost btn-xs">&#128065; View</button>
              </div>
            </div>
            <div class="dropzone" style="margin-top:12px">
              <div class="dz-icon">&#128196;</div>
              <div class="dz-title">Drop files here or click to upload</div>
              <div class="dz-sub">PDF, JPG, PNG &middot; max 10 MB per file</div>
            </div>
          </div>
        </div>

        <!-- BULK PRODUCTION SUB-STAGES -->
        <div class="locked-section">
          <div class="locked-header">
            <div style="display:flex;align-items:center;gap:8px">
              <span style="font-size:13px;font-weight:600">Bulk Production Sub-Stages</span>
              <span class="badge waiting" style="font-size:10px">Locked</span>
            </div>
            <span class="lock-badge">Unlocks after sample approval</span>
          </div>
          <div class="locked-body">
            <div class="lock-icon">&#128274;</div>
            <div class="lock-msg">Bulk production tracking not yet available</div>
            <div class="lock-sub">Approve the sample first to unlock Cutting &#8594; Sewing &#8594; Finishing &#8594; QC &#8594; Packing stages</div>
          </div>
          <div style="padding:0 18px 16px">
            <div class="substage-bar" style="opacity:.35;pointer-events:none">
              <div class="substage ss-pending">Cutting</div>
              <div class="substage ss-pending">Sewing</div>
              <div class="substage ss-pending">Finishing</div>
              <div class="substage ss-pending">QC</div>
              <div class="substage ss-pending">Packing</div>
            </div>
          </div>
        </div>

        <!-- SAMPLE REVISIONS SUMMARY -->
        <div class="card" style="margin-top:16px">
          <div class="card-header">
            <span class="ctitle">Sample Revisions</span>
            <span class="badge correction">R3 &mdash; Correction pending</span>
          </div>
          <div class="card-body">
            <div class="revision-item">
              <div class="revision-header">
                <span class="rno">R1 &mdash; Revision 1</span>
                <span class="badge correction" style="margin-left:auto;font-size:10px">Correction</span>
                <span style="font-size:11px;color:var(--text3);margin-left:8px">5 Apr 2026</span>
              </div>
              <div class="revision-body">
                <div class="rev-grid">
                  <div class="rev-item"><div class="rlabel">Made By</div><div class="rvalue">In-house (IKON)</div></div>
                  <div class="rev-item"><div class="rlabel">Sent Date</div><div class="rvalue">6 Apr 2026</div></div>
                  <div class="rev-item"><div class="rlabel">Buyer Feedback</div><div class="rvalue" style="color:var(--red)">Size incorrect &mdash; 18L not 14L</div></div>
                  <div class="rev-item"><div class="rlabel">Revision Cost</div><div class="rvalue">&#2547; 0 (in-house)</div></div>
                </div>
                <div class="feedback-box">
                  <div class="flabel">Buyer Note</div>
                  <div class="ftext">"Button diameter is 14L but we need 18L exactly. Please re-make and match Pantone 19-0303. Also check the hole spacing &mdash; too narrow."</div>
                </div>
              </div>
            </div>
            <div class="revision-item active-rev">
              <div class="revision-header">
                <span class="rno">R2 &mdash; Revision 2 (Current)</span>
                <span class="badge correction" style="margin-left:auto;font-size:10px">Correction</span>
                <span style="font-size:11px;color:var(--text3);margin-left:8px">7 Apr 2026</span>
              </div>
              <div class="revision-body">
                <div class="rev-grid">
                  <div class="rev-item"><div class="rlabel">Made By</div><div class="rlabel">Outsourced &mdash; Mirpur</div></div>
                  <div class="rev-item"><div class="rlabel">Sent Date</div><div class="rvalue">8 Apr 2026</div></div>
                  <div class="rev-item"><div class="rlabel">Status</div><div class="rvalue" style="color:var(--orange)">Awaiting buyer response</div></div>
                  <div class="rev-item"><div class="rlabel">Revision Cost</div><div class="rvalue">&#2547; 1,200</div></div>
                </div>
                <div class="feedback-box internal">
                  <div class="flabel">Internal Note</div>
                  <div class="ftext">18L corrected. Hole spacing now 1.2mm as spec. Color match looks good. Sent via courier to Faruq bhai. Waiting callback.</div>
                </div>
                <div class="rev-actions">
                  <button class="btn btn-green btn-sm">Mark Approved</button>
                  <button class="btn btn-red btn-sm">Log Correction</button>
                </div>
              </div>
            </div>
          </div>
        </div>

      </div>

      <!-- RIGHT SIDEBAR -->
      <div>

        <!-- Timeline -->
        <div class="card">
          <div class="card-header"><span class="ctitle">Order Timeline</span></div>
          <div class="card-body">
            <div class="timeline">
              <div class="tl-item">
                <div class="tl-dot-wrap"><div class="tl-dot done"></div><div class="tl-line"></div></div>
                <div class="tl-content"><div class="tl-date">3 Apr 2026, 10:30</div><div class="tl-title">Order Created</div><div class="tl-sub">By Nezam Uddin &middot; Faruq Hossain visited</div></div>
              </div>
              <div class="tl-item">
                <div class="tl-dot-wrap"><div class="tl-dot done"></div><div class="tl-line"></div></div>
                <div class="tl-content"><div class="tl-date">5 Apr 2026, 14:00</div><div class="tl-title">R1 Sample Made</div><div class="tl-sub">In-house production &middot; sent same day</div></div>
              </div>
              <div class="tl-item">
                <div class="tl-dot-wrap"><div class="tl-dot done"></div><div class="tl-line"></div></div>
                <div class="tl-content"><div class="tl-date">6 Apr 2026, 09:15</div><div class="tl-title">R1 Correction Received</div><div class="tl-sub">Size issue &mdash; 14L instead of 18L</div></div>
              </div>
              <div class="tl-item">
                <div class="tl-dot-wrap"><div class="tl-dot done"></div><div class="tl-line"></div></div>
                <div class="tl-content"><div class="tl-date">7 Apr 2026, 16:00</div><div class="tl-title">R2 Sample Made</div><div class="tl-sub">Outsourced to Mirpur vendor &middot; &#2547; 1,200</div></div>
              </div>
              <div class="tl-item">
                <div class="tl-dot-wrap"><div class="tl-dot current"></div><div class="tl-line"></div></div>
                <div class="tl-content"><div class="tl-date">8 Apr 2026, 11:00</div><div class="tl-title">R2 Sent to Buyer</div><div class="tl-sub">Waiting response from Faruq Hossain</div></div>
              </div>
              <div class="tl-item">
                <div class="tl-dot-wrap"><div class="tl-dot pending"></div><div class="tl-line"></div></div>
                <div class="tl-content"><div class="tl-date tl-title pending">Pending</div><div class="tl-title pending">Sample Approval</div></div>
              </div>
              <div class="tl-item">
                <div class="tl-dot-wrap"><div class="tl-dot pending"></div><div class="tl-line"></div></div>
                <div class="tl-content"><div class="tl-date tl-title pending">Pending</div><div class="tl-title pending">Bulk Production Start</div></div>
              </div>
              <div class="tl-item">
                <div class="tl-dot-wrap"><div class="tl-dot pending"></div></div>
                <div class="tl-content"><div class="tl-date tl-title pending">Pending</div><div class="tl-title pending">Delivery &amp; Payment</div></div>
              </div>
            </div>
          </div>
        </div>

        <!-- Contacts -->
        <div class="card">
          <div class="card-header"><span class="ctitle">Contact &amp; Company</span></div>
          <div class="card-body">
            <div style="display:flex;align-items:center;gap:12px;margin-bottom:14px">
              <div class="merch-avatar" style="background:linear-gradient(135deg,#4f8ef7,#818cf8)">F</div>
              <div>
                <div style="font-size:14px;font-weight:700">Faruq Hossain</div>
                <div style="font-size:11px;color:var(--text3)">Senior Merchandiser &middot; Noman Group</div>
                <div style="font-size:12px;color:var(--text2);margin-top:3px">&#128222; +88 01811-222333</div>
              </div>
            </div>
            <div class="info-grid" style="grid-template-columns:1fr 1fr">
              <div class="info-item"><div class="label">Company</div><div class="value" style="color:var(--accent)">Noman Group</div></div>
              <div class="info-item"><div class="label">Location</div><div class="value">Mirpur, Dhaka</div></div>
              <div class="info-item"><div class="label">Total Orders</div><div class="value">47</div></div>
              <div class="info-item"><div class="label">With Faruq</div><div class="value">12</div></div>
            </div>
          </div>
        </div>

        <!-- Quick actions -->
        <div class="card">
          <div class="card-header"><span class="ctitle">Quick Actions</span></div>
          <div class="card-body" style="display:flex;flex-direction:column;gap:8px">
            <a href="05-sample-revision.html" class="btn btn-outline" style="justify-content:flex-start">&#128260; Log New Revision</a>
            <a href="06-pi.html" class="btn btn-outline" style="justify-content:flex-start">&#128196; Create PI</a>
            <a href="08-challan.html" class="btn btn-outline" style="justify-content:flex-start">&#128230; Issue Challan</a>
            <button class="btn btn-ghost" style="justify-content:flex-start;color:var(--red)">&#128465; Archive Order</button>
          </div>
        </div>

      </div>
    </div>

  </div>
</div>
</body></html>"""

# ─── 04 NEW ORDER ────────────────────────────────────────────────────────
new_order = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>New Order — IKON GAS</title>
<link rel="stylesheet" href="_shared.css">
</head>
<body>
""" + sidebar('n') + """
<div id="main">
  <div id="topbar">
    <div class="topbar-title">New Order</div>
    <div class="topbar-sep"></div>
    <div class="topbar-sub">Create a new order from a buyer visit</div>
    <div class="topbar-right">
      <a href="01-dashboard.html" class="btn btn-ghost btn-sm">Cancel</a>
    </div>
  </div>
  <div id="content">

    <div class="breadcrumb">
      <a href="01-dashboard.html">Dashboard</a><span class="sep">/</span>
      <span class="current">New Order</span>
    </div>

    <!-- Step Wizard -->
    <div class="step-wizard">
      <div class="step-item active">
        <div class="step-box"><div class="step-num">1</div>Company &amp; Buyer</div>
      </div>
      <div class="step-item">
        <div class="step-box"><div class="step-num">2</div>Product Details</div>
      </div>
      <div class="step-item">
        <div class="step-box"><div class="step-num">3</div>Sample Plan</div>
      </div>
      <div class="step-item">
        <div class="step-box"><div class="step-num">4</div>Review &amp; Create</div>
      </div>
    </div>

    <div class="two-col" style="grid-template-columns:1fr 320px">
      <div>

        <!-- Step 1 -->
        <div class="form-section focus-section">
          <div class="fs-header">
            <div style="display:flex;align-items:center">
              <div class="fs-num">1</div>
              <div class="fs-title">Company &amp; Buyer Information</div>
            </div>
          </div>
          <div class="fs-body">
            <div class="form-row">
              <div class="form-group">
                <label class="form-label">Buyer Company <span class="req">*</span></label>
                <select class="form-select">
                  <option value="">Select company...</option>
                  <option>Noman Group</option>
                  <option>Bay Group</option>
                  <option>KDS Accessories Ltd.</option>
                  <option>Grameen Check Ltd.</option>
                  <option value="new">+ Add New Company</option>
                </select>
              </div>
              <div class="form-group">
                <label class="form-label">Merchandiser <span class="req">*</span></label>
                <select class="form-select">
                  <option value="">Select merchandiser...</option>
                  <option>Faruq Hossain</option>
                  <option>Rashida Begum</option>
                  <option>Anwar Hossain</option>
                  <option value="new">+ Add New Person</option>
                </select>
                <div class="form-hint">Person who visited and placed the order</div>
              </div>
            </div>
            <div class="form-row-3">
              <div class="form-group">
                <label class="form-label">Visit Date <span class="req">*</span></label>
                <input class="form-input" type="date" value="2026-04-08">
              </div>
              <div class="form-group">
                <label class="form-label">Priority</label>
                <select class="form-select">
                  <option>Normal</option>
                  <option>Urgent</option>
                  <option>Rush</option>
                </select>
              </div>
              <div class="form-group">
                <label class="form-label">Expected Delivery</label>
                <input class="form-input" type="date">
              </div>
            </div>
          </div>
        </div>

        <!-- Step 2 -->
        <div class="form-section">
          <div class="fs-header">
            <div style="display:flex;align-items:center">
              <div class="fs-num">2</div>
              <div class="fs-title">Product Details</div>
            </div>
          </div>
          <div class="fs-body">
            <div class="form-row">
              <div class="form-group">
                <label class="form-label">Product Type <span class="req">*</span></label>
                <select class="form-select">
                  <option value="">Select type...</option>
                  <option>Button</option>
                  <option>Zipper Pull</option>
                  <option>Hang Tag</option>
                  <option>Woven Label</option>
                  <option>Printed Label</option>
                  <option>Elastic Band</option>
                  <option>Ribbon</option>
                  <option>Buckle</option>
                  <option>Thread</option>
                  <option>Other</option>
                </select>
              </div>
              <div class="form-group">
                <label class="form-label">Season / Collection</label>
                <input class="form-input" type="text" placeholder="e.g. SS2026, AW2026">
              </div>
            </div>
            <div class="form-row-3">
              <div class="form-group">
                <label class="form-label">Quantity (pcs) <span class="req">*</span></label>
                <input class="form-input" type="number" placeholder="e.g. 150000">
              </div>
              <div class="form-group">
                <label class="form-label">Unit Price (&#2547;)</label>
                <div class="input-group">
                  <input class="form-input" type="number" step="0.01" placeholder="0.00">
                  <span class="input-addon">/ pc</span>
                </div>
              </div>
              <div class="form-group">
                <label class="form-label">Est. Total Value</label>
                <div class="form-input" style="background:var(--bg4);color:var(--text3);cursor:default">Auto-calculated</div>
              </div>
            </div>
            <div class="form-group">
              <label class="form-label">Product Specification / Description <span class="req">*</span></label>
              <textarea class="form-textarea" rows="3" placeholder="Describe size, color ref (Pantone), material, finishing, special requirements..."></textarea>
            </div>
            <div class="form-group">
              <label class="form-label">Tech Pack / Spec Sheet</label>
              <div class="dropzone">
                <div class="dz-icon">&#128196;</div>
                <div class="dz-title">Drop tech pack here or click to upload</div>
                <div class="dz-sub">PDF, JPG, PNG &middot; max 10 MB</div>
              </div>
              <div class="form-hint">Optional but recommended &mdash; buyer often provides this during visit</div>
            </div>
          </div>
        </div>

        <!-- Step 3 -->
        <div class="form-section">
          <div class="fs-header">
            <div style="display:flex;align-items:center">
              <div class="fs-num">3</div>
              <div class="fs-title">Sample Plan</div>
            </div>
          </div>
          <div class="fs-body">
            <div class="form-group">
              <label class="form-label">Where will the sample be made? <span class="req">*</span></label>
              <div class="radio-cards">
                <label class="radio-card selected">
                  <input type="radio" name="sample_src" value="inhouse" checked>
                  <div class="rc-icon">&#127981;</div>
                  <div class="rc-title">In-house</div>
                  <div class="rc-sub">Made at IKON factory. No extra cost.</div>
                </label>
                <label class="radio-card">
                  <input type="radio" name="sample_src" value="mirpur">
                  <div class="rc-icon">&#128228;</div>
                  <div class="rc-title">Outsource &mdash; Mirpur</div>
                  <div class="rc-sub">Send to Mirpur vendor. Costs extra.</div>
                </label>
                <label class="radio-card">
                  <input type="radio" name="sample_src" value="gilistan">
                  <div class="rc-icon">&#128228;</div>
                  <div class="rc-title">Outsource &mdash; Gilistan</div>
                  <div class="rc-sub">Send to Gilistan area vendor.</div>
                </label>
              </div>
            </div>
            <div class="form-row">
              <div class="form-group">
                <label class="form-label">Sample Due Date</label>
                <input class="form-input" type="date">
              </div>
              <div class="form-group">
                <label class="form-label">Sample Cost (if outsourced)</label>
                <div class="input-group">
                  <span class="input-addon">&#2547;</span>
                  <input class="form-input" type="number" placeholder="0">
                </div>
              </div>
            </div>
            <div class="form-group">
              <label class="form-label">Internal Notes</label>
              <textarea class="form-textarea" rows="2" placeholder="Any special instructions for the production team..."></textarea>
            </div>
          </div>
        </div>

        <div class="form-footer">
          <button class="btn btn-outline">Save as Draft</button>
          <button class="btn btn-primary">Create Order &amp; Start Sample &#8594;</button>
        </div>

      </div>

      <!-- Right summary panel -->
      <div>
        <div class="card" style="position:sticky;top:80px">
          <div class="card-header"><span class="ctitle">Order Summary</span></div>
          <div class="card-body">
            <div style="font-size:11px;color:var(--text3);margin-bottom:14px">Fill the form to see a live preview</div>
            <div style="display:flex;flex-direction:column;gap:8px">
              <div class="info-item"><div class="label">Company</div><div class="value" style="color:var(--text3)">Not selected</div></div>
              <div class="info-item"><div class="label">Merchandiser</div><div class="value" style="color:var(--text3)">Not selected</div></div>
              <div class="info-item"><div class="label">Product</div><div class="value" style="color:var(--text3)">Not selected</div></div>
              <div class="info-item"><div class="label">Quantity</div><div class="value" style="color:var(--text3)">&mdash;</div></div>
              <div class="info-item"><div class="label">Est. Value</div><div class="value" style="color:var(--text3)">&mdash;</div></div>
              <div class="info-item"><div class="label">Priority</div><div class="value" style="color:var(--text3)">Normal</div></div>
            </div>
            <hr class="divider">
            <div style="font-size:11px;color:var(--text3)">
              <strong style="color:var(--text2)">What happens next?</strong><br><br>
              1. Order is created with status <em>Sample Making</em><br>
              2. Sample is produced (in-house or outsourced)<br>
              3. Sample is sent to buyer &mdash; log under Revisions<br>
              4. Repeat until <em>Approved</em><br>
              5. Move to Bulk Production
            </div>
          </div>
        </div>
      </div>
    </div>

  </div>
</div>
</body></html>"""

# Write files
files = {
    '03-order-detail.html': order_detail,
    '04-new-order.html': new_order,
}

for fname, content in files.items():
    path = os.path.join(BASE, fname)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f'Written: {fname}')

print('DONE batch 2')

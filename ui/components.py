# ui/components.py
import datetime
from ui.styles import THEME

def colorize_payload_html(raw_payload_str, mode="Standard 2-Byte Words"):
    if not isinstance(raw_payload_str, str) or not raw_payload_str.strip():
        return ""
    
    bytes_list = raw_payload_str.strip().split()
    chips = []
    
    for idx, b in enumerate(bytes_list):
        is_padding = b in ("00", "FF")
        if mode == "AUTOSAR / E2E Safety":
            if idx in (0, 1):
                cls = "byte-safety"
            elif is_padding and idx >= 6:
                cls = "byte-padding"
            elif (idx // 2) % 2 == 0:
                cls = "byte-data-1"
            else:
                cls = "byte-data-2"
        elif mode == "UDS / Diagnostic (ISO-TP)":
            if idx == 0:
                cls = "byte-header-1"
            elif idx == 1:
                cls = "byte-header-2"
            elif idx in (2, 3):
                cls = "byte-safety"
            elif is_padding and idx >= 6:
                cls = "byte-padding"
            else:
                cls = "byte-data-1"
        elif mode == "Standard 2-Byte Words":
            if is_padding and idx >= 8:
                cls = "byte-padding"
            elif (idx // 2) % 4 == 0:
                cls = "byte-header-1"
            elif (idx // 2) % 4 == 1:
                cls = "byte-data-1"
            elif (idx // 2) % 4 == 2:
                cls = "byte-header-2"
            else:
                cls = "byte-data-2"
        else:
            cls = "byte-padding" if is_padding else "byte-header-1"
            
        chips.append(f'<span class="byte-chip {cls}">{b}</span>')
    return "".join(chips)

def render_themed_table(dataframe, verdict_col=None, payload_col=None, payload_mode="Standard 2-Byte Words"):
    if dataframe.empty:
        return "<p>No data recorded.</p>"
    
    html = ['<div class="custom-table-container"><table class="custom-table"><thead><tr>']
    for col in dataframe.columns:
        html.append(f'<th>{col}</th>')
    html.append('</tr></thead><tbody>')
    
    for _, row in dataframe.iterrows():
        html.append('<tr>')
        for col in dataframe.columns:
            val = str(row[col])
            if verdict_col and col == verdict_col:
                if "FAIL" in val:
                    html.append(f'<td><span style="background-color: {THEME["badge_fail_bg"]}; color: {THEME["badge_fail_fg"]}; padding: 3px 8px; border-radius: 2px; font-weight: 700; font-family: monospace;">{val}</span></td>')
                elif "PASS" in val:
                    html.append(f'<td><span style="background-color: {THEME["badge_pass_bg"]}; color: {THEME["badge_pass_fg"]}; padding: 3px 8px; border-radius: 2px; font-weight: 700; font-family: monospace;">{val}</span></td>')
                else:
                    html.append(f'<td>{val}</td>')
            elif payload_col and col == payload_col:
                highlighted_hex = colorize_payload_html(val, mode=payload_mode)
                html.append(f'<td>{highlighted_hex}</td>')
            else:
                html.append(f'<td>{val}</td>')
        html.append('</tr>')
    html.append('</tbody></table></div>')
    return "".join(html)

def generate_html_report(filename, total_msgs, unique_ids, duration_sec, health_df, event_df, audit_df):
    health_html = health_df.head(15).to_html(classes="table", index=False) if not health_df.empty else "<p>No periodic messages evaluated.</p>"
    event_html = event_df.to_html(classes="table", index=False) if not event_df.empty else "<p>No transition events logged.</p>"
    audit_html = audit_df.to_html(classes="table", index=False) if not audit_df.empty else "<p>No safety alive counters evaluated.</p>"
    timestamp_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    return f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>CAN Diagnostics & Functional Safety Report</title>
<style>
    body {{ font-family: "Segoe UI", -apple-system, BlinkMacSystemFont, sans-serif; background-color: #0F172A; color: #F1F5F9; margin: 30px; }}
    .container {{ max-width: 1100px; margin: auto; background: #1E293B; padding: 25px; border-radius: 4px; border: 1px solid #334155; }}
    h1 {{ font-size: 18px; color: #38BDF8; border-bottom: 2px solid #334155; padding-bottom: 8px; text-transform: uppercase; }}
    h2 {{ font-size: 14px; color: #94A3B8; margin-top: 24px; text-transform: uppercase; letter-spacing: 0.05em; }}
    .meta-box {{ display: flex; gap: 15px; background: #0F172A; padding: 12px; border-radius: 4px; margin-bottom: 20px; border: 1px solid #334155; }}
    .meta-item {{ flex: 1; text-align: center; }}
    .meta-item strong {{ display: block; font-size: 18px; color: #38BDF8; font-family: Consolas, monospace; }}
    table.table {{ width: 100%; border-collapse: collapse; margin-top: 10px; font-size: 11px; font-family: Consolas, monospace; }}
    table.table th, table.table td {{ border: 1px solid #334155; padding: 6px 10px; text-align: left; }}
    table.table th {{ background-color: #0F172A; color: #94A3B8; font-weight: 700; text-transform: uppercase; }}
    table.table tr:nth-child(even) {{ background-color: rgba(255,255,255,0.02); }}
    .btn-print {{ background: #0284C7; color: #FFFFFF; padding: 8px 14px; border: none; border-radius: 2px; cursor: pointer; float: right; font-weight: 700; }}
    @media print {{ .btn-print {{ display: none; }} body {{ margin: 0; background: white; color: black; }} .container {{ border: none; }} }}
</style>
</head>
<body>
<div class="container">
    <button class="btn-print" onclick="window.print()">Print / Export PDF</button>
    <h1>CAN Network Diagnostic Audit</h1>
    <p style="color: #94A3B8; font-size: 12px;"><b>Trace Source:</b> {filename} | <b>Timestamp:</b> {timestamp_str}</p>
    <div class="meta-box">
        <div class="meta-item"><span>Total Frames</span><strong>{total_msgs:,}</strong></div>
        <div class="meta-item"><span>Unique IDs</span><strong>{unique_ids}</strong></div>
        <div class="meta-item"><span>Duration</span><strong>{duration_sec} s</strong></div>
    </div>
    <h2>1. Network Health & Jitter Audit</h2>
    {health_html}
    <h2>2. Functional Safety (ASIL) Alive Counter Audit</h2>
    {audit_html}
    <h2>3. State-Transition Event Log</h2>
    {event_html}
</div>
</body>
</html>
"""
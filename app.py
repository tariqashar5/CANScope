# app.py
import streamlit as st
import os
import io
import pandas as pd
from src.exporter import ask_save_path, save_content, open_in_explorer

# Core Engine Modules
from src.parser import parse_can_log
from src.decoder import (
    load_dbc_database, 
    extract_dbc_indices, 
    get_message_name_by_hex, 
    decode_can_payload
)
from src.diagnostics import (
    calculate_network_health, 
    evaluate_alive_counters, 
    detect_state_transitions
)

# Presentation Modules
from ui.styles import THEME, get_theme_css
from ui.components import render_themed_table, generate_html_report
from ui.charts import build_oscilloscope_figure

st.set_page_config(
    page_title="CAN Protocol & Multi-Trace Analyzer",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply Dark Workstation Stylesheet
st.markdown(get_theme_css(), unsafe_allow_html=True)

# Cached Loaders
@st.cache_data(show_spinner=False)
def cached_parse_log(file_path):
    return parse_can_log(file_path)

@st.cache_resource(show_spinner=False)
def cached_load_dbc(dbc_path):
    return load_dbc_database(dbc_path)

# --- SIDEBAR: CONFIGURATION & SETUP ---
with st.sidebar:
    st.markdown("<h2>Configuration & Setup</h2>", unsafe_allow_html=True)
    st.caption("Channel definitions and measurement trace inputs.")
    
    st.markdown("<div style='margin-top: 14px;'></div>", unsafe_allow_html=True)
    
    # 1. DBC Section
    st.markdown('<div class="tool-titlebar">DATABASE DEFINITION [.DBC]</div>', unsafe_allow_html=True)
    dbc_file = st.file_uploader(
        "Upload DBC File", 
        type=['dbc'], 
        key="dbc_uploader", 
        label_visibility="collapsed"
    )
    
    st.markdown(f"<hr style='border: 0; border-top: 1px solid {THEME['border_card']}; margin: 20px 0 16px 0;'>", unsafe_allow_html=True)
    
    # 2. Measurement Traces Bay
    st.markdown('<div class="tool-titlebar">MEASUREMENT TRACES [.BLF / .ASC]</div>', unsafe_allow_html=True)
    
    primary_log_file = st.file_uploader(
        "Upload Primary Log",
        type=['asc', 'blf'],
        key="primary_log_upload",
        label_visibility="collapsed"
    )
    
    st.markdown("<div style='margin-top: 14px;'></div>", unsafe_allow_html=True)
    
    st.markdown("<span class='metric-label' style='display:block; margin-bottom: 4px;'>Add log file(s) for comparison</span>", unsafe_allow_html=True)
    comp_log_files = st.file_uploader(
        "Add log file(s) for comparison",
        type=['asc', 'blf'],
        accept_multiple_files=True,
        key="comp_logs_upload",
        label_visibility="collapsed"
    )

# --- LOAD DATABASE ---
db = None
signal_to_msg_hex, signal_choices, alive_counter_candidates = {}, {}, []

if dbc_file is not None:
    os.makedirs("data", exist_ok=True)
    temp_dbc_path = os.path.join("data", dbc_file.name)
    with open(temp_dbc_path, "wb") as f:
        f.write(dbc_file.getbuffer())
    try:
        db = cached_load_dbc(temp_dbc_path)
        signal_to_msg_hex, signal_choices, alive_counter_candidates = extract_dbc_indices(db)
    except Exception as e:
        st.sidebar.error(f"DBC Load Error: {e}")

# --- MAIN HEADING (BIGGER & CENTERED) ---
st.markdown(f"""
<div style="text-align: center; margin-bottom: 24px; padding-top: 6px;">
    <div class="main-app-title">CANScope</div>
    <p style="color: {THEME['text_muted']}; font-size: 14px; margin: 0;">Automotive bus timing analysis, functional safety validation, and multi-channel trace comparison.</p>
</div>
""", unsafe_allow_html=True)

if primary_log_file is None:
    st.info("No active measurement log. Attach a primary `.blf` or `.asc` file in the Configuration panel to begin analysis.")
else:
    active_files = [primary_log_file]
    if comp_log_files:
        for cf in comp_log_files:
            if cf.name != primary_log_file.name and cf.name not in [f.name for f in active_files]:
                active_files.append(cf)

    loaded_data = {}
    os.makedirs("data", exist_ok=True)
    
    for f in active_files:
        f_path = os.path.join("data", f.name)
        with open(f_path, "wb") as buffer:
            buffer.write(f.getbuffer())
        
        parsed_df = cached_parse_log(f_path).copy()
        t_start = parsed_df['Timestamp'].iloc[0]
        parsed_df['Relative_Time_ms'] = ((parsed_df['Timestamp'] - t_start) * 1000.0).round(2)
        
        if db is not None:
            id_map = {can_id: get_message_name_by_hex(can_id, db) for can_id in parsed_df['CAN_ID'].cat.categories}
            parsed_df['Message_Name'] = parsed_df['CAN_ID'].map(id_map)
        else:
            parsed_df['Message_Name'] = "Unknown"
            
        loaded_data[f.name] = parsed_df

    primary_name = primary_log_file.name
    primary_df = loaded_data[primary_name]
    duration_ms = round(primary_df['Relative_Time_ms'].iloc[-1], 2)
    duration_s = round(duration_ms / 1000.0, 4)

    # Status Cards
    s1, s2, s3, s4 = st.columns(4)
    with s1:
        st.markdown(f"""
        <div class="tool-window">
            <span class="metric-label">Measurement Frames</span>
            <div class="metric-value">{len(primary_df):,} <span style="font-size: 13px; color:{THEME['text_muted']};">({len(loaded_data)} traces loaded)</span></div>
        </div>
        """, unsafe_allow_html=True)
    with s2:
        st.markdown(f"""
        <div class="tool-window">
            <span class="metric-label">Active CAN IDs</span>
            <div class="metric-value">{primary_df['CAN_ID'].nunique()}</div>
        </div>
        """, unsafe_allow_html=True)
    with s3:
        st.markdown(f"""
        <div class="tool-window">
            <span class="metric-label">Trace Duration</span>
            <div class="metric-value">{duration_ms:,.0f} <span style="font-size: 13px; color:{THEME['text_muted']};">ms ({duration_s} s)</span></div>
        </div>
        """, unsafe_allow_html=True)
    with s4:
        status_color = THEME['badge_pass_fg'] if db else THEME['badge_fail_fg']
        status_text = "Attached" if db else "Unloaded"
        st.markdown(f"""
        <div class="tool-window">
            <span class="metric-label">Database Status</span>
            <div class="metric-value" style="color: {status_color}; font-size: 1.5rem;">{status_text}</div>
        </div>
        """, unsafe_allow_html=True)

    # Separator
    st.markdown(f"<div style='margin-top: 18px; margin-bottom: 22px; border-bottom: 1px solid {THEME['border_card']};'></div>", unsafe_allow_html=True)

    # Seamless Ribbon Tabs
    tab_scope, tab_health, tab_safety, tab_export, tab_raw = st.tabs([
        "Graphics [Measurement]",
        "Bus Statistics [Timing & Jitter]",
        "Trace & ASIL Analysis",
        "Logging & Export Setup",
        "Trace Window [CAN / CAN FD]"
    ])

    file_options = list(loaded_data.keys())

    # ==========================================
    # TAB 1: GRAPHICS WINDOW [MEASUREMENT]
    # ==========================================
    with tab_scope:
        st.markdown("<div style='margin-top: 14px;'></div>", unsafe_allow_html=True)
        if db is None:
            st.info("Attach a `.dbc` file in Configuration to decode physical signals.")
        else:
            all_signals = sorted(list(signal_to_msg_hex.keys()))
            unique_trace_names = list(dict.fromkeys(loaded_data.keys()))
            num_logs = len(unique_trace_names)
            
            scope_cols = st.columns(num_logs) if num_logs > 1 else [st.container()]
            
            for idx, fname in enumerate(unique_trace_names):
                f_df = loaded_data[fname]
                f_duration_ms = round(f_df['Relative_Time_ms'].iloc[-1], 1)
                
                with scope_cols[idx]:
                    st.markdown(f"""
                    <div class="tool-titlebar">Channel {idx+1}: {fname} [{len(f_df):,} frames | {f_duration_ms:,.0f} ms]</div>
                    """, unsafe_allow_html=True)
                    
                    # Consistent session key for this trace across all tabs
                    f_signals = st.multiselect(
                        f"Signals for {fname}",
                        all_signals,
                        key=f"scope_signals_{fname}",
                        placeholder="Add signals to plot...",
                        label_visibility="collapsed"
                    )
                    
                    if f_signals:
                        fig_col = build_oscilloscope_figure(
                            f_df, f_signals, signal_to_msg_hex, signal_choices, db
                        )
                        st.plotly_chart(fig_col, use_container_width=True, key=f"plotly_chart_{fname}_{idx}")
                        
                        # Native Save As Dialog for Plot
                        default_plot_name = f"scope_{os.path.splitext(fname)[0]}.html"
                        if st.button("Save Plot as Interactive HTML", key=f"btn_save_plot_{fname}_{idx}"):
                            save_dest = ask_save_path(
                                default_filename=default_plot_name,
                                file_types=[("Interactive HTML Plot", "*.html"), ("All Files", "*.*")]
                            )
                            if save_dest:
                                fig_col.write_html(save_dest)
                                st.success(f"Plot saved: `{save_dest}`")
                                open_in_explorer(save_dest)
                    else:
                        st.caption("Select physical signals to render waveform channels.")

    # ==========================================
    # TAB 2: BUS STATISTICS [TIMING & JITTER]
    # ==========================================
    with tab_health:
        st.markdown("<div style='margin-top: 14px;'></div>", unsafe_allow_html=True)
        # TAB HEADING: BIGGER & NOT BOLD
        st.markdown('<div class="tab-section-heading">Bus Timing & Message Statistics</div>', unsafe_allow_html=True)
        
        target_health_file = st.radio(
            "Target Log Selection", 
            options=file_options, 
            horizontal=True, 
            key="health_target_file",
            label_visibility="collapsed"
        )
        st.markdown("<div style='margin-top: 10px;'></div>", unsafe_allow_html=True)
        
        h_df = loaded_data[target_health_file]
        health_summary_df = calculate_network_health(h_df)
        
        if not health_summary_df.empty:
            st.markdown(render_themed_table(health_summary_df, verdict_col="Verdict"), unsafe_allow_html=True)
        else:
            st.info("Insufficient periodic message data.")

    # ==========================================
    # TAB 3: TRACE & ASIL ANALYSIS
    # ==========================================
    with tab_safety:
        st.markdown("<div style='margin-top: 14px;'></div>", unsafe_allow_html=True)
        # TAB HEADING: BIGGER & NOT BOLD
        st.markdown('<div class="tab-section-heading">Functional Safety & Transition Trace</div>', unsafe_allow_html=True)
        
        target_safety_file = st.radio(
            "Target Log Selection", 
            options=file_options, 
            horizontal=True, 
            key="safety_target_file",
            label_visibility="collapsed"
        )
        s_df = loaded_data[target_safety_file]
        st.markdown("<div style='margin-top: 10px;'></div>", unsafe_allow_html=True)
        
        st.markdown("<h3>1. Alive Counter Integrity (ISO 26262 ASIL Check)</h3>", unsafe_allow_html=True)
        if db is not None and alive_counter_candidates:
            selected_counters = st.multiselect(
                f"Active Alive Counters ({target_safety_file})",
                sorted(alive_counter_candidates),
                default=sorted(alive_counter_candidates)[:3] if alive_counter_candidates else None,
                key=f"safety_counters_{target_safety_file}"
            )
            audit_summary_df = evaluate_alive_counters(
                s_df, selected_counters, signal_to_msg_hex, db, decode_can_payload, get_message_name_by_hex
            )
            if not audit_summary_df.empty:
                st.markdown(render_themed_table(audit_summary_df, verdict_col="Verdict"), unsafe_allow_html=True)
        else:
            st.caption("No alive counter signals identified.")

        st.markdown(f"<hr style='border: 0; border-top: 1px solid {THEME['border_card']}; margin: 20px 0 16px 0;'>", unsafe_allow_html=True)

        st.markdown("<h3>2. Discrete State Machine Transition Log</h3>", unsafe_allow_html=True)
        all_signals = sorted(list(signal_to_msg_hex.keys())) if db else []
        if db is not None:
            trigger_signals = st.multiselect(
                f"State Transition Triggers ({target_safety_file})",
                all_signals,
                key=f"trans_signals_{target_safety_file}"
            )
            if trigger_signals:
                event_summary_df = detect_state_transitions(
                    s_df, trigger_signals, signal_to_msg_hex, db, decode_can_payload
                )
                if not event_summary_df.empty:
                    st.markdown(render_themed_table(event_summary_df), unsafe_allow_html=True)
                else:
                    st.info("No transitions occurred.")

    # ==========================================
    # TAB 4: LOGGING & EXPORT SETUP
    # ==========================================
    with tab_export:
        st.markdown("<div style='margin-top: 14px;'></div>", unsafe_allow_html=True)
        st.markdown('<div class="tab-section-heading">Automated Documentation & Data Export</div>', unsafe_allow_html=True)
        
        target_export_file = st.radio(
            "Target Log Selection", 
            options=file_options, 
            horizontal=True, 
            key="export_target_file", 
            label_visibility="collapsed"
        )
        st.markdown("<div style='margin-top: 14px;'></div>", unsafe_allow_html=True)
        
        exp_df = loaded_data[target_export_file]
        exp_duration_s = round(exp_df['Relative_Time_ms'].iloc[-1] / 1000.0, 4)
        exp_health_df = calculate_network_health(exp_df)
        
        c1, c2 = st.columns(2)
        with c1:
            st.markdown(f"""
            <div class="tool-window">
                <div class="tool-titlebar" style="margin-top:0;">Verification Test Report [.html]</div>
                <p style="font-size: 13.5px; color: {THEME['text_muted']}; margin: 10px 0 14px 0;">Export complete bus statistics, ASIL verification, and transition logs for {target_export_file}.</p>
            </div>
            """, unsafe_allow_html=True)
            
            default_report_name = f"report_{os.path.splitext(target_export_file)[0]}.html"
            
            if st.button(f"Save Verification Report ({target_export_file})", use_container_width=True, key="btn_save_report"):
                chosen_path = ask_save_path(
                    default_filename=default_report_name,
                    file_types=[("HTML Report", "*.html"), ("All Files", "*.*")]
                )
                if chosen_path:
                    report_html = generate_html_report(
                        target_export_file, len(exp_df), exp_df['CAN_ID'].nunique(), exp_duration_s,
                        exp_health_df, pd.DataFrame(), pd.DataFrame()
                    )
                    save_content(chosen_path, report_html)
                    st.success(f"Report saved: `{chosen_path}`")
                    open_in_explorer(chosen_path)
                
        with c2:
            st.markdown(f"""
            <div class="tool-window">
                <div class="tool-titlebar" style="margin-top:0;">Resampled Time-Series Export [.csv]</div>
                <p style="font-size: 13.5px; color: {THEME['text_muted']}; margin: 10px 0 14px 0;">Export synchronized signal traces configured in the Graphics window.</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Read signals using the exact key stored in Tab 1
            f_selected_signals = st.session_state.get(f"scope_signals_{target_export_file}", [])
            default_csv_name = f"signals_{os.path.splitext(target_export_file)[0]}.csv"
            
            if f_selected_signals:
                if st.button(f"Save Synchronized CSV ({len(f_selected_signals)} Signals)", use_container_width=True, key="btn_save_csv"):
                    chosen_path = ask_save_path(
                        default_filename=default_csv_name,
                        file_types=[("CSV Spreadsheet", "*.csv"), ("All Files", "*.*")]
                    )
                    if chosen_path:
                        combined_frames = {}
                        for s_name in f_selected_signals:
                            m_hex = signal_to_msg_hex[s_name]
                            df_s = exp_df[exp_df['CAN_ID'] == m_hex].copy()
                            df_s['Decoded'] = df_s['Payload'].apply(lambda x: decode_can_payload(m_hex, x, db))
                            df_s[s_name] = df_s['Decoded'].apply(lambda d: d.get(s_name) if isinstance(d, dict) else None)
                            combined_frames[s_name] = df_s[['Relative_Time_ms', s_name]].dropna(subset=[s_name])
                        
                        export_df = pd.DataFrame()
                        for s_name, s_df in combined_frames.items():
                            s_idx = s_df.set_index('Relative_Time_ms')
                            export_df = s_idx if export_df.empty else export_df.join(s_idx, how='outer')
                        export_df = export_df.ffill().reset_index()
                        
                        save_content(chosen_path, export_df.to_csv(index=False))
                        st.success(f"CSV saved: `{chosen_path}`")
                        open_in_explorer(chosen_path)
            else:
                st.info("Select signals in the Graphics window to enable CSV export.")

    # ==========================================
    # TAB 5: TRACE WINDOW [CAN / CAN FD]
    # ==========================================
    with tab_raw:
        st.markdown("<div style='margin-top: 14px;'></div>", unsafe_allow_html=True)
        # TAB HEADING: BIGGER & NOT BOLD
        st.markdown('<div class="tab-section-heading">CAN / CAN FD Frame Trace Inspector</div>', unsafe_allow_html=True)
        
        c_tr1, c_tr2 = st.columns([3, 2])
        with c_tr1:
            target_raw_file = st.radio(
                "Target Log Selection", 
                options=file_options, 
                horizontal=True, 
                key="raw_target_file",
                label_visibility="collapsed"
            )
        with c_tr2:
            payload_color_mode = st.selectbox(
                "Byte Field Highlighting Profile",
                ["Standard 2-Byte Words", "AUTOSAR / E2E Safety", "UDS / Diagnostic (ISO-TP)", "Monochrome (Off)"]
            )
        
        raw_df_preview = loaded_data[target_raw_file].head(500).copy()
        st.markdown(
            render_themed_table(raw_df_preview, payload_col="Payload", payload_mode=payload_color_mode), 
            unsafe_allow_html=True
        )
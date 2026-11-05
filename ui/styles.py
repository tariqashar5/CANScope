# ui/styles.py

THEME = {
    "bg_app": "#0F172A",           # Deep Slate Canvas
    "bg_sidebar": "#111827",       # Configuration Dock
    "bg_card": "#1E293B",          # Tool Window Pane
    "border_card": "#334155",      # Crisp Boundary Line
    "toolbar_bg": "#151F32",       # Ribbon Strip Background
    "input_bg": "#1E293B",         # Dropdown & Multiselect Background
    "input_border": "#475569",     # Form Outline
    "tag_bg": "#334155",           # Muted Tag Pill
    "tag_border": "#475569",       # Tag Border
    "tag_text": "#F8FAFC",         # Tag Label Text
    "text_main": "#F8FAFC",        # High-Contrast Pure Light Text
    "text_muted": "#94A3B8",       # Technical Subtitle Slate
    "accent": "#38BDF8",           # Precision Instrument Cyan
    "btn_bg": "#0284C7",           # Action Button Blue
    "btn_text": "#FFFFFF",         # Button Text White
    "table_header_bg": "#0B0F17",  # Table Header Slate
    "table_row_even": "#1E293B",
    "table_row_odd": "#172033",
    "plot_bg": "#0B0F17",          # Oscilloscope Deep Black Grid
    "plot_grid": "#1E293B",        # Raster Grid Lines
    "plot_axis": "#475569",
    "badge_pass_bg": "#064E3B",
    "badge_pass_fg": "#34D399",
    "badge_fail_bg": "#7F1D1D",
    "badge_fail_fg": "#F87171"
}

SIGNAL_COLORS = [
    "#38BDF8",  # Precision Cyan
    "#F87171",  # Signal Red
    "#34D399",  # Signal Green
    "#C084FC",  # Signal Purple
    "#FBBF24",  # Signal Amber
    "#2DD4BF",  # Signal Teal
    "#F472B6",  # Signal Pink
    "#94A3B8"   # Slate Iron
]

def get_theme_css():
    return f"""
    <style>
        /* --- HIDE STREAMLIT CHROME (DEPLOY BUTTON, MAIN MENU, FOOTER) --- */
        #MainMenu {{ visibility: hidden !important; display: none !important; }}
        footer {{ visibility: hidden !important; display: none !important; }}
        header[data-testid="stHeader"] {{ visibility: hidden !important; height: 0 !important; }}
        [data-testid="stToolbar"] {{ visibility: hidden !important; display: none !important; }}
        [data-testid="stDecoration"] {{ visibility: hidden !important; display: none !important; }}
        [data-testid="stStatusWidget"] {{ visibility: hidden !important; display: none !important; }}
        .stDeployButton {{ display: none !important; }}

        /* Base Desktop UI Typography */
        html, body, [class*="css"] {{
            font-family: "Segoe UI", -apple-system, BlinkMacSystemFont, "Tahoma", sans-serif !important;
            font-size: 14.5px !important;
            color: {THEME['text_main']};
        }}
        
        [data-testid="stAppViewContainer"] {{
            background-color: {THEME['bg_app']} !important;
        }}
        
        .block-container {{
            padding-top: 1.6rem !important;
            padding-bottom: 3rem !important;
            padding-left: 2.5rem !important;
            padding-right: 2.5rem !important;
            max-width: 98% !important;
        }}
        
        /* FIX 1: Dedicated Main App Header Class (Big & Centered) */
        .main-app-title {{
            font-size: 32px !important;
            font-weight: 800 !important;
            text-transform: uppercase !important;
            letter-spacing: 0.05em !important;
            color: #FFFFFF !important;
            text-align: center !important;
            margin: 0 0 6px 0 !important;
        }}
        
        /* FIX 2: Dedicated Tab Section Heading Class (Bigger & NOT Bold) */
        .tab-section-heading {{
            font-size: 24px !important;
            font-weight: 400 !important;
            color: #F8FAFC !important;
            letter-spacing: 0.01em !important;
            margin: 0 0 16px 0 !important;
            display: block !important;
        }}

        h3 {{
            font-size: 17px !important;
            font-weight: 600 !important;
            margin: 16px 0 10px 0 !important;
            color: {THEME['text_main']} !important;
        }}
        h4, label {{
            font-size: 15px !important;
            font-weight: 600 !important;
            color: {THEME['text_main']} !important;
        }}
        p, span {{
            font-size: 14px;
            color: {THEME['text_main']};
        }}
        .stCaption, small {{
            font-size: 13px !important;
            color: {THEME['text_muted']} !important;
            line-height: 1.5 !important;
        }}

        /* Sidebar Dock */
        section[data-testid="stSidebar"] {{
            background-color: {THEME['bg_sidebar']} !important;
            border-right: 1px solid {THEME['border_card']} !important;
            padding: 1.5rem 1.2rem !important;
        }}
        section[data-testid="stSidebar"] h2 {{
            font-size: 22px !important;
            font-weight: 800 !important;
            color: #FFFFFF !important;
            margin-bottom: 4px !important;
        }}
        section[data-testid="stSidebar"] label {{
            color: {THEME['text_main']} !important;
        }}
        
        /* Tool Windows */
        .tool-window {{
            background: {THEME['bg_card']};
            border: 1px solid {THEME['border_card']};
            border-radius: 6px;
            padding: 18px 22px;
            margin-bottom: 16px;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
        }}
        
        .tool-titlebar {{
            background: {THEME['toolbar_bg']};
            font-weight: 700;
            font-size: 12.5px;
            text-transform: uppercase;
            letter-spacing: 0.08em;
            padding: 10px 14px;
            border: 1px solid {THEME['border_card']};
            border-bottom: none;
            border-radius: 6px 6px 0 0;
            color: {THEME['accent']};
            margin-top: 14px;
        }}

        .metric-value {{
            font-family: Consolas, "Courier New", monospace !important;
            font-size: 2.2rem;
            font-weight: 800;
            color: {THEME['accent']} !important;
            line-height: 1.1;
            margin-top: 6px;
        }}
        .metric-label {{
            font-size: 11.5px;
            text-transform: uppercase;
            letter-spacing: 0.08em;
            font-weight: 700;
            color: {THEME['text_muted']} !important;
        }}

        /* Ribbon Tab Bar */
        div[data-baseweb="tab-list"] {{
            gap: 0px !important;
            background-color: {THEME['toolbar_bg']} !important;
            border: 1px solid {THEME['border_card']} !important;
            border-radius: 6px 6px 0 0 !important;
            padding: 0 !important;
            margin-top: 10px !important;
        }}
        
        button[data-baseweb="tab"] {{
            font-family: "Segoe UI", Tahoma, sans-serif !important;
            font-size: 14px !important;
            font-weight: 600 !important;
            padding: 12px 24px !important;
            color: {THEME['text_muted']} !important;
            border-radius: 0 !important;
            background: transparent !important;
            border: none !important;
            border-right: 1px solid {THEME['border_card']} !important;
            margin: 0 !important;
            transition: all 0.2s ease !important;
        }}
        button[data-baseweb="tab"]:last-child {{
            border-right: none !important;
        }}
        button[data-baseweb="tab"]:hover {{
            background: rgba(255, 255, 255, 0.04) !important;
            color: {THEME['text_main']} !important;
        }}
        button[data-baseweb="tab"][aria-selected="true"] {{
            color: {THEME['accent']} !important;
            background: {THEME['bg_card']} !important;
            box-shadow: inset 0 3px 0 0 {THEME['accent']} !important;
            border-bottom: 1px solid {THEME['bg_card']} !important;
        }}
        div[data-baseweb="tab-border"] {{
            display: none !important;
        }}

        /* Multiselect & Inputs */
        div[data-baseweb="select"] > div {{
            background-color: {THEME['input_bg']} !important;
            border: 1px solid {THEME['input_border']} !important;
            border-radius: 4px !important;
            padding: 4px 6px !important;
            color: {THEME['text_main']} !important;
        }}
        div[data-baseweb="select"] input {{
            color: {THEME['text_main']} !important;
        }}
        div[data-baseweb="select"] input::placeholder {{
            color: {THEME['text_muted']} !important;
            -webkit-text-fill-color: {THEME['text_muted']} !important;
            opacity: 1 !important;
        }}
        div[data-baseweb="select"] [class*="placeholder"] {{
            color: {THEME['text_muted']} !important;
            -webkit-text-fill-color: {THEME['text_muted']} !important;
        }}

        span[data-baseweb="tag"] {{
            background-color: {THEME['tag_bg']} !important;
            border: 1px solid {THEME['tag_border']} !important;
            border-radius: 3px !important;
            padding: 2px 6px !important;
        }}
        span[data-baseweb="tag"] span {{
            color: {THEME['tag_text']} !important;
            font-weight: 700 !important;
            font-size: 12.5px !important;
            font-family: Consolas, monospace !important;
        }}
        
        div[data-baseweb="popover"], div[data-baseweb="menu"], ul[role="listbox"] {{
            background-color: {THEME['input_bg']} !important;
            border: 1px solid {THEME['border_card']} !important;
            border-radius: 4px !important;
        }}
        li[role="option"] {{
            color: {THEME['text_main']} !important;
            background-color: {THEME['input_bg']} !important;
            font-size: 13.5px !important;
            padding: 8px 14px !important;
        }}
        li[role="option"]:hover, li[aria-selected="true"] {{
            background-color: {THEME['tag_bg']} !important;
        }}

        /* Action Buttons */
        button[kind="primary"], 
        button[kind="secondary"], 
        div.stButton > button, 
        div.stDownloadButton > button,
        button[data-testid="baseButton-secondary"],
        button[data-testid="baseButton-primary"] {{
            background-color: {THEME['btn_bg']} !important;
            color: #FFFFFF !important;
            border: 1px solid {THEME['border_card']} !important;
            font-weight: 700 !important;
            font-size: 13.5px !important;
            border-radius: 4px !important;
            padding: 10px 22px !important;
            transition: all 0.2s ease !important;
        }}
        div.stDownloadButton > button *,
        div.stButton > button * {{
            color: #FFFFFF !important;
            -webkit-text-fill-color: #FFFFFF !important;
        }}
        div.stDownloadButton > button:hover,
        div.stButton > button:hover {{
            filter: brightness(1.2) !important;
            box-shadow: 0 2px 8px rgba(2, 132, 199, 0.4) !important;
        }}

        /* Sidebar File Uploaders */
        section[data-testid="stSidebar"] div[data-testid="stFileUploader"] {{
            margin-top: 0px !important;
            margin-bottom: 12px !important;
        }}
        section[data-testid="stSidebar"] div[data-testid="stFileUploader"] section[data-testid="stFileUploaderDropzone"] {{
            background-color: {THEME['input_bg']} !important;
            border: 1px dashed {THEME['input_border']} !important;
            border-radius: 0 0 6px 6px !important;
            padding: 14px 12px !important;
        }}
        section[data-testid="stSidebar"] div[data-testid="stFileUploader"] section[data-testid="stFileUploaderDropzone"] * {{
            color: {THEME['text_muted']} !important;
        }}
        section[data-testid="stSidebar"] div[data-testid="stFileUploader"] section[data-testid="stFileUploaderDropzone"] button {{
            background-color: {THEME['tag_bg']} !important;
            color: {THEME['text_main']} !important;
            border: 1px solid {THEME['border_card']} !important;
            font-size: 12.5px !important;
            padding: 5px 14px !important;
            border-radius: 3px !important;
        }}

        div[data-testid="stFileUploaderFile"] {{
            background-color: {THEME['bg_card']} !important;
            border: 1px solid {THEME['border_card']} !important;
            border-radius: 4px !important;
            margin-top: 6px !important;
            padding: 8px 12px !important;
        }}
        div[data-testid="stFileUploaderFile"] * {{
            color: {THEME['text_main']} !important;
            font-weight: 700 !important;
        }}
        div[data-testid="stFileUploaderFile"] svg {{
            fill: {THEME['text_main']} !important;
        }}

        /* Data Tables */
        .custom-table-container {{
            background: {THEME['bg_card']};
            border: 1px solid {THEME['border_card']};
            border-radius: 6px;
            overflow-x: auto;
            margin-top: 14px;
            margin-bottom: 20px;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
        }}
        table.custom-table {{
            width: 100%;
            border-collapse: collapse;
            font-size: 13px;
            font-family: Consolas, "Segoe UI", monospace;
            color: {THEME['text_main']};
        }}
        table.custom-table th {{
            background-color: {THEME['table_header_bg']};
            color: {THEME['text_main']};
            font-weight: 700;
            text-transform: uppercase;
            font-size: 11.5px;
            letter-spacing: 0.05em;
            padding: 10px 14px;
            border: 1px solid {THEME['border_card']};
            text-align: left;
        }}
        table.custom-table td {{
            padding: 8px 14px;
            border: 1px solid {THEME['border_card']};
            color: {THEME['text_main']};
        }}
        table.custom-table tr:nth-child(even) {{
            background-color: {THEME['table_row_even']};
        }}
        table.custom-table tr:nth-child(odd) {{
            background-color: {THEME['table_row_odd']};
        }}

        /* Raw Frame Byte Chips */
        .byte-chip {{
            display: inline-block;
            padding: 2px 5px;
            margin: 1px;
            border-radius: 3px;
            font-family: Consolas, monospace;
            font-size: 12.5px;
            font-weight: 700;
        }}
        .byte-header-1 {{ background: rgba(56, 189, 248, 0.2); color: #38BDF8; border: 1px solid rgba(56, 189, 248, 0.4); }}
        .byte-header-2 {{ background: rgba(167, 139, 250, 0.2); color: #A78BFA; border: 1px solid rgba(167, 139, 250, 0.4); }}
        .byte-data-1   {{ background: rgba(52, 211, 153, 0.2); color: #34D399; border: 1px solid rgba(52, 211, 153, 0.4); }}
        .byte-data-2   {{ background: rgba(251, 191, 36, 0.2); color: #FBBF24; border: 1px solid rgba(251, 191, 36, 0.4); }}
        .byte-safety   {{ background: rgba(244, 114, 182, 0.2); color: #F472B6; border: 1px solid rgba(244, 114, 182, 0.4); }}
        .byte-padding  {{ background: rgba(148, 163, 184, 0.1); color: #64748B; border: 1px solid rgba(148, 163, 184, 0.2); }}
    </style>
    """
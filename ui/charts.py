# ui/charts.py
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from src.decoder import decode_can_payload

SIGNAL_PALETTE = [
    "#38bdf8", "#4ade80", "#f59e0b", "#f43f5e", 
    "#a855f7", "#06b6d4", "#ec4899", "#10b981"
]

def build_oscilloscope_figure(df, selected_signals, signal_to_msg_hex, signal_choices, db):    
    if not selected_signals or df is None or df.empty:
        return go.Figure()

    # Deduplicate strictly
    unique_signals = []
    for s in selected_signals:
        if s not in unique_signals:
            unique_signals.append(s)
            
    num_signals = len(unique_signals)

    fig = make_subplots(
        rows=num_signals,
        cols=1,
        shared_xaxes=True,
        vertical_spacing=0.08,
        subplot_titles=[f"<b>{s}</b>" for s in unique_signals]
    )

    for row_idx, s_name in enumerate(unique_signals, start=1):
        color = SIGNAL_PALETTE[(row_idx - 1) % len(SIGNAL_PALETTE)]
        m_hex = signal_to_msg_hex.get(s_name)

        if not m_hex:
            continue

        msg_df = df[df["CAN_ID"] == m_hex]
        times = []
        vals = []

        for _, row in msg_df.iterrows():
            payload = row.get("Payload")
            rel_time = row.get("Relative_Time_ms")
            if payload is None or rel_time is None:
                continue

            decoded = decode_can_payload(m_hex, payload, db)
            if isinstance(decoded, dict) and s_name in decoded:
                v = decoded[s_name]
                if v is not None:
                    times.append(rel_time)
                    vals.append(v)

        is_discrete = len(vals) > 0 and isinstance(vals[0], str)
        line_shape = "hv" if is_discrete else "linear"

        # Add single trace per row
        fig.add_trace(
            go.Scatter(
                x=times,
                y=vals,
                mode="lines",
                name=s_name,
                line=dict(color=color, width=2, shape=line_shape)
            ),
            row=row_idx,
            col=1
        )

    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(15,23,42,0.6)",
        height=max(280, 220 * num_signals),
        showlegend=False,
        margin=dict(l=60, r=30, t=30, b=30)
    )

    return fig
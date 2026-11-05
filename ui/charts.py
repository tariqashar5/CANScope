# ui/charts.py
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
from ui.styles import SIGNAL_COLORS, THEME
from src.decoder import extract_signal_timeseries

def build_oscilloscope_figure(
    df: pd.DataFrame, 
    selected_signals: list, 
    signal_to_msg_hex: dict, 
    signal_choices: dict, 
    db
) -> go.Figure:
    """
    Renders an oscilloscope graph with clean signal names and zero title overlap.
    """
    num_sigs = len(selected_signals)
    if num_sigs == 0:
        return go.Figure()

    # Vertical spacing prevents tracks from crowding headers
    fig = make_subplots(
        rows=num_sigs, cols=1,
        shared_xaxes=True,
        vertical_spacing=max(0.12, 0.26 / num_sigs),
        subplot_titles=[f"<b>{sig}</b>" for sig in selected_signals]
    )

    for s_idx, s_name in enumerate(selected_signals, 1):
        df_plot = extract_signal_timeseries(df, s_name, signal_to_msg_hex, db)
        trace_color = SIGNAL_COLORS[(s_idx - 1) % len(SIGNAL_COLORS)]
        
        is_discrete = s_name in signal_choices or (not df_plot.empty and df_plot[s_name].dtype == object)

        if not df_plot.empty:
            fig.add_trace(
                go.Scatter(
                    x=df_plot['Relative_Time_ms'],
                    y=df_plot[s_name],
                    mode='lines+markers',
                    line=dict(
                        color=trace_color,
                        width=1.5,
                        shape='hv' if is_discrete else 'linear'
                    ),
                    marker=dict(size=3.5, color=trace_color),
                    name=s_name
                ),
                row=s_idx, col=1
            )

        # Technical Y-Axis
        y_conf = dict(
            showline=True, 
            linewidth=1, 
            linecolor=THEME['plot_axis'], 
            mirror=True,
            showgrid=True, 
            gridcolor=THEME['plot_grid'], 
            gridwidth=1,
            zeroline=False,
            tickfont=dict(family="Consolas, monospace", size=10, color=THEME['text_muted'])
        )
        if s_name in signal_choices:
            y_conf.update(dict(categoryarray=signal_choices[s_name], type='category'))
        fig.update_yaxes(**y_conf, row=s_idx, col=1)

        # Technical X-Axis
        fig.update_xaxes(
            showline=True, 
            linewidth=1, 
            linecolor=THEME['plot_axis'], 
            mirror=True,
            showgrid=True, 
            gridcolor=THEME['plot_grid'],
            gridwidth=1,
            showspikes=True, 
            spikemode="across", 
            spikesnap="cursor",
            spikethickness=1, 
            spikedash="solid", 
            spikecolor=THEME['accent'],
            rangeslider=dict(visible=False),
            ticksuffix=" ms",
            tickfont=dict(family="Consolas, monospace", size=10, color=THEME['text_muted']),
            row=s_idx, col=1
        )

    # Shift titles above the coordinate box line
    for annotation in fig['layout']['annotations']:
        annotation['font'] = dict(family="Segoe UI, Tahoma, sans-serif", size=11, color=THEME['text_main'])
        annotation['x'] = 0.005
        annotation['xanchor'] = 'left'
        annotation['yanchor'] = 'bottom'
        annotation['yshift'] = 14

    fig.update_layout(
        height=max(220 * num_sigs, 280),
        showlegend=False,
        hovermode="x unified",
        margin=dict(l=45, r=45, t=48, b=25),
        plot_bgcolor=THEME['plot_bg'],
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Segoe UI, Tahoma, sans-serif", color=THEME['text_muted'])
    )
    return fig
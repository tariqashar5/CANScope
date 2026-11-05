# src/diagnostics.py
import pandas as pd

def calculate_network_health(df):
    """Calculates mean, min, max cycle times and jitter for periodic frames."""
    records = []
    grouped = df.groupby(['CAN_ID', 'Message_Name'], observed=True)
    
    for (can_id, msg_name), group in grouped:
        if len(group) > 3:
            diffs_ms = group['Relative_Time_ms'].diff().dropna()
            mean_cycle = diffs_ms.mean()
            min_cycle = diffs_ms.min()
            max_cycle = diffs_ms.max()
            jitter = max_cycle - min_cycle
            dropped_frames = int((diffs_ms > (mean_cycle * 1.8)).sum())
            
            verdict = "FAIL" if (dropped_frames > 0 or jitter > 15) else "PASS"
            
            records.append({
                "CAN ID": f"0x{can_id}",
                "Message Name": msg_name,
                "Frames": len(group),
                "Mean Cycle [ms]": round(mean_cycle, 2),
                "Min Cycle [ms]": round(min_cycle, 2),
                "Max Cycle [ms]": round(max_cycle, 2),
                "Jitter [ms]": round(jitter, 2),
                "Dropped Frames": dropped_frames,
                "Verdict": verdict
            })
            
    return pd.DataFrame(records).sort_values(by=["Dropped Frames", "Jitter [ms]"], ascending=False) if records else pd.DataFrame()

def evaluate_alive_counters(df, counter_signals, signal_to_msg_hex, db, decode_payload_fn, get_msg_name_fn):
    """Audits functional safety alive counters for freezes and sequence skips."""
    audit_records = []
    for counter_sig in counter_signals:
        msg_hex = signal_to_msg_hex[counter_sig]
        df_sub = df[df['CAN_ID'] == msg_hex].copy()
        df_sub['Decoded'] = df_sub['Payload'].apply(lambda x: decode_payload_fn(msg_hex, x, db))
        df_sub[counter_sig] = pd.to_numeric(
            df_sub['Decoded'].apply(lambda d: d.get(counter_sig) if isinstance(d, dict) else None),
            errors='coerce'
        )
        df_sub = df_sub.dropna(subset=[counter_sig])
        
        if len(df_sub) > 2:
            vals = df_sub[counter_sig].values
            freeze_count = 0
            skip_count = 0
            
            for j in range(1, len(vals)):
                delta = vals[j] - vals[j-1]
                if delta == 0:
                    freeze_count += 1
                elif delta > 1:
                    skip_count += 1
                    
            verdict = "PASS" if (freeze_count == 0 and skip_count == 0) else "FAIL"
            
            audit_records.append({
                "Signal": counter_sig,
                "Message": get_msg_name_fn(msg_hex, db),
                "Sample Count": len(vals),
                "Freeze Count": freeze_count,
                "Skip Count": skip_count,
                "Verdict": verdict
            })
            
    return pd.DataFrame(audit_records)

def detect_state_transitions(df, trigger_signals, signal_to_msg_hex, db, decode_payload_fn):
    """Extracts exact timestamps for discrete state flips across state-machine signals."""
    events = []
    for sig in trigger_signals:
        msg_hex = signal_to_msg_hex[sig]
        df_sub = df[df['CAN_ID'] == msg_hex].copy()
        df_sub['Decoded'] = df_sub['Payload'].apply(lambda x: decode_payload_fn(msg_hex, x, db))
        df_sub[sig] = df_sub['Decoded'].apply(lambda d: d.get(sig) if isinstance(d, dict) else None)
        df_sub = df_sub.dropna(subset=[sig])
        
        diff_mask = df_sub[sig] != df_sub[sig].shift()
        trans_df = df_sub[diff_mask].copy()
        
        for idx in range(1, len(trans_df)):
            prev = trans_df[sig].iloc[idx - 1]
            curr = trans_df[sig].iloc[idx]
            t = trans_df['Relative_Time_ms'].iloc[idx]
            events.append({
                "Time [ms]": round(t, 2),
                "Signal": sig,
                "State Transition": f"{prev} -> {curr}",
                "New State": curr
            })
            
    return pd.DataFrame(events).sort_values(by="Time [ms]") if events else pd.DataFrame()
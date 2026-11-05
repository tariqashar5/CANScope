# src/decoder.py
import cantools
import pandas as pd

def load_dbc_database(dbc_path: str):
    """Loads and compiles a .dbc database file."""
    return cantools.database.load_file(dbc_path)

def extract_dbc_indices(db):
    """
    Scans the database and builds:
      - signal_to_msg_hex: mapping of signal names to frame hex IDs.
      - signal_choices: discrete state mappings (e.g., 'D', 'P', 'R').
      - alive_counter_candidates: detected safety/rolling counters.
    """
    signal_to_msg_hex = {}
    signal_choices = {}
    alive_counter_candidates = []

    for msg in db.messages:
        msg_hex = hex(msg.frame_id)[2:].upper()
        for sig in msg.signals:
            signal_to_msg_hex[sig.name] = msg_hex
            if sig.choices:
                signal_choices[sig.name] = [str(val) for val in sig.choices.values()]
            
            sig_lower = sig.name.lower()
            if any(tag in sig_lower for tag in ["alv", "cnt", "counter", "rolling"]) and "crc" not in sig_lower:
                alive_counter_candidates.append(sig.name)

    return signal_to_msg_hex, signal_choices, alive_counter_candidates

def get_message_name_by_hex(can_id_hex: str, database) -> str:
    """Translates a hexadecimal CAN frame ID to its DBC symbolic message name."""
    if database is None:
        return "Unknown"
    try:
        return database.get_message_by_frame_id(int(can_id_hex, 16)).name
    except KeyError:
        return "Unknown ID"

def decode_can_payload(can_id_hex: str, payload_str: str, database):
    """Decodes a space-delimited hex payload string into clean physical signal values."""
    if database is None:
        return None
    try:
        data_bytes = bytes.fromhex(payload_str)
        decoded = database.decode_message(int(can_id_hex, 16), data_bytes)
        clean_dict = {}
        for key, value in decoded.items():
            if type(value).__name__ == 'NamedSignalValue':
                clean_dict[key] = str(value)
            else:
                clean_dict[key] = value
        return clean_dict
    except Exception:
        return None

def extract_signal_timeseries(df: pd.DataFrame, signal_name: str, signal_to_msg_hex: dict, db):
    """
    Extracts, decodes, and returns a sanitized [Relative_Time_ms, signal_name] DataFrame.
    """
    msg_hex = signal_to_msg_hex.get(signal_name)
    if not msg_hex:
        return pd.DataFrame()
        
    df_msg = df[df['CAN_ID'] == msg_hex].copy()
    if df_msg.empty:
        return pd.DataFrame()
        
    df_msg['Decoded'] = df_msg['Payload'].apply(lambda x: decode_can_payload(msg_hex, x, db))
    df_msg[signal_name] = df_msg['Decoded'].apply(lambda d: d.get(signal_name) if isinstance(d, dict) else None)
    return df_msg[['Relative_Time_ms', signal_name]].dropna(subset=[signal_name]).copy()
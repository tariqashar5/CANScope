import pandas as pd
import can
import os

def parse_asc_file(file_path):
    """Parses a standard Vector .asc log file with low memory overhead."""
    timestamps = []
    channels = []
    can_ids = []
    directions = []
    dlcs = []
    payloads = []
    
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith(('date', 'base', 'internal', 'Begin', 'End', '//')):
                continue
            
            parts = line.split()
            if 'd' in parts and len(parts) >= 6:
                try:
                    timestamps.append(float(parts[0]))
                    channels.append(parts[1])
                    can_ids.append(parts[2].upper())
                    directions.append(parts[3])
                    dlc = int(parts[5])
                    dlcs.append(dlc)
                    payloads.append(" ".join(parts[6:6+dlc]))
                except ValueError:
                    continue

    df = pd.DataFrame({
        "Timestamp": timestamps,
        "Channel": pd.Categorical(channels),
        "CAN_ID": pd.Categorical(can_ids),
        "Direction": pd.Categorical(directions),
        "DLC": pd.Series(dlcs, dtype='uint8'),
        "Payload": payloads
    })
    return df

def parse_blf_file(file_path):
    """Parses a Vector .blf binary log file using compact categorical structures."""
    timestamps = []
    channels = []
    can_ids = []
    directions = []
    dlcs = []
    payloads = []
    
    with can.BLFReader(file_path) as reader:
        for msg in reader:
            if getattr(msg, 'is_error_frame', False):
                continue
            
            timestamps.append(msg.timestamp)
            channels.append(str(msg.channel))
            can_ids.append(hex(msg.arbitration_id)[2:].upper())
            directions.append("Rx" if msg.is_rx else "Tx")
            dlcs.append(msg.dlc)
            payloads.append(" ".join([f"{b:02X}" for b in msg.data]))
            
    df = pd.DataFrame({
        "Timestamp": timestamps,
        "Channel": pd.Categorical(channels),
        "CAN_ID": pd.Categorical(can_ids),
        "Direction": pd.Categorical(directions),
        "DLC": pd.Series(dlcs, dtype='uint8'),
        "Payload": payloads
    })
    return df

def parse_can_log(file_path):
    """Wrapper function to choose the right parser based on file extension."""
    ext = os.path.splitext(file_path)[1].lower()
    if ext == '.asc':
        return parse_asc_file(file_path)
    elif ext == '.blf':
        return parse_blf_file(file_path)
    else:
        raise ValueError(f"Unsupported file format: {ext}. Please use .asc or .blf")
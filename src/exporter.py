# src/exporter.py
import os
import subprocess
import platform

def ask_save_path(default_filename, file_types):
    if platform.system() != "Windows":
        return os.path.join(os.path.expanduser("~"), "Downloads", default_filename)

    filter_parts = []
    for desc, ext in file_types:
        filter_parts.append(f"{desc} ({ext})|{ext}")
    filter_string = "|".join(filter_parts)

    initial_dir = os.path.join(os.path.expanduser("~"), "Downloads").replace("\\", "\\\\")

    ps_cmd = (
        f"Add-Type -AssemblyName System.Windows.Forms; "
        f"$dlg = New-Object System.Windows.Forms.SaveFileDialog; "
        f"$dlg.Title = 'Save As'; "
        f"$dlg.InitialDirectory = '{initial_dir}'; "
        f"$dlg.FileName = '{default_filename}'; "
        f"$dlg.Filter = '{filter_string}'; "
        f"$dlg.TopMost = $true; "
        f"if ($dlg.ShowDialog() -eq [System.Windows.Forms.DialogResult]::OK) {{ $dlg.FileName }}"
    )

    try:
        result = subprocess.run(
            ["powershell", "-NoProfile", "-Command", ps_cmd],
            capture_output=True,
            text=True,
            creationflags=subprocess.CREATE_NO_WINDOW if hasattr(subprocess, 'CREATE_NO_WINDOW') else 0
        )
        selected_path = result.stdout.strip()
        print(f"[DEBUG] Dialog output path: '{selected_path}'")
        return selected_path if selected_path else None
    except Exception as e:
        print(f"[DEBUG] Dialog error: {e}")
        return None

def open_in_explorer(file_path):
    if platform.system() == "Windows" and file_path and os.path.exists(file_path):
        try:
            subprocess.Popen(f'explorer /select,"{os.path.abspath(file_path)}"')
        except Exception:
            pass

def save_content(file_path, content_data):
    if not file_path:
        return False
    mode = "wb" if isinstance(content_data, (bytes, bytearray)) else "w"
    encoding = None if "b" in mode else "utf-8"
    with open(file_path, mode, encoding=encoding) as f:
        f.write(content_data)
    return True
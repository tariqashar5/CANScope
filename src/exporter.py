# src/exporter.py
import os
import subprocess
import platform

def _open_dialog(default_filename, file_types):
    import tkinter as tk
    from tkinter import filedialog
    
    root = tk.Tk()
    root.withdraw()
    root.attributes("-topmost", True)
    
    initial_dir = os.path.join(os.path.expanduser("~"), "Downloads")
    
    # Ensure correct format for tkinter filetypes
    tk_types = [(desc, ext) for desc, ext in file_types]
    def_ext = file_types[0][1].replace("*", "") if file_types else ""

    chosen = filedialog.asksaveasfilename(
        parent=root,
        initialdir=initial_dir,
        initialfile=default_filename,
        title="Save As",
        filetypes=tk_types,
        defaultextension=def_ext
    )
    root.destroy()
    return chosen if chosen else None

def ask_save_path(default_filename, file_types):
    """Safely opens native Save As dialog."""
    try:
        return _open_dialog(default_filename, file_types)
    except Exception as e:
        print(f"File dialog fallback: {e}")
        return os.path.join(os.path.expanduser("~"), "Downloads", default_filename)

def open_in_explorer(file_path):
    """Highlights the saved file in Windows Explorer."""
    if platform.system() == "Windows" and file_path and os.path.exists(file_path):
        try:
            subprocess.Popen(f'explorer /select,"{os.path.abspath(file_path)}"')
        except Exception:
            pass

def save_content(file_path, content_data):
    """Writes string or byte payload directly to the specified file path."""
    if not file_path:
        return False
        
    mode = "wb" if isinstance(content_data, (bytes, bytearray)) else "w"
    encoding = None if "b" in mode else "utf-8"
    
    with open(file_path, mode, encoding=encoding) as f:
        f.write(content_data)
    return True
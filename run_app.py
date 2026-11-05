# run_app.py
import sys
import os
import time
import signal
import threading
import urllib.request

# --- 1. HOTFIX: Mock importlib metadata for frozen Streamlit bundle ---
import importlib.metadata

try:
    importlib.metadata.version("streamlit")
except Exception:
    class MockDist:
        version = "1.35.0"

    _orig_distribution = importlib.metadata.distribution
    def _safe_distribution(dist_name):
        if dist_name == "streamlit":
            return MockDist()
        return _orig_distribution(dist_name)

    _orig_version = importlib.metadata.version
    def _safe_version(dist_name):
        if dist_name == "streamlit":
            return "1.35.0"
        return _orig_version(dist_name)

    importlib.metadata.distribution = _safe_distribution
    importlib.metadata.version = _safe_version

# --- 2. HOTFIX: Bypass Windows signal handler check in background threads ---
_original_signal = signal.signal

def _patched_signal(signalnum, handler):
    try:
        return _original_signal(signalnum, handler)
    except ValueError:
        # Ignore 'signal only works in main thread of the main interpreter'
        return None

signal.signal = _patched_signal
# --------------------------------------------------------------------------

import webview
import streamlit.web.cli as stcli

SERVER_PORT = 8501
SERVER_URL = f"http://127.0.0.1:{SERVER_PORT}"

def resolve_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_path, relative_path)

def wait_for_server(url, timeout=30.0):
    """Polls local server until health endpoint confirms active status."""
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            with urllib.request.urlopen(f"{url}/_stcore/health", timeout=1) as response:
                if response.status == 200:
                    return True
        except Exception:
            time.sleep(0.2)
    return False

def start_streamlit_server(app_path):
    sys.argv = [
        "streamlit",
        "run",
        app_path,
        "--global.developmentMode=false",
        "--server.headless=true",
        "--server.address=127.0.0.1",
        f"--server.port={SERVER_PORT}",
        "--browser.gatherUsageStats=false",
        "--server.enableCORS=false",
        "--server.enableXsrfProtection=false"
    ]
    stcli.main()

if __name__ == "__main__":
    app_main_path = resolve_path("app.py")

    # 1. Start Streamlit in worker thread (now safe from signal.signal crash)
    server_thread = threading.Thread(
        target=start_streamlit_server,
        args=(app_main_path,),
        daemon=True
    )
    server_thread.start()

    # 2. Block until the Streamlit server finishes booting and answers HTTP
    server_ready = wait_for_server(SERVER_URL, timeout=25.0)

    # 3. Create native desktop window
    window = webview.create_window(
        title="CANscope - CAN Protocol Analyzer & Telemetry Suite",
        url=SERVER_URL,
        width=1500,
        height=920,
        resizable=True,
        min_size=(1024, 700)
    )

    # 4. Start GUI event loop
    webview.start(debug=False)
    sys.exit(0)
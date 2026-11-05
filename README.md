# CANscope — Automotive CAN / CAN FD Diagnostic & Telemetry Suite

[![Platform: Windows](https://img.shields.io/badge/Platform-Windows-blue.svg)](https://github.com/tariqashar5/CANScope)
[![Python: 3.10+](https://img.shields.io/badge/Python-3.10%2B-brightgreen.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Domain: Automotive](https://img.shields.io/badge/Domain-ISO%2026262%20%7C%20CAN%20FD-orange.svg)]()

**CANscope** is a standalone, license-free desktop diagnostic and telemetry workbench designed for automotive systems engineers, ECU software developers, and test engineers. It enables rapid post-test analysis, physical signal decoding, and network verification without relying on proprietary commercial software licenses (such as Vector CANoe/CANalyzer).

---

## Key Features

- **Zero-License Operation:** Runs offline on Windows as an air-gapped desktop workstation without external license servers or hardware dongles.
- **Trace & Network Matrix Ingestion:** Direct parsing of Vector `.blf` and `.asc` trace logs alongside `.dbc` communication databases.
- **Multi-Trace Oscilloscope:** Synchronized multi-channel waveform viewing with comparison columns to benchmark runs against reference traces.
- **Timing & Jitter Auditing:** Automated calculation of frame cycle periodicity ($T_{\text{actual}}$ vs. $T_{\text{nominal}}$), transmission jitter, and dropped packet detection.
- **Functional Safety (ISO 26262):** Automated alive-counter sequence integrity audits (freeze/skip fault detection) and discrete state-machine transition logging.
- **Protocol Inspection:** Raw CAN / CAN FD frame inspector with domain-specific payload color mapping (AUTOSAR E2E, UDS/ISO-TP, Standard byte pairs).
- **Report & Data Export:** Automated HTML compliance verification test reports and resampled, time-aligned CSV exports.

---

## Architecture & System Workflow

```
+--------------------+      +--------------------+
|   DBC Matrix File  |      | BLF / ASC Log File |
+---------+----------+      +---------+----------+
          |                           |
          +------------+--------------+
                       |
                       v
             [ CANscope Core Engine ]
                       |
     +-----------------+-----------------+-----------------+
     |                 |                 |                 |
     v                 v                 v                 v
Waveform Plots    Timing/Jitter    Safety Checks     HTML Reports
```

---

## Workspace Layout

| Tab | Purpose | Key Capabilities |
| :--- | :--- | :--- |
| **Graphics [Measurement]** | Oscilloscope & Signal Decoding | Synchronized analog waveforms, multi-trace comparisons, interactive zooming and tooltips |
| **Bus Statistics** | Network Health & Jitter | Cycle times, jitter ($\Delta t$), message drop detection, Pass/Fail thresholds |
| **Trace & ASIL Analysis** | Functional Safety (ISO 26262) | E2E rolling counter audits, discrete state-machine transition timelines |
| **Logging & Export Setup** | Archival & Data Interchange | One-click HTML verification reports, resampled synchronized CSV exports |
| **Trace Window** | Frame-Level Diagnostics | Chronological CAN/CAN FD traffic, DLC/hex inspections, payload coloring |

---
> For complete step-by-step operating instructions, ISO 26262 audit specifications, and troubleshooting, refer to the [CANscope User & Operations Manual](docs/CANscope User & Operations Manual.pdf).

## Quick Start (Pre-Compiled Executable)

1. Navigate to the **[Releases](../../releases)** tab on GitHub.
2. Download the latest `CANscope_win64.zip`.
3. Extract the archive to any local directory.
4. Launch **`CANscope.exe`** (no Python runtime or environment setup required).

---

## Developer Setup (Run from Source)

If you wish to inspect the codebase, run from source, or contribute:

### 1. Clone the Repository
```bash
git clone https://github.com/tariqashar5/CANScope.git
cd CANScope
```

### 2. Create and Activate Virtual Environment
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### 3. Install Dependencies
```powershell
pip install -r requirements.txt
```

### 4. Run the Desktop Application
```powershell
python run_app.py
```

---

## Building the Standalone Executable

CANscope bundles its runtime via PyInstaller and PyWebView into a self-contained Windows executable:

```powershell
pyinstaller --clean CANscope.spec
```

The resulting distribution folder is created at `dist/CANscope/`.

---

## Verification & Trace Compatibility

- **Vector Formats:** `.blf` (Binary Logging Format), `.asc` (ASCII Bus Logging)
- **Database:** CAN / CAN FD `.dbc` network matrix definition files
- **Standard Conformance:** ISO 11898-1 (Classical CAN), ISO 11898-2 (CAN FD), ISO 26262 (E2E alive counters)

---

## Contributing

Contributions to support additional trace formats, diagnostic protocols (e.g., UDS/DoIP), or UI enhancements are welcome. Please refer to [CONTRIBUTING.md](CONTRIBUTING.md) for branch management and pull request guidelines.

---

## License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.
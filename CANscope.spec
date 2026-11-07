# -*- mode: python ; coding: utf-8 -*-
from PyInstaller.utils.hooks import collect_data_files, collect_submodules, copy_metadata

datas = [
    ('src', 'src'),
    ('ui', 'ui'),
    ('app.py', '.')
]

datas += collect_data_files('streamlit')
datas += collect_data_files('cantools')
datas += collect_data_files('plotly')
datas += collect_data_files('webview')
datas += collect_data_files('pyarrow')
datas += copy_metadata('streamlit')
datas += copy_metadata('cantools')
datas += copy_metadata('pyarrow')

hiddenimports = [
    'tkinter',
    'tkinter.filedialog',
    'src.exporter',
    'streamlit',
    'streamlit.web.cli',
    'streamlit.runtime.scriptrunner.magic_expressions',
    'cantools',
    'plotly',
    'pandas',
    'numpy',
    'pyarrow',
    'can',
    'can.io.blf',
    'can.io.asc',
    'webview',
    'clr'
]
hiddenimports += collect_submodules('streamlit')
hiddenimports += collect_submodules('cantools')
hiddenimports += collect_submodules('plotly')
hiddenimports += collect_submodules('webview')
hiddenimports += collect_submodules('pyarrow')

block_cipher = None

# Ensure the entry file matches your root script (run_app.py or app.py)
entry_script = 'run_app.py'

a = Analysis(
    [entry_script],
    pathex=[],
    binaries=[],
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=['matplotlib', 'scipy', 'pytest'],  # Removed tkinter from here
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='CANscope',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,  # Set to False to prevent permission/EDR locks
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=False,
    upx_exclude=[],
    name='CANscope',
)
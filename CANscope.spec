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
datas += copy_metadata('streamlit')
datas += copy_metadata('cantools')

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

block_cipher = None

a = Analysis(
    ['run_app.py'],
    pathex=[],
    binaries=[],
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=['matplotlib', 'scipy', 'tkinter', 'pytest'],
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
    upx=True,
    console=False,  # Set to False so NO black terminal pops up
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
    upx=True,
    upx_exclude=[],
    name='CANscope',
)
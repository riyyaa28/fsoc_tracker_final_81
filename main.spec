# -*- mode: python ; coding: utf-8 -*-
# Windows desktop build:  pyinstaller main.spec
# Output: dist/FSOC Control Center/FSOC Control Center.exe (one folder; copy or
# zip the whole folder). A one-file build is avoided on purpose: with torch
# inside it would unpack ~2 GB to a temp folder on every start.

from PyInstaller.utils.hooks import collect_data_files

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('ui/web3d', 'ui/web3d'),
        ('node_modules/three/build', 'node_modules/three/build'),
        ('beacon_yolo.pt', '.'),
    ] + collect_data_files('ultralytics'),      # model / tracker config files YOLO reads at run time
    hiddenimports=[
        'PyQt5.QtWebEngineWidgets',
        'PyQt5.QtWebEngineCore',
        'PyQt5.QtWebChannel',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=['tkinter'],
    noarchive=False,
    optimize=0,
)

# PyQt5 ships an old (14.26) MSVC runtime in Qt5/bin. If torch resolves against
# it, c10.dll fails with WinError 1114 at start-up. Drop those copies so Qt and
# torch both use the newer runtime PyInstaller places in the bundle root.
_old_qt_runtime = {'msvcp140.dll', 'msvcp140_1.dll', 'vcruntime140.dll', 'vcruntime140_1.dll'}
a.binaries = [
    b for b in a.binaries
    if not (b[0].replace('\\', '/').lower().startswith('pyqt5/qt5/bin/')
            and b[0].replace('\\', '/').rsplit('/', 1)[-1].lower() in _old_qt_runtime)
]

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='FSOC Control Center',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,                  # UPX can corrupt the torch / Qt DLLs
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
    a.datas,
    strip=False,
    upx=False,
    name='FSOC Control Center',
)

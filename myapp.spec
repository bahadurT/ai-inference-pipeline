from PyInstaller.building.build_main import Analysis, PYZ, EXE, COLLECT

binaries = [
    # Add more CUDA libraries as needed
]

datas = [
    # Include all necessary data files
    ('boxmot/appearance/backbones/clip/clip/bpe_simple_vocab_16e6.txt.gz', 'boxmot/appearance/backbones/clip/clip'),
    # Add more data files as needed
]

hiddenimports = [
    'torch',
    'torchaudio',
    'GiStream',
    'boxmot',
]

# Adding the CUDA library paths and any other necessary paths to pathex
a = Analysis(
    ['GiStream.py'],
    pathex=[
        'gistreamer',
        '/usr/local/lib'
    ],
    binaries=binaries,
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=['./hooks'],  # Ensure the path to custom hooks
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,  # Ensure that binaries are not included here
    name='gistream',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
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
    name='gistream'
)

# -*- mode: python ; coding: utf-8 -*-

from PyInstaller.building.build_main import Analysis, PYZ, EXE
import PyInstaller

# This will only package the shared libraries from torchaudio and torch
a = Analysis(
    [],
    pathex=['gistream'],
    binaries=[
        ('env_gi/lib/python3.8/site-packages/torchaudio/lib/libtorchaudio.so', 'lib'),
        ('env_gi/lib/python3.8/site-packages/torchaudio/lib/libtorchaudio_ffmpeg.so', 'lib'),
        ('env_gi/lib/python3.8/site-packages/torchaudio/lib/libtorchaudio_sox.so', 'lib'),
        ('env_gi/lib/python3.8/site-packages/torchaudio/lib/_torchaudio.so', 'lib'),
        ('env_gi/lib/python3.8/site-packages/torchaudio/lib/_torchaudio_ffmpeg.so', 'lib'),
        ('env_gi/lib/python3.8/site-packages/torchaudio/lib/_torchaudio_sox.so', 'lib'),
        ('env_gi/lib/python3.8/site-packages/torch/lib/libtorch.so', 'lib'),
        ('env_gi/lib/python3.8/site-packages/torch/lib/libtorch_python.so', 'lib'),
        ('env_gi/lib/python3.8/site-packages/torch/lib/libtorch_cuda.so', 'lib'),
        ('env_gi/lib/python3.8/site-packages/torch/lib/libc10.so', 'lib'),
        ('env_gi/lib/python3.8/site-packages/torch/lib/libc10_cuda.so', 'lib'),
    ],
    datas=[],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='dependencies',
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

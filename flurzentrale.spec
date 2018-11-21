# -*- mode: python -*-

block_cipher = None

add_files = [
                ('gui/*.ui', 'gui'),
                ('resources_rc.py', '.'),
                ('config.ini', '.')
            ]

a = Analysis(['main.py'],
             pathex=['/Users/sld/Documents/privat/projekte/fz_window/flurzentrale'],
             binaries=[],
             datas=add_files,
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          [],
          exclude_binaries=True,
          name='flurzentrale',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=False )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               name='Flurzentrale')
app = BUNDLE(coll,
             name='flurzentrale.app',
             icon='icon.icns',
             bundle_identifier=None)

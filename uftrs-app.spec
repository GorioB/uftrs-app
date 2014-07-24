# -*- mode: python -*-
a = Analysis(['login.py'],
             pathex=['D:\\devel\\code\\uftrs'],
             hiddenimports=[],
             hookspath=None,
             runtime_hooks=None)
pyz = PYZ(a.pure)
a.datas+=[('assets/logo.gif','D:\\devel\\code\\uftrs\\assets\\logo.gif','DATA'),
('assets/default.docx','D:\\devel\\code\\uftrs\\assets\\default.docx','DATA'),
('icon.ico','icon.ico','DATA')]
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='uftrs-app.exe',
          debug=False,
          strip=None,
          upx=True,
          console=False , icon='icon.ico')

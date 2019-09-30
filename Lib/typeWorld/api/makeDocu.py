# -*- coding: utf-8 -*-

import os
from typeWorld.api import *
from typeWorld.api.base import *
from ynlib.files import WriteToFile, ReadFromFile

docstrings = []

docstrings.extend(RootResponse().docu())
docstrings.extend(InstallableFontsResponse().docu())
docstrings.extend(InstallFontResponse().docu())
docstrings.extend(UninstallFontResponse().docu())
docstrings.extend(SetAnonymousAppIDStatusResponse().docu())

docstring = ReadFromFile(os.path.join(os.path.dirname(__file__), 'docu.md'))


handles = []
for key in [x[0] for x in docstrings]:
	if not key in handles:
		handles.append(key)

classTOC = ''
for handle in handles:
	classTOC += '- [%s](#user-content-class-%s)<br />\n' % (handle, handle.lower())
classTOC += '\n\n'

docstring = docstring.replace('__classTOC__', classTOC)

for handle in handles:
	for className, string in docstrings:
		if handle == className:
			docstring += string
			docstring += '\n\n'
			break

if not 'TRAVIS' in os.environ:
	WriteToFile(os.path.join(os.path.dirname(__file__), 'README.md'), docstring)

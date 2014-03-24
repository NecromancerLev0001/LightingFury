'''
Created on 2014. 3. 21.

@author: Su-Jin Lee
'''

from distutils.core import setup
import py2exe, sys
 
#sys.argv.append("py2exe")

setup(name = "LightingFury-winpeer",
      version = "0.0.0",
      author = "Su-Jin Lee",
      author_email = "kanobaoha@gmail.com",
      url = "#",
      license = "MIT",
      windows = [{"script": "lfpeer.py", }, ],
      options = {"py2exe": {"optimize": 2,
                            "compressed": True,
                            "bundle_files": 1,
                            "dll_excludes": ["MSVCP90.dll", "msvcr71.dll",
                                             "oci.dll", 'POWRPROF.dll', ],
                            "excludes": ['_ssl', "pywin", 
                                         "pywin.debugger",
                                         "pywin.debugger.dbgcon",
                                         "pywin.dialogs", 
                                         "pywin.dialogs.list",
                                         "Tkconstants","Tkinter","tcl", 
                                         "email", 'difflib', 'doctest',
                                         'optparse', 'calendar', 'pdb', 'unittest', ], }, },
      zipfile = None, )

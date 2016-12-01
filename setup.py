#!/usr/bin/python

from distutils.core import setup
import py2exe,os

manifest = """
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<assembly xmlns="urn:schemas-microsoft-com:asm.v1"
manifestVersion="1.0">
<assemblyIdentity
    version="0.64.1.0"
    processorArchitecture="x86"
    name="Controls"
    type="win32"
/>
<description>VEXDisplay Server</description>
<trustInfo xmlns="urn:schemas-microsoft-com:asm.v2">
    <security>
      <requestedPrivileges>
        <requestedExecutionLevel
          level="requireAdministrator"
          uiAccess="false"/>
        </requestedPrivileges>
       </security>
  </trustInfo>
<dependency>
    <dependentAssembly>
        <assemblyIdentity
            type="win32"
            name="Microsoft.Windows.Common-Controls"
            version="6.0.0.0"
            processorArchitecture="X86"
            publicKeyToken="6595b64144ccf1df"
            language="*"
        />
    </dependentAssembly>
</dependency>
<dependency>
    <dependentAssembly>
        <assemblyIdentity
            type="win32"
            name="Microsoft.VC90.CRT"
            version="9.0.30729.4918"
            processorArchitecture="X86"
            publicKeyToken="1fc8b3b9a1e18e3b"
            language="*"
        />
    </dependentAssembly>
</dependency>
</assembly>
"""

"""
installs manifest and icon into the .exe
but icon is still needed as we open it
for the window icon (not just the .exe)
changelog and logo are included in dist
"""

setup(
    windows = [
        {
            "script": "C:\\Users\\jammerxd\\Desktop\\VEXDisplayServer\\VEXSERVER.py",
            "icon_resources": [(1, "favicon.ico")],
            "other_resources": [(24,1,manifest)],
            "uac_info": "requireAdministrator"
        }
    ],
    
    options = {
           "py2exe":{"dll_excludes":["MSVCP90.dll"],
		   "includes" : ["backports_abc"],
		   "excludes" : ["tcl","Tkinter"],
                   "compressed":1,
                   "bundle_files" : 3,
                   "dist_dir" : "VEXDisplayServer"
		   }},
    zipfile = None,
    data_files = ["favicon.ico","icon.png"]
)
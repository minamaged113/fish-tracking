import cx_Freeze as cf
import sys
import os



sys.path.append(os.path.join(os.getcwd(), "UI"))
sys.path.append(os.path.join(os.getcwd(), "file_handlers"))

os.environ['TCL_LIBRARY'] = r'C:\Program Files (x86)\Microsoft Visual Studio\Shared\Python36_64\tcl\tcl8.6'
os.environ['TK_LIBRARY'] = r"C:\Program Files (x86)\Microsoft Visual Studio\Shared\Python36_64\tcl\tk8.6"

print(sys.path)

base = None
targetName = None
if sys.platform == 'win32':
    base = 'Win32GUI'
    targetName = "Fisher.exe"
# The following packages has to be included, as follows:
#   ` "packages": ["numpy"] `

cf.setup(
    name = "Fisher",
    version = "0.1",
    description = "",
    options = {
        "build_exe" : {
            "packages": [
                "numpy",
                "os",
                "scipy",
                "skimage"
                ],
            "includes": [
                "atexit"
                ]
        }

    },
    executables = [
        cf.Executable("main.py",
                      base=base,
                      targetName=targetName)
    ]
)
import cx_Freeze as cf
import sys
import os

sys.path.append(os.path.join(os.getcwd()))
print(sys.path)
cf.setup(
    name = "Fisher",
    version = "0.1",
    description = "",
    options = {
        "build_exe" : {
            "packages":{
                # ["PyQt5", "cv2"]
            }
        }
    },
    executables = [
        cf.Executable("main.py")
    ]
)
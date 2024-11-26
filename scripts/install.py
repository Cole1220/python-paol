import subprocess
from sys import platform
if platform == "linux" or platform == "linux2":
    # linux
    pass

elif platform == "darwin":
    # OS X
    pass

elif platform == "win32":
    # Windows
    subprocess.run(["python3","scripts/install_via_python_windows.py"])

from pathlib import Path

from PyQt5.QtCore import QDir

packageName = __name__

resourcePath = Path(__file__).resolve().parent / "resources"
if not resourcePath.exists():
    _msg = "Cannot find resources directory"
    raise FileNotFoundError(_msg)

QDir.addSearchPath(packageName, str(resourcePath))

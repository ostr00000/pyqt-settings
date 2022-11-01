from pathlib import Path

from PyQt5.QtCore import QDir

packageName = __name__

resourcePath = Path(__file__).resolve().parent / 'resources'
assert resourcePath.exists()
QDir.addSearchPath(packageName, str(resourcePath))

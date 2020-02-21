from setuptools import find_packages, setup

setup(
    name='pyqt-settings',
    version=0.1,
    python_requires='>=3.8',
    description='Descriptors for QSettings with GUI generating',
    packages=find_packages(where="lib", exclude=("*test*",)),
    package_dir={"": "lib"},
    install_requires=['decorator', 'PyQt5'],
    extras_require={
        'dev': ['PyQt5-stubs'],
    },
)
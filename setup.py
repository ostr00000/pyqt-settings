from setuptools import find_packages, setup

setup(
    name='pyqt-settings',
    version='0.2',
    python_requires='>=3.8',
    description="Descriptors for QSettings with GUI generating",

    package_dir={'': 'lib'},
    packages=find_packages(where='lib', exclude=('*test*',)),
    package_data={'': ['*.svg', '*.jpg']},

    install_requires=['decorator', 'PyQt5', 'boltons'],
    extras_require={
        'dev': ['PyQt5-stubs'],
    },
)

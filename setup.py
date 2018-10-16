from setuptools import setup

try:
    from pyqt_distutils.build_ui import build_ui
    cmdclass = {"build_ui": build_ui}
except ImportError:
    cmdclass = {}

setup(
    name="flurzentrale",
    version="0.1",
    packages=["flurzentrale"],
    cmdclass=cmdclass,
)


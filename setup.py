"""
setup.py - this module makes the package installable
"""

from distutils.core import setup

NAME = "slmsuite"
VERSION = "0.1"
DEPENDENCIES = [
    "scipy", "matplotlib", "numpy", "opencv-python", "tqdm", "h5py"
]
DESCRIPTION = ("Package for high-performance spatial light "
               "modulator (SLMs) control and holography.")
AUTHOR = "MIT Quantum Photonics Group"
AUTHOR_EMAIL = "qp-slm@mit.edu"

setup(author=AUTHOR,
      author_email=AUTHOR_EMAIL,
      description=DESCRIPTION,
      install_requires=DEPENDENCIES,
      name=NAME,
      version=VERSION,
)

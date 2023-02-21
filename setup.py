from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '0.1.0'
DESCRIPTION = 'Generating HVAC&R performance table - ASHRAE STD 205'
LONG_DESCRIPTION = 'ASHRAE Standard 205 - Heat Pump Design Model supply; This package helps OEMs to convert HPDM output to STD 205 format; it also provide some RS sample tables.'

# Setting up
setup(
    name="HPDMSTD205",
    version=VERSION,
    author="Hanlong Wan, Bo Shen (ORNL)",
    author_email="<wanh@ornl.gov>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    install_requires=['pandas', 'json', 'pint'],
    keywords=['python', 'ASHRAE', 'performance table', 'HPDM', 'standard 205'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)

"""Setup tool for making a library."""
from pathlib import Path

from setuptools import find_packages
from setuptools import setup

import src.Logges as Logges

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()


setup(
    name="Logges",
    version=Logges.__version__,
    license="MIT",
    author="Serkan UYSAL, Ozkan UYSAL",
    maintainer="Ozkan UYSAL",
    author_email="uysalserkan08@gmail.com",
    maintainer_email="ozkan.uysal.2009@gmail.com",
    python_requires=">=3.6",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    include_package_data=True,
    url="https://github.com/uysalserkan/Logges",
    description="A simple Logging tool can extract as Markdown, PDF, or print console.",
    long_description=long_description,
    keywords="Log, Logging, Logges, Logger",
    install_requires=[
        "matplotlib==3.5.2",
        "rich==10.16.2",
        "reportlab==3.5.67",
    ],
)

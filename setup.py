"""Setup tool for making a library."""
from setuptools import setup, find_packages

with open('requirements.txt', 'r') as file:
    reqs = file.read().splitlines()
    file.close()

with open('README.md', 'r') as file:
    long_desc = file.readlines()
    file.close()

setup(
    name="Logges",
    version="1.0.0",
    license='MIT',
    author='Serkan UYSAL, Ozkan UYSAL',
    author_email='uysalserkan08@gmail.com',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    url="https://github.com/uysalserkan/Logges",
    description="A simple Logging tool can extract as Markdown, PDF, or print console.",
    long_description=long_desc,
    keywords="Log, Logges, uysal, Logger",
    install_requires=reqs,
)

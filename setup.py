from codecs import open
from distutils.util import convert_path
from pathlib import Path

from setuptools import setup

here = Path(__file__).cwd()

# Get the long description from the README file
with open(here / 'README.md', encoding='utf-8') as f:
    long_description = f.read()

main_ns = {}
version_path = convert_path('pychart/version.py')
with open(version_path) as version_file:
    exec(version_file.read(), main_ns)

setup(
    name='pychart',
    packages=['pychart'],
    entry_points={'console_scripts': ['pychart=pychart:cli']},
    version=main_ns['__version__'],
    author="Mike Lane",
    author_email="mikelane@gmail.com",
    url='https://github.com/mikelane/pychart',
    download_url='https://pypi.python.org/pypi/pychart/',
    license='MIT',
    description='a python command-line tool which draws basic graphs in the terminal',
    platforms='any',
    keywords='python CLI tool drawing graphs shell terminal',
    python_requires='>=3.6',
    install_requires=['colorama', 'pandas'],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: POSIX',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6'],
    long_description=long_description,
    long_description_content_type='text/markdown'
)

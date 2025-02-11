import os
import sys
from setuptools import setup, find_packages
from setuptools.command.install import install as _install
from setuptools.command.sdist import sdist as _sdist
from subprocess import CalledProcessError, run

def _run_build_tables(dir):
    """Runs the _build_tables.py script to generate lexing/parsing tables."""
    try:
        run([sys.executable, '_build_tables.py'], cwd=os.path.join(dir, 'ctoepl'), check=True)
    except (FileNotFoundError, CalledProcessError) as e:
        print(f"Error: Failed to build tables - {e}")

class install(_install):
    """Custom install command that builds lexing/parsing tables."""
    def run(self):
        _install.run(self)
        self.execute(_run_build_tables, (self.install_lib,), msg="Building lexing/parsing tables")

class sdist(_sdist):
    """Custom sdist command that builds tables before packaging."""
    def make_release_tree(self, basedir, files):
        _sdist.make_release_tree(self, basedir, files)
        self.execute(_run_build_tables, (basedir,), msg="Building lexing/parsing tables")

# Load README.md for PyPI-friendly long description
with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name='c-to-epl',
    version='1.2.2',
    description='C to ePL Converter in Python',
    long_description=long_description,
    long_description_content_type="text/markdown",
    license='BSD',
    author='',
    maintainer='Xeline',
    author_email='',  # Updated email
    url='',
    download_url='',
    platforms='Cross Platform',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
    ],
    packages=find_packages(),
    package_data={'ctoepl': ['*.cfg']},
    install_requires=[
        'ply>=3.11'  # Example dependency (add real ones)
    ],
    entry_points={
        'console_scripts': [
            'c_to_epl=ctoepl:main',
        ],
    },
    cmdclass={'install': install, 'sdist': sdist},
    python_requires='>=3.6',
)

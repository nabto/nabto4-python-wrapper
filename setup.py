import glob
import os
import shutil
import sys
from setuptools import setup, Extension
from setuptools.command.build_py import build_py as _build_py

VERSION = '0.1.5'


def read(f):
    return open(f, 'r', encoding='utf-8').read()


class build_ext_first(_build_py):
    def move_extension_to_package(self):
        for f in glob.glob("build/lib.linux-**/*.so", recursive=False):
            chunks = f.split("/")
            new_name = "/".join([chunks[0], chunks[1], "nabto_client", chunks[2]],)
            print(f"Moving {f} to {new_name}")
            os.rename(f, new_name)
    
    def run(self):
        self.run_command('build_ext')
        _build_py.run(self)
        self.move_extension_to_package()


nabto_api = Extension(
    '_nabto_api',
    sources=[
        'nabto_client/nabto_client.i',
        'extension/src/wrapper.cpp', 
    ],
    swig_opts=['-c++'],
    include_dirs=['extension/inc/', 'extension/linux64/include/'],
    library_dirs=['extension/linux64/lib/'],
    libraries=['nabto_client_api_static', 'nabto_static_external'],
)

if sys.argv[-1] == 'publish':
    if os.system("pip freeze | grep twine"):
        print("twine not installed.\nUse `pip install twine`.\nExiting.")
        sys.exit()
    os.system("python setup.py sdist")
    if os.system("twine check dist/*"):
        print("twine check failed. Packages might be outdated.")
        sys.exit()
    os.system("twine upload -r testpypi dist/*")
    # print("You probably want to also tag the version now:")
    # print("  git tag -a %s -m 'version %s'" % (VERSION, VERSION))
    # print("  git push --tags")
    shutil.rmtree('dist')
    shutil.rmtree('nabto_client.egg-info')
    sys.exit()

setup(
    name='nabto_client',
    version=VERSION,
    cmdclass={'build_py': build_ext_first},
    packages=['nabto_client'],
    author='Alexandru Gandrabur',
    author_email='alexandru.gandrabur@tremend.com',
    description="""Nabto Client Wrapper for Python""",
    long_description=read('README.md'),
    long_description_content_type='text/markdown',
    python_requires=">=3.6",
    ext_modules=[nabto_api],
    classifiers=[
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content'
    ],
)

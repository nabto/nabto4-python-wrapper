import os
import glob
from setuptools import setup, Extension
from setuptools.command.build_py import build_py as _build_py


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
        'extension/src/example.c', 
    ],
    include_dirs=['extension/inc/'],
    
)

setup(
    name='nabto_client',
    version='0.1.0',
    cmdclass={'build_py': build_ext_first},
    packages=['nabto_client'],
    author='Alexandru Gandrabur',
    author_email='alexandru.gandrabur@tremend.com',
    description="""Nabto Client Wrapper for Python""",
    ext_modules=[nabto_api],
)
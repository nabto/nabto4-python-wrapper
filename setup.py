from setuptools import setup, Extension

nabto_api = Extension(
    '_nabto_api',
    sources=[
        'nabto_client.i',
        'src/example.c', 
    ],
    include_dirs=['inc/']
)

setup(
    name='nabto_client',
    version='0.1.0',
    author='Alexandru Gandrabur',
    description="""Nabto Client Wrapper for Python""",
    ext_modules=[nabto_api],
    py_modules='nabto_client'
)
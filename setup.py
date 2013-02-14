from distutils.core import setup

setup(
    name='pywakeonlan',
    version='0.1',
    description='A small python module for wake on lan.',
    url='https://github.com/Trollhammaren/pywakeonlan',
    author='Remco Haszing',
    author_email='remcohaszing@gmail.com',
    packages=['wakeonlan'],
    license='DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE',
    long_description=open('README.md').read(),
)

import versioneer
from setuptools import setup, find_packages

# To use a consistent encoding
from codecs import open
from os import path, environ

cur_dir = path.abspath(path.dirname(__file__))

with open(path.join(cur_dir, 'requirements.txt')) as f:
    requirements = f.read().split()

with open(path.join(cur_dir, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='clockwidget',
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    # Author details
    author='SLAC National Accelerator Laboratory',

    packages=find_packages(),
    package_dir={'clockwidget':'clockwidget'},
    description='The famous LCLS Clock Widget',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/slaclab/pydm_clock_widget',
    license='BSD',
    install_requires=requirements,
    include_package_data=True,
    classifiers=[
        'License :: OSI Approved :: BSD License',
        'Development Status :: 4 - Beta',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
    ]
)

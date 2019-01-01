from ez_setup import use_setuptools
use_setuptools()
from setuptools import setup, find_packages

classifiers = ['Development Status :: 4 - Beta',
               'Operating System :: POSIX :: Linux',
               'License :: OSI Approved :: MIT License',
               'Intended Audience :: Developers',
               'Programming Language :: Python :: 2.7',
               'Topic :: System :: Hardware']

setup(name              = 'Simple_AM2315',
      version           = '1.0.3',
      author            = 'Robert Wolterman',
      author_email      = 'robert.wolterman@gmail.com',
      description       = 'Python code to use the AM2315 Temp and Humidity Sensor with a CHIP, Raspberry Pi, or BeagleBone black.',
      license           = 'MIT',
      classifiers       = classifiers,
      url               = 'https://github.com/xtacocorex/Simple_AM2315',
      dependency_links  = [],
      install_requires  = [],
      packages          = find_packages())

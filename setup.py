from setuptools import setup, find_packages


setup(name='dropper',
      version='1.0',
      description='A CLI for Dropbox manipulation',
      author='Olli Wang',
      author_email='olliwang@ollix.com',
      url='http://www.ollix.com/',
      packages=['dropper'],
      install_requires = ['dropbox-client', 'oparse'],
      entry_points={
        'console_scripts': ['dropper=dropper.command:dropper_command'],
      })

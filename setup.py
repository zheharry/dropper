from setuptools import setup, find_packages


setup(name='backsql',
      version='1.0',
      description='Backup PostgreSQL database to Dropbox',
      author='Olli Wang',
      author_email='olliwang@ollix.com',
      url='http://www.ollix.com/',
      packages=['backsql'],
      install_requires = ['dropbox-client', 'oparse'],)

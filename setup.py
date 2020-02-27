import setuptools
from os import path


this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setuptools.setup(name='qubolepystream',
      version='0.8.0',
      description='Simple and easy to use Qubole connector',
      long_description=long_description,
      long_description_content_type='text/markdown',
      url='https://github.com/achilleasatha/PyQubole',
      author='Achilleas Athanasiou Fragkoulis',
      author_email='achilleasatha@gmail.com',
      license='MIT',
      packages=setuptools.find_packages(),
      zip_safe=False,
      install_requires=[
            'qds_sdk'
      ]
      )

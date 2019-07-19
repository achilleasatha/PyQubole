import setuptools

setuptools.setup(name='pyqubole',
      version='0.1',
      description='Simple and easy to use Qubole connector',
      url='https://github.com/achilleasatha/PyQubole',
      author='Achilleas Athanasiou Fragkoulis',
      author_email='achilleasatha@gmail.com',
      license='MIT',
      packages=setuptools.find_packages(),
      zip_safe=False,
      install_requires=[
            'qds_sdk',
            're',
            'os',
            'pandas',
            'json',
            'time',
            'warnings'
      ]
      )

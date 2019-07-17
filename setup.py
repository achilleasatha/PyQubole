from setuptools import setup

setup(name='pyqubole',
      version='0.1',
      description='Simple and easy to use Qubole connector',
      url='https://github.com/achilleasatha/PyQubole',
      author='Achilleas Athanasiou Fragkoulis',
      author_email='achilleasatha@gmail.com',
      license='MIT',
      packages=['pyqubole'],
      zip_safe=False,
      install_requires=[
            'pandas>=0.23.0',
            'numpy'
            #todo add frozen dependencies here pip freeze > requirements.txt
      ]
      )

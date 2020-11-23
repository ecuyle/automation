from setuptools import find_packages, setup

setup(
    name='ecuyle/automation/python_packages',
    version='0.1',
    description='Homebrewed python packages used for personal automation projects',
    author='Eric Cuyle',
    author_email='ecuyle@gmail.com',
    packages=find_packages(),
    install_requires=['Rpi.GPIO', 'Adafruit_DHT'],
)


from setuptools import find_packages, setup

setup(
    name='battlebotslib',
    packages=find_packages(),
    version='0.5.0',
    description='Client lib to interact with the battlebots server',
    author='CGI DT AURA',
    license='',
    install_requires=['paho-mqtt==1.6.1', 'requests==2.28.1', 'stomp.py==8.0.1']
)

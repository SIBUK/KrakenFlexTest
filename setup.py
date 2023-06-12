from setuptools import setup, find_packages

setup(
    name='KrakenFlexTest',
    version='2.0',
    packages=find_packages(),
    install_requires=['requests==2.31.0',
                      'python-dateutil==2.8.2'],
    url='https://github.com/SIBUK/KrakenFlexTest',
    license='',
    python_requires='>=3.7, <4',
    author='Simon Bailey',
    author_email='simonbailey2018@gmail.com',
    description='Kraken Flex interview test'
)

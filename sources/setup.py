from setuptools import setup

setup(
    name='x100speed_interface',
    version='0.0.1',

    description='interface for x100speed',
    long_description="",
    url='https://github.com/laodifang',
    author='Ren Peng',
    author_email='ithink.ren@gmail.com',
    license='MIT',

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Topic :: Internet :: WWW/HTTP :: HTTP Servers',
        'Topic :: Multimedia :: Video :: Conversion',

        'License :: OSI Approved :: MIT License',

        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3 :: Only',
    ],
    keywords='',

    packages=['tests'],
    py_modules=['x100speed_interface'],
    install_requires = ['requests>=2.7.0'],
    test_suite='tests',
)


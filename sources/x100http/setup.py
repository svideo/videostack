from setuptools import setup

setup(
    name='x100http',
    version='0.2.4',

    description='web framework support customing file upload processing',
    long_description=open('README.rst').read(),
    url='https://github.com/chengang/x100http',
    author='Chen Gang',
    author_email='yikuyiku.com@gmail.com',
    license='MIT',

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Internet :: WWW/HTTP :: HTTP Servers',

        'License :: OSI Approved :: MIT License',

        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3 :: Only',
    ],
    keywords='http framework webframework file upload rfc1867 x100',

    packages=['tests', 'tests/sta'],
    package_data = { '': ['*.html', '*.htm'], },
    py_modules=['x100http'],
    install_requires = ['requests>=2.7.0'],
    test_suite='tests',
)

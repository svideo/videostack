from setuptools import setup

setup(
    name='x100monitor',
    version='0.1.0',

    description='get system basic infomation',
    long_description=open('README.rst').read(),
    #url='https://github.com/WayneZhouChina/x100monitor',
    author='Wayne Zhou',
    author_email='cumtxhzyy@gmail.com',
    license='MIT',

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',

        'License :: OSI Approved :: MIT License',

        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3 :: Only',
    ],
    keywords='x100 monitor system',

    py_modules=['x100monitor'],
    test_suite='test',
)

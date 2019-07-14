from setuptools import setup

setup(
    name='reqcreate',
    version='0.0.1',
    packages=['reqcreate'],
    package_dir={'reqcreate':
                 'reqcreate'},
    include_package_data=True,
    package_data={'': ['mapping.txt','built-in.txt']},
    install_requires=['yarg'],
    url='https://github.com/cllbck/reqcreate',
    license='',
    author='Evgeniy Kolbin',
    author_email='cllbck@cllbck.me',
    description='Create requirements file (from imports) for a project without it',
    test_suite='tests',
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'reqcreate=reqcreate.main:main',
        ],
    },
)

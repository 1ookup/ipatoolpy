import setuptools

setuptools.setup(
    name='ipatoolpy',
    version='0.0.2',
    entry_points={
        'console_scripts': [
            'ipatoolpy = cli.main:main'
        ]
    },
    author='1ookup',
    author_email='1ookup@1ookup.1ookup',
    url='https://github.com/1ookup/ipatoolpy',
    description='ipatoolpy is a command line tool that allows you to search for iOS apps on the App Store and download a copy of the app package, known as an ipa file.',
    packages=setuptools.find_packages(),
    install_requires=[
        'setuptools',
        'requests',
        'click',
        'loguru',
        'psutil',
        'PySocks',
    ],
    python_requires='>=3.5'
)

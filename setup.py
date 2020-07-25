from setuptools import setup, find_packages


setup(
    name='wisp',
    packages=find_packages(),
    install_requires=[
        'parsec'
    ],
    entry_points={
        'console_scripts': [
            'wisp = wisp.repl:main',
        ],
    }
)

from setuptools import setup
setup(
    name='katamorph',
    version='0.1',
    entry_points={
        'console_scripts': [
            'katamorph=katamorph:run'
        ]
    }
)


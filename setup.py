from setuptools import setup

setup(
    name='spottpreis',
    version='0.1',
    py_modules=['spottpreis'],
    install_requires=[
        'boto3', 'Click'
    ],
    entry_points='''
        [console_scripts]
        spottpreis=spottpreis:cli
    ''',
)
from setuptools import setup

setup(
    name='ec2spotter',
    version='0.1',
    py_modules=['ec2spotter'],
    install_requires=[
        'boto3', 'Click'
    ],
    entry_points='''
        [console_scripts]
        ec2spotter=ec2spotter:cli
    ''',
)
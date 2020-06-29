from setuptools import setup, find_packages

setup(
    name='reality_check',
    version='0.1',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'Click',
        'pandas'
    ],
    entry_points='''
        [console_scripts]
        reality_check=reality_check.reality_check:cli
    ''',
)
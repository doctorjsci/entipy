from setuptools import setup, find_packages

setup(
    name='Entipy',
    version='1.0',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'attrs==20.3.0',
        'certifi==2020.12.5',
        'iniconfig==1.1.1',
        'packaging==20.9',
        'pluggy==0.13.1',
        'py==1.10.0',
        'pyparsing==2.4.7',
        'pytest==6.2.3',
        'toml==0.10.2'
    ]
)

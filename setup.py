#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = ['Click>=7.0', 'PyOpenSSL>=20.0.1']

test_requirements = ['pytest>=3', 'flake8>=3.7.8', 'pylint>=2.8.3']

setup(
    author="Avishay Bar",
    author_email='avishay.il@gmail.com',
    python_requires='>=3.6',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    description="Tool for Signing and Verifying Signatures of CloudFormation Templates",
    entry_points={
        'console_scripts': [
            'cf_signer=cf_signer.cli:main',
        ],
    },
    install_requires=requirements,
    license="MIT license",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='cf_signer',
    name='cf_signer',
    packages=find_packages(include=['cf_signer', 'cf_signer.*']),
    test_suite='tests',
    tests_require=test_requirements,
    extras_require={
        'develop': test_requirements,
    },
    url='https://github.com/avishayil/cf-signer',
    version='0.0.3',
    zip_safe=False,
)

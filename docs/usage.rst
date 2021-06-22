=====
Usage
=====

Preparation
-----------

First, the utility provides the ``prepare`` functionality that does the following:

* Reading your template ``JSON`` file

* Converting the template to Python dictionary object.

* Converting the Python dictionary object back to a ``JSON`` file.

This is done to ensure that the tool will not tamper the template contents during the signing process.

To prepare a CloudFormation template to the signing process::

  cf_signer --prepare --template cf.template

This will create a cf-prepared.template file you can sign using the ``cf-signer`` tool.

Getting Started
===============

To sign a CloudFormation template using the ``cf-signer`` tool::

  cf_signer --sign --template cf.template --key key.pem

To verify a signature of a CloudFormation template using the ``cf-signer`` tool::

  cf_signer --verify --template cf-signed.template --key pubkey.pem


==========================================
CF-Signer - CloudFormation Signing Utility
==========================================


.. image:: https://img.shields.io/pypi/v/cf-signer.svg
        :target: https://pypi.python.org/pypi/cf-signer

.. image:: https://img.shields.io/travis/avishayil/cf-signer.svg
        :target: https://travis-ci.com/avishayil/cf-signer

.. image:: https://readthedocs.org/projects/cf-signer/badge/?version=latest
        :target: https://cf-signer.readthedocs.io/en/latest/?version=latest
        :alt: Documentation Status




Tool for signing and verifying the integrity of CloudFormation templates


* Free software: MIT license
* Documentation: https://cf-signer.readthedocs.io.


Features
--------

* Signing CloudFormation templates by creating a sha256 hash of the file, encrypted with the user's private key and store base64 form of the signature in the CloudFormation template ``Metadata`` section.
* Verifying the integrity of CloudFormation templates by looking for the signature in the ``Metadata``, extracting it and verifying.

Usage
-----

To sign a CloudFormation template using the ``cf-signer`` tool::

  cf_signer --sign --template cf.template --key key.pem

To verify a signature of a CloudFormation template using the ``cf-signer`` tool::

  cf_signer --verify --template cf-signed.template --key pubkey.pem

Signing Flow
------------

The process of signing is based on the following flow:

* Generate RSA private key::

    openssl genrsa -out key.pem 2048

* Get public key from the RSA generated private key::

    openssl rsa -in key.pem -outform PEM -pubout -out pubkey.pem

* Create a sha256 hash signature, encrypted with the private key::

    openssl dgst -sha256 -sign key.pem -out sign.sha256 cf.template

* Convert the signature to base64 string::
    
    base64 -i sign.sha256 -o sign.b64

* Attach the base64 signature to the CloudFormation template, under the ``Metadata`` block (creating one if it doesn't exist).

Verification Flow
-----------------

The process of signature verification is based on the following flow:

* Detach the signature from the CloudFormation template

* Convert the base64 detached signature string to binary format::

    base64 -d sign.b64 > sign.sha256

* Validate the signature using the public key::

    openssl dgst -sha256 -verify pubkey.pem -signature sign.sha256 cf.template

Credits
-------

* The signing and verification process was inspired by `sgershtein/SignedJSON`_.

* This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _`sgershtein/SignedJSON`: https://github.com/sgershtein/SignedJSON
.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
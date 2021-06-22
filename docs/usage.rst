=====
Usage
=====

To sign a CloudFormation template using the ``cf-signer`` tool::

  cf_signer --sign --template cf.template --key key.pem

To verify a signature of a CloudFormation template using the ``cf-signer`` tool::

  cf_signer --verify --template cf-signed.template --key pubkey.pem

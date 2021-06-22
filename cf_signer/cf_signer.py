"""Main module."""

# Assumptions:
# JSON template is indented with 2 space indentation

import os
import base64
import json
import logging
import click

from OpenSSL import crypto


def create_signature(target_file_path: str, key_file_path: str, logger: logging.Logger):
    # Creating signature

    logger.debug('Evaluate key and target file...')

    try:
        key_file = open(key_file_path, 'r')
        target_file = open(target_file_path, 'r').read()
        key = key_file.read()
        key_file.close()
    except Exception as e:
        click.echo('Failed to evaluate key / target file')
        logger.error('Failed to evaluate key / target file: ' + str(e))
        raise

    logger.debug('Validating private key format...')

    try:
        if key.startswith('-----BEGIN '):
            pkey = crypto.load_privatekey(crypto.FILETYPE_PEM, key)
        else:
            pkey = crypto.load_pkcs12(key).get_privatekey()
        data = str.encode(target_file)
    except Exception as e:
        click.echo('Error validating private key format')
        logger.error('Error validating private key format: ' + str(e))
        raise

    logger.debug('Creating base64 signature...')

    try:
        signature = crypto.sign(pkey, data, 'sha256')

        # Convert signature to base64 signature
        sign_base64_bytes = base64.b64encode(signature)
        sign_base64 = sign_base64_bytes.decode()
    except Exception as e:
        click.echo('Error creating base64 signature')
        logger.error('Error creating base64 signature: ' + str(e))
        raise

    logger.debug('Attaching signature...')

    try:
        # Attaching signature to the cloudformation template under 'Metadata'
        with open(target_file_path, 'r+') as file:
            file_name_without_ext = os.path.splitext(target_file_path)[0]
            file_ext = os.path.splitext(target_file_path)[1]
            with open(file_name_without_ext + '-signed' + file_ext, 'w') as signed_file:
                file_data = json.load(file)
                new_data = {'Metadata': {'Integrity': sign_base64}}
                file_data.update(new_data)
                file.seek(0)
                json.dump(file_data, signed_file, indent=2)
                click.echo('Signing completed successfully')
                logger.debug('Signing completed successfully')
    except Exception as e:
        click.echo('Error attaching signature')
        logger.error('Error attaching signature: ' + str(e))
        raise


def verify_signature(target_file_path: str, key_file_path: str, logger: logging.Logger):
    logger.debug('Detaching signature...')

    try:
        # Detaching signature from CloudFormation template
        sign_base64 = ''
        with open(target_file_path, 'r') as signed_file:
            file_data = json.load(signed_file)
            for i in file_data:
                if i == 'Metadata':
                    sign_base64 = file_data['Metadata']['Integrity']
                    file_data[i].pop('Integrity', None)
            if file_data['Metadata'] == {}:
                file_data.pop('Metadata', None)
    except Exception as e:
        click.echo('Error detaching signature')
        logger.error('Error detaching signature: ' + str(e))
        raise

    logger.debug('Creating signature certificate from public key...')

    try:
        sign_base64_bytes = sign_base64.encode()
        signature = base64.b64decode(sign_base64_bytes)

        # Signature verification
        public_key_data = open(key_file_path, 'r').read()
        pkey = crypto.load_publickey(crypto.FILETYPE_PEM, public_key_data)
        x509 = crypto.X509()
        x509.set_pubkey(pkey)
    except Exception as e:
        click.echo('Error creating signature certificate')
        logger.error('Error creating signature certificate: ' + str(e))
        raise

    logger.debug('Extracting CloudFormation template original data...')

    try:
        template_file = json.dumps(file_data, indent=2)
        data = str.encode(template_file)
    except Exception as e:
        click.echo('Error extracting CloudFormation template data')
        logger.error('Error extracting CloudFormation template data: ' + str(e))
        raise

    logger.debug('Verifying integrity...')

    try:
        verify = crypto.verify(x509, signature, data, 'sha256')
        if verify is None:
            click.echo('Signature verification completed successfully')
            logger.debug('Signature verification completed successfully')

        else:
            click.echo('Signature verification failed from unknown reason')
            logger.error('Signature verification failed from unknown reason')
    except Exception as e:
        click.echo('Error validating template integrity')
        logger.error('Error validating template integrity: ' + str(e))
        raise


def prepare_template(target_file_path: str, logger: logging.Logger):
    logger.debug('Preparing template...')

    try:
        # Cleaning the template and converting it to 2 spaces indentation JSON
        with open(target_file_path, 'r+') as file:
            file_name_without_ext = os.path.splitext(target_file_path)[0]
            file_ext = os.path.splitext(target_file_path)[1]
            with open(file_name_without_ext + '-prepared' + file_ext, 'w') as signed_file:
                file_data = json.load(file)
                file.seek(0)
                json.dump(file_data, signed_file, indent=2)
                click.echo('Template preparation completed successfully')
                logger.debug('Template preparation completed successfully')
    except Exception as e:
        click.echo('Error preparing template')
        logger.error('Error preparing template: ' + str(e))
        raise

"""Main module."""

# Assumptions:
# JSON template is indented with 2 space indentation

import os
import base64
import json

from OpenSSL import crypto

from cf_signer.utils import get_logger, click_echo


def create_signature(target_file_path: str, key_file_path: str, from_cli: bool = False) -> bool:
    """Signing a CloudFormation template with a private key

    Args:
        target_file_path: the relative path to the CloudFormation template
        key_file_path: the relative path to the private key,
        from_cli: Whether the function called from command line interface
    Returns:
        True / False
    Raises:
        None

    """

    logger = get_logger()
    logger.debug('Evaluate key and target file...')

    try:
        with open(key_file_path, 'r+') as key_file:
            with open(target_file_path, 'r+') as target_file:
                target_file_contents = target_file.read()
                key_file_contents = key_file.read()
    except Exception as ex:
        click_echo('Failed to evaluate key / target file', from_cli)
        logger.debug('Failed to evaluate key / target file: %s', str(ex))
        return False

    logger.debug('Validating private key format...')

    try:
        if key_file_contents.startswith('-----BEGIN '):
            pkey = crypto.load_privatekey(crypto.FILETYPE_PEM, key_file_contents)
        else:
            pkey = crypto.load_pkcs12(key_file).get_privatekey()
        data = str.encode(target_file_contents)
    except Exception as ex:
        click_echo('Error validating private key format', from_cli)
        logger.debug('Error validating private key format: %s', str(ex))
        return False

    logger.debug('Creating base64 signature...')

    try:
        signature = crypto.sign(pkey, data, 'sha256')

        # Convert signature to base64 signature
        sign_base64_bytes = base64.b64encode(signature)
        sign_base64 = sign_base64_bytes.decode()
    except Exception as ex:
        click_echo('Error creating base64 signature', from_cli)
        logger.debug('Error creating base64 signature: %s', str(ex))
        return False

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
                click_echo('Signing completed successfully', from_cli)
                logger.debug('Signing completed successfully')
                return True

    except Exception as ex:
        click_echo('Error attaching signature', from_cli)
        logger.debug('Error attaching signature: %s', str(ex))
        return False


def verify_signature(target_file_path: str, key_file_path: str, from_cli: bool = False):
    """Verifying the signature of a CloudFormation template with a public key

    Args:
        target_file_path: the relative path to the CloudFormation template with the signature
        key_file_path: the relative path to the public key
        from_cli: Whether the function called from command line interface
    Returns:
        True / False
    Raises:
        None

    """

    logger = get_logger()
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
    except Exception as ex:
        click_echo('Error detaching signature', from_cli)
        logger.debug('Error detaching signature: %s', str(ex))
        return False

    logger.debug('Creating signature certificate from public key...')

    try:
        sign_base64_bytes = sign_base64.encode()
        signature = base64.b64decode(sign_base64_bytes)

        # Signature verification
        public_key_data = open(key_file_path, 'r').read()
        pkey = crypto.load_publickey(crypto.FILETYPE_PEM, public_key_data)
        x509 = crypto.X509()
        x509.set_pubkey(pkey)
    except Exception as ex:
        click_echo('Error creating signature certificate', from_cli)
        logger.debug('Error creating signature certificate: %s', str(ex))
        return False

    logger.debug('Extracting CloudFormation template original data...')

    try:
        template_file = json.dumps(file_data, indent=2)
        data = str.encode(template_file)
    except Exception as ex:
        click_echo('Error extracting CloudFormation template data', from_cli)
        logger.debug('Error extracting CloudFormation template data: %s', str(ex))
        return False

    logger.debug('Verifying integrity...')

    try:
        if crypto.verify(x509, signature, data, 'sha256') is None:
            click_echo('Signature verification completed successfully', from_cli)
            logger.debug('Signature verification completed successfully')
            return True

        click_echo('Signature verification failed from unknown reason', from_cli)
        logger.debug('Signature verification failed from unknown reason')
        return False

    except Exception as ex:
        click_echo('Error validating template integrity', from_cli)
        logger.debug('Error validating template integrity: %s', str(ex))
        return False


def prepare_template(target_file_path: str, from_cli: bool = False):
    """Preparing a CloudFormation template to the signing process

    Args:
        target_file_path: The relative path to the CloudFormation template
        from_cli: Whether the function called from command line interface
    Returns:
        True / False
    Raises:
        None

    """

    logger = get_logger()
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
                click_echo('Template preparation completed successfully', from_cli)
                logger.debug('Template preparation completed successfully')
                return True
    except Exception as ex:
        click_echo('Error preparing template', from_cli)
        logger.debug('Error preparing template: %s', str(ex))
        return False

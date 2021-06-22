"""Console script for cf_signer."""
import sys
import logging
import click

from cf_signer.cf_signer import create_signature, verify_signature, prepare_template

logger = logging.getLogger(__name__)
stdout_handler = logging.StreamHandler(sys.stdout)
stdout_handler.setFormatter(logging.Formatter('%(asctime)s %(message)s'))
stdout_handler.setLevel(logging.INFO)
logger.setLevel(logging.INFO)


@click.command()
@click.option('-p', '--prepare', is_flag=True, help='Prepare a CloudFormation template for Signing')
@click.option('-s', '--sign', is_flag=True, help='Sign a CloudFormation template')
@click.option('-v', '--verify', is_flag=True, help='Verify the integrity of a CloudFormation template')
@click.option('-t', '--template', is_flag=False, help='Relative path of a CloudFormation template file')
@click.option('-k', '--key', is_flag=False, help='Relative path of a private / public key, depends on the operation')
@click.option('-d', '--debug', is_flag=True, help='View debug messages')
def main(prepare: bool, sign: bool, verify: bool, template: str, key: str, debug: bool):
    """Tool for Signing and Verifying Signatures of Cloud Templates"""
    if debug:
        logger.addHandler(stdout_handler)
        stdout_handler.setLevel(logging.DEBUG)
        logger.setLevel(logging.DEBUG)
    if prepare:
        prepare_template(target_file_path=template, logger=logger)
    if sign:
        create_signature(target_file_path=template, key_file_path=key, logger=logger)
    if verify:
        verify_signature(target_file_path=template, key_file_path=key, logger=logger)


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover

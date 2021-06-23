# pylint: disable=no-value-for-parameter

"""Console script for cf_signer."""
import sys
import click

from cf_signer.cf_signer import create_signature, verify_signature, prepare_template
from cf_signer.utils import init_logger


@click.command()
@click.option('-p', '--prepare', is_flag=True, help='Prepare a CloudFormation template for Signing')
@click.option('-s', '--sign', is_flag=True, help='Sign a CloudFormation template')
@click.option('-v', '--verify', is_flag=True, help='Verify the integrity of a CloudFormation template')
@click.option('-t', '--template', is_flag=False, help='Relative path of a CloudFormation template file')
@click.option('-k', '--key', is_flag=False, help='Relative path of a private / public key, depends on the operation')
def main(prepare: bool, sign: bool, verify: bool, template: str, key: str) -> int:
    """Tool for Signing and Verifying Signatures of Cloud Templates"""

    init_logger()

    if prepare:
        if prepare_template(target_file_path=template, from_cli=True) is True:
            sys.exit(0)
    if sign:
        if create_signature(target_file_path=template, key_file_path=key, from_cli=True) is True:
            sys.exit(0)
    if verify:
        if verify_signature(target_file_path=template, key_file_path=key, from_cli=True) is True:
            sys.exit(0)
    sys.exit(1)


if __name__ == "__main__":
    main()  # pragma: no cover

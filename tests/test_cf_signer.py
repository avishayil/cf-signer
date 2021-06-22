#!/usr/bin/env python

"""Tests for `cf_signer` package."""

from click.testing import CliRunner

from cf_signer import cli


def test_create_signature():
    """Test the signing action."""
    runner = CliRunner()
    sign_result = runner.invoke(cli.main, ['--sign', '--template', 'tests/cf.template', '--key', 'tests/key.pem'])
    assert sign_result.exit_code == 0
    assert 'Signing completed successfully' in sign_result.output


def test_verify_signature():
    """Test the verify action."""
    runner = CliRunner()
    verify_result = runner.invoke(cli.main,
                                  ['--verify', '--template', 'tests/cf-signed.template', '--key', 'tests/pubkey.pem'])
    assert verify_result.exit_code == 0
    assert 'Signature verification completed successfully' in verify_result.output


def test_verify_wrong_signature():
    """Test the verify action."""
    runner = CliRunner()
    verify_result = runner.invoke(cli.main,
                                  ['--verify', '--template', 'tests/cf-signed.template', '--key', 'tests/wrongpubkey.pem'])
    assert verify_result.exit_code == 1
    assert 'Error validating template integrity' in verify_result.output


def test_verify_wrong_template():
    """Test the verify action."""
    runner = CliRunner()
    verify_result = runner.invoke(cli.main,
                                  ['--verify', '--template', 'tests/cf-tampered.template', '--key', 'tests/pubkey.pem'])
    assert verify_result.exit_code == 1
    assert 'Error validating template integrity' in verify_result.output

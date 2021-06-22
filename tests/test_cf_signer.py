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
    """Test the verify action with an invalid public key."""
    runner = CliRunner()
    verify_result = runner.invoke(cli.main,
                                  ['--verify', '--template', 'tests/cf-signed.template', '--key', 'tests/wrongpubkey.pem'])
    assert verify_result.exit_code == 1
    assert 'Error validating template integrity' in verify_result.output


def test_verify_wrong_template():
    """Test the verify action with a tampered template."""
    runner = CliRunner()
    verify_result = runner.invoke(cli.main,
                                  ['--verify', '--template', 'tests/cf-tampered.template', '--key', 'tests/pubkey.pem'])
    assert verify_result.exit_code == 1
    assert 'Error validating template integrity' in verify_result.output


def test_prepare_template():
    """Test the prepare template action."""
    runner = CliRunner()
    prepare_result = runner.invoke(cli.main, ['--prepare', '--template', 'tests/cf-unprepared.template'])
    assert prepare_result.exit_code == 0
    assert 'Template preparation completed successfully' in prepare_result.output

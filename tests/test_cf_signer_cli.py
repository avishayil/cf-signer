#!/usr/bin/env python

"""Tests for the ``cf_signer`` command line interface."""

from click.testing import CliRunner

from cf_signer import cli


def test_prepare_cli(unprepared_template_path):
    """The --prepare command normalizes a template and exits 0."""
    runner = CliRunner()
    result = runner.invoke(
        cli.main, ["--prepare", "--template", str(unprepared_template_path)]
    )
    assert result.exit_code == 0
    assert "Template preparation completed successfully" in result.output


def test_sign_cli(template_path, private_key_path):
    """The --sign command signs a template and exits 0."""
    runner = CliRunner()
    result = runner.invoke(
        cli.main,
        ["--sign", "--template", str(template_path), "--key", str(private_key_path)],
    )
    assert result.exit_code == 0
    assert "Signing completed successfully" in result.output


def test_verify_cli(signed_template_path, public_key_path):
    """The --verify command succeeds for a valid signature and exits 0."""
    runner = CliRunner()
    result = runner.invoke(
        cli.main,
        ["--verify", "--template", str(signed_template_path), "--key", str(public_key_path)],
    )
    assert result.exit_code == 0
    assert "Signature verification completed successfully" in result.output


def test_verify_wrong_key_cli(signed_template_path, wrong_public_key_path):
    """The --verify command fails with a mismatched public key and exits 1."""
    runner = CliRunner()
    result = runner.invoke(
        cli.main,
        [
            "--verify",
            "--template",
            str(signed_template_path),
            "--key",
            str(wrong_public_key_path),
        ],
    )
    assert result.exit_code == 1
    assert "Error validating template integrity" in result.output


def test_verify_tampered_template_cli(tampered_template_path, public_key_path):
    """The --verify command fails for a tampered template and exits 1."""
    runner = CliRunner()
    result = runner.invoke(
        cli.main,
        [
            "--verify",
            "--template",
            str(tampered_template_path),
            "--key",
            str(public_key_path),
        ],
    )
    assert result.exit_code == 1
    assert "Error validating template integrity" in result.output

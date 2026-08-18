#!/usr/bin/env python

"""Tests for the ``cf_signer`` library API."""

import json

from cf_signer.cf_signer import (
    create_signature,
    prepare_template,
    verify_signature,
)


def test_sign_verify_round_trip(template_path, private_key_path, public_key_path):
    """Signing then verifying a template with the matching key pair succeeds."""
    assert create_signature(
        target_file_path=str(template_path), key_file_path=str(private_key_path)
    ) is True

    signed = template_path.with_name("cf-signed.template")
    assert signed.exists()
    assert "Integrity" in json.loads(signed.read_text())["Metadata"]

    assert verify_signature(
        target_file_path=str(signed), key_file_path=str(public_key_path)
    ) is True


def test_verify_wrong_key_fails(signed_template_path, wrong_public_key_path):
    """Verification with an unrelated public key fails."""
    assert verify_signature(
        target_file_path=str(signed_template_path),
        key_file_path=str(wrong_public_key_path),
    ) is False


def test_verify_tampered_template_fails(tampered_template_path, public_key_path):
    """Verification of a template modified after signing fails."""
    assert verify_signature(
        target_file_path=str(tampered_template_path),
        key_file_path=str(public_key_path),
    ) is False


def test_sign_missing_template_errors_cleanly(private_key_path, tmp_path):
    """Signing a non-existent template returns False rather than raising."""
    missing = tmp_path / "does-not-exist.template"
    assert create_signature(
        target_file_path=str(missing), key_file_path=str(private_key_path)
    ) is False


def test_sign_missing_key_errors_cleanly(template_path, tmp_path):
    """Signing with a non-existent key returns False rather than raising."""
    missing_key = tmp_path / "no-key.pem"
    assert create_signature(
        target_file_path=str(template_path), key_file_path=str(missing_key)
    ) is False


def test_sign_invalid_key_errors_cleanly(template_path, tmp_path):
    """Signing with a malformed key file returns False rather than raising."""
    bad_key = tmp_path / "bad-key.pem"
    bad_key.write_text("not a real key")
    assert create_signature(
        target_file_path=str(template_path), key_file_path=str(bad_key)
    ) is False


def test_verify_missing_template_errors_cleanly(public_key_path, tmp_path):
    """Verifying a non-existent template returns False rather than raising."""
    missing = tmp_path / "does-not-exist.template"
    assert verify_signature(
        target_file_path=str(missing), key_file_path=str(public_key_path)
    ) is False


def test_verify_malformed_template_errors_cleanly(public_key_path, tmp_path):
    """Verifying a non-JSON template returns False rather than raising."""
    malformed = tmp_path / "malformed.template"
    malformed.write_text("this is not json")
    assert verify_signature(
        target_file_path=str(malformed), key_file_path=str(public_key_path)
    ) is False


def test_prepare_template(unprepared_template_path):
    """Preparing a template produces a normalized ``-prepared`` file."""
    assert prepare_template(target_file_path=str(unprepared_template_path)) is True
    prepared = unprepared_template_path.with_name("cf-unprepared-prepared.template")
    assert prepared.exists()


def test_prepare_missing_template_errors_cleanly(tmp_path):
    """Preparing a non-existent template returns False rather than raising."""
    missing = tmp_path / "does-not-exist.template"
    assert prepare_template(target_file_path=str(missing)) is False

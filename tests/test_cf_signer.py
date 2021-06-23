#!/usr/bin/env python

"""Tests for `cf_signer` package."""

from cf_signer.cf_signer import create_signature, verify_signature, prepare_template


def test_create_signature():
    """Test the signing action."""
    sign_result = create_signature(target_file_path='tests/cf.template', key_file_path='tests/key.pem')
    assert sign_result is True


def test_verify_signature():
    """Test the verify action."""
    verify_result = verify_signature(target_file_path='tests/cf-signed.template', key_file_path='tests/pubkey.pem')
    assert verify_result is True


def test_verify_wrong_signature():
    """Test the verify action with an invalid public key."""
    verify_result = verify_signature(target_file_path='tests/cf-signed.template', key_file_path='tests/wrongpubkey.pem')
    assert verify_result is False


def test_verify_wrong_template():
    """Test the verify action with a tampered template."""
    verify_result = verify_signature(target_file_path='tests/cf-tampered.template', key_file_path='tests/pubkey.pem')
    assert verify_result is False


def test_prepare_template():
    """Test the prepare template action."""
    prepare_result = prepare_template(target_file_path='tests/cf-unprepared.template')
    assert prepare_result is True

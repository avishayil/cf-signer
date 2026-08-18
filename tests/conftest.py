#!/usr/bin/env python

"""Shared pytest fixtures for the cf_signer test suite.

RSA keys are generated fresh in a temporary directory for every test run so
that no private keys are ever committed to the repository.
"""

import json
import shutil
from pathlib import Path

import pytest
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa

from cf_signer.cf_signer import create_signature

SAMPLE_TEMPLATE = Path(__file__).parent / "cf.template"


def _write_private_key(path: Path) -> rsa.RSAPrivateKey:
    """Generate an RSA private key and write it as an unencrypted PEM file."""
    private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.NoEncryption(),
    )
    path.write_bytes(pem)
    return private_key


def _write_public_key(private_key: rsa.RSAPrivateKey, path: Path) -> None:
    """Write the public key matching ``private_key`` as a PEM file."""
    pem = private_key.public_key().public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo,
    )
    path.write_bytes(pem)


@pytest.fixture
def private_key_path(tmp_path):
    """Path to a freshly generated RSA private key PEM file."""
    key_path = tmp_path / "key.pem"
    _write_private_key(key_path)
    return key_path


@pytest.fixture
def public_key_path(tmp_path, private_key_path):
    """Public key PEM matching ``private_key_path``."""
    private_key = serialization.load_pem_private_key(
        private_key_path.read_bytes(), password=None
    )
    pub_path = tmp_path / "pubkey.pem"
    _write_public_key(private_key, pub_path)
    return pub_path


@pytest.fixture
def wrong_public_key_path(tmp_path):
    """Public key PEM belonging to an unrelated key pair."""
    other_key = _write_private_key(tmp_path / "wrong-key.pem")
    pub_path = tmp_path / "wrongpubkey.pem"
    _write_public_key(other_key, pub_path)
    return pub_path


@pytest.fixture
def template_path(tmp_path):
    """Copy of the sample CloudFormation template inside ``tmp_path``."""
    dest = tmp_path / "cf.template"
    shutil.copy(SAMPLE_TEMPLATE, dest)
    return dest


@pytest.fixture
def signed_template_path(template_path, private_key_path):
    """A signed template produced by the signing routine under test."""
    assert create_signature(
        target_file_path=str(template_path), key_file_path=str(private_key_path)
    ) is True
    return template_path.with_name("cf-signed.template")


@pytest.fixture
def tampered_template_path(signed_template_path):
    """A signed template whose contents were modified after signing."""
    data = json.loads(signed_template_path.read_text())
    data["Description"] = "This template has been tampered with."
    tampered = signed_template_path.with_name("cf-tampered.template")
    tampered.write_text(json.dumps(data, indent=2))
    return tampered


@pytest.fixture
def unprepared_template_path(tmp_path):
    """An inconsistently indented template that needs preparation."""
    dest = tmp_path / "cf-unprepared.template"
    dest.write_text(
        '{\n  "AWSTemplateFormatVersion" : "2010-09-09",\n\n'
        '  "Description" : "Needs preparation"\n}\n'
    )
    return dest

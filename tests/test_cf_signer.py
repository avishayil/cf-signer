#!/usr/bin/env python

"""Tests for `cf_signer` package."""

import pytest

from click.testing import CliRunner

from cf_signer import cf_signer
from cf_signer import cli


@pytest.fixture
def response():
    """Sample pytest fixture.

    See more at: http://doc.pytest.org/en/latest/fixture.html
    """
    # import requests
    # return requests.get('https://github.com/audreyr/cookiecutter-pypackage')


def test_content(response):
    """Sample pytest test function with the pytest fixture as an argument."""
    # from bs4 import BeautifulSoup
    # assert 'GitHub' in BeautifulSoup(response.content).title.string


def test_create_signature():
    """Test the signing action."""
    runner = CliRunner()
    sign_result = runner.invoke(cli.main, ['--sign', '--template', 'tests/cf.template', '--key', 'tests/key.pem'])
    assert sign_result.exit_code == 0
    assert 'Signing completed succesfully.' in sign_result.output


def test_verify_signature():
    """Test the verify action."""
    runner = CliRunner()
    verify_result = runner.invoke(cli.main, ['--verify', '--template', 'tests/cf-signed.template', '--key', 'tests/pubkey.pem'])
    assert verify_result.exit_code == 0
    assert 'Signature verification completed succesfully.' in verify_result.output

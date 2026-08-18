=======
History
=======

0.1.0 (unreleased)
------------------

* refactor: replace PyOpenSSL with the maintained ``cryptography`` library (RSA PKCS#1 v1.5 over SHA-256; sign/verify behavior preserved)
* chore: migrate packaging from ``setup.py``/``setup.cfg`` to ``pyproject.toml``; console script renamed to ``cf-signer``
* ci: replace Travis CI with GitHub Actions (test matrix Python 3.9-3.13) and OIDC Trusted Publishing to PyPI
* chore: drop Python 3.6-3.8 support, add 3.9-3.13
* test: generate throwaway RSA keys in fixtures; add round-trip, tamper, wrong-key and error-handling tests

0.0.1 (2021-06-22)
------------------

* First release on PyPI.

0.0.2 (2021-06-22)
------------------

* feat: prepare template before signing
* feat: clear linter errors
* chore: version bump and documentation updates regarding installation

0.0.3 (2021-06-23)
------------------

* feat: added the usecase of using the library in python code, added pylint

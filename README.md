# Python implementation of the Bifid Cipher

This repository contains a simple implementation of the Bifid Cipher.

## Usage:
Create a BifidCipher object. You can create it using a predefined Polybius square, or you can generate one by default
by leaving the variable empty.

```python
from BifidCipher import BifidCipher

cipher = BifidCipher()
encrypted = cipher.encrypt_message('testing hello')
```

```doctest
>>> cipher.decrypt_message(encrypted)
QTIXTMFNHVND
```

Additionally, you can supply a period/block size for the BifidCipher in the constructor.

```python
from BifidCipher import BifidCipher

cipher = BifidCipher('ABCDEFGHIJKLMNOPQRSTUVWXYZ', period=3)
encrypted = cipher.encrypt_message('testing hello')
```
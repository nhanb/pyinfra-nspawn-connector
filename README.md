WIP

# Installation

```sh
pip install pyinfra
pip install git+https://github.com/nhanb/pyinfra-nspawn-connector.git
```

# Usage


```python
# inventory.py:
hosts = [
    ("@nspawn/machine-name", {}),
]

# or from the command line:
pyinfra @nspawn/machine-name exec -- cat /etc/os-release
```

# Installation

```sh
pip install pyinfra
pip install git+https://github.com/nhanb/pyinfra-nspawn-connector.git
```

# Usage


```python
# inventory.py:
hosts = [
    ("nspawn/machine_name", {}),
]

# or from the command line:
[sudo/doas] pyinfra @nspawn/my-machine exec -- cat /etc/os-release
```

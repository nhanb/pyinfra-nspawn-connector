# WIP

Feature checklist:

- [x] `run_shell_command`
- [x] `put_file`
- [ ] `get_file`

I've only implemented the bare minimum for my use case to work. YMMV.

Don't hold me responsible if this eats your files or kills your pets.
I'm not saying it will, but I ain't promising it 100% won't.

# Installation

```sh
pip install pyinfra
pip install git+https://github.com/nhanb/pyinfra-nspawn-connector.git
# or `poetry add --dev` if you're a responsible adult
# or `uv add --dev` if you're a proud webshitter
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

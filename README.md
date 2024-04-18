Software Quality and Reliability project.

# Install

## Development

### Nix
[Install](https://nixos.org/download/) nix through the install script and downgrade it to a stable release:
```bash
sh <(curl -L https://nixos.org/nix/install) --no-daemon
nix-env --install --file '<nixpkgs>' --attr nix cacert -I nixpkgs=channel:nixpkgs-stable
```

Pin registry version on the system:
```bash
nix registry add nixpkgs github:NixOS/nixpkgs/nixos-21.05
nix registry pin github:NixOS/nixpkgs/nixos-21.05
```

For caching in tests, build a few basic packages (optional):
```bash
nix build --no-link nixpkgs#glibc
nix build --no-link nixpkgs#hello
```


### BackEnd
1. Clone project
2. Install [poetry](https://python-poetry.org/docs/#installation) and [pre-commit](https://pre-commit.com/#install)
3. Run `poetry install` in root directory
4. Run `pre-commit install` to initialize pre-commit hooks (linters and formatters)
5. Run `poetry run dev` to run API backend

# Tests

For executing tests run `poetry run pytest`

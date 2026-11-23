# Bash exercise: development environment setup

This is a GitHub-ready solution to the course exercise. It checks for Python 3, installs it when missing using Homebrew (macOS) or apt-get (Debian/Ubuntu), creates an isolated virtual environment, installs Jupyter Notebook there, and runs `brew doctor` on macOS. It also includes timestamped logging, readable status messages, strict shell options, and `--dry-run`, `--verbose`, and `--quiet` flags.

## Run

```bash
chmod +x env_install.sh
./env_install.sh --dry-run
./env_install.sh
```

The real install may ask for your administrator password on Debian/Ubuntu. On macOS, install Homebrew first. Jupyter is installed in `~/.local/share/jupyter-venv` by default; override `JUPYTER_VENV` to choose another location. Review the commands before running on a machine you care about. The exercise's uninstall bonus is intentionally omitted because package managers cannot safely infer whether these packages were already present or are used elsewhere.

The script writes `env_install.log` in the current working directory. Add that log to `.gitignore` if you run the script inside a repository.

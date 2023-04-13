#!/usr/bin/env python3
import config
import os
import subprocess
import sys
from venv import EnvBuilder

# A venv manager
class Venv:
    name: str
    """The venv name"""
    packages: list[str]
    """The required packages"""
    _venv_dir: str
    """The venv directory"""

    def __init__(self, name: str, packages: list[str]) -> None:
        """Creates a venv manager with the given name and package requirements"""
        self.name = name
        self.packages = packages
        self._venv_dir = os.path.expanduser(f"~/.venv-wrapper/{ self.name }")
    
    def setup(self) -> None:
        """Setups the venv"""
        # Create or update the venv
        print(f"Setup venv in { self._venv_dir }...")
        env_builder = EnvBuilder(upgrade=True, with_pip=True, prompt=self.name, upgrade_deps=True)
        env_builder.create(self._venv_dir)

        # Install dependencies
        print(f"Installing packages...")
        if len(self.packages) > 0:
            args = [
                f"{ self._venv_dir }/bin/python3", "-m", "pip",
                "--require-virtualenv", "install", "--upgrade",
                *self.packages
            ]
            subprocess.run(args, check=True)
    
    def execv(self, binary_name: str, args: list[str] = []) -> None:
        """Executes the given binary within the venv"""
        os.execv(f"{ self._venv_dir }/bin/{ binary_name }", [binary_name, *args])


# Call `main` if we are executed as script
if __name__ == "__main__":
    # Create venv
    venv = Venv(config.name, config.packages)

    # Call the appropriate binary or setup the venv
    binary_name = os.path.basename(sys.argv[0])
    if binary_name == config.setup:
        venv.setup()
    else:
        venv.execv(binary_name, sys.argv[1:])

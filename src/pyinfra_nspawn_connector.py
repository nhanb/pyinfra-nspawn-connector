import subprocess
from typing import TYPE_CHECKING

from pyinfra.connectors.base import BaseConnector
from typing_extensions import Unpack

if TYPE_CHECKING:
    from pyinfra.api.arguments import ConnectorArguments


class PyinfraNspawnConnector(BaseConnector):
    handles_execution = True

    @staticmethod
    def make_names_data(name):
        yield (
            f"@nspawn/{name}",
            {"machine_name": name},
            ["@nspawn"],
        )

    def connect(self):
        """
        Ensure the container is up
        """
        subprocess.run(
            ["machinectl", "start", self.host.data.get("machine_name")],
            check=True,
        )
        return True

    def run_shell_command(
        self,
        command,
        print_output: bool = False,
        print_input: bool = False,
        **arguments: Unpack["ConnectorArguments"],
    ):
        machine_name = self.host.data.get("machine_name")
        full_cmd = [
            "machinectl",
            "shell",
            machine_name,
            "/usr/bin/bash",
            "-c",
            str(command),
        ]

        if print_input:
            print(">>", full_cmd)

        proc = subprocess.run(
            full_cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
        )

        if print_output:
            print("<<", proc.stdout)

        return (
            proc.returncode == 0,
            proc.stdout,
        )

    def put_file(
        self,
        filename_or_io,
        remote_filename,
        remote_temp_filename=None,  # ignored
        print_output: bool = False,
        print_input: bool = False,
        **arguments,
    ) -> bool:
        return False

    def get_file(
        self,
        remote_filename,
        filename_or_io,
        remote_temp_filename=None,  # ignored
        print_output: bool = False,
        print_input: bool = False,
        **arguments,
    ) -> bool:
        return False

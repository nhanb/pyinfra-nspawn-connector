import subprocess
from typing import TYPE_CHECKING

from pyinfra.connectors.base import BaseConnector
from pyinfra.connectors.util import CommandOutput, OutputLine
from typing_extensions import Unpack, override

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

    @override
    def connect(self) -> None:
        """
        Ensure the container is up
        """
        subprocess.run(
            ["machinectl", "start", self.host.data.machine_name],
            check=True,
        )

    def run_shell_command(
        self,
        command,
        print_output: bool = False,
        print_input: bool = False,
        **arguments: Unpack["ConnectorArguments"],
    ):
        machine_name = self.host.data.machine_name
        full_cmd = [
            "machinectl",
            # Commands with long outputs (e.g. `dpkg -l`) may "helpfully" pipe into
            # `less` automatically, blocking our whole script.
            # Setting PAGER=cat prevents that.
            "--setenv=PAGER=cat",
            "shell",
            machine_name,
            "/usr/bin/sh",
            "-c",
            str(command),
        ]

        if print_input:
            print(">>", full_cmd)

        proc = subprocess.run(
            full_cmd,
            capture_output=True,
            text=True,
        )

        if print_output:
            print("<<", proc.stdout)

        success = proc.returncode == 0

        stdout = [
            OutputLine(buffer_name="stdout", line=str(i + 1))
            for i, line in enumerate(proc.stdout.splitlines())
        ]
        stderr = [
            OutputLine(buffer_name="stderr", line=str(i + 1))
            for i, line in enumerate(proc.stderr.splitlines())
        ]
        command_output = CommandOutput(stdout + stderr)

        return (success, command_output)

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

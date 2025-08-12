import os
import subprocess
from tempfile import mkstemp
from typing import TYPE_CHECKING

from pyinfra.api.util import get_file_io
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

        command_prefix = []
        if arguments.get("_sudo"):
            command_prefix.extend(["/usr/bin/sudo", "-H", "--preserve-env=PAGER"])
            if sudo_user := arguments.get("_sudo_user"):
                command_prefix.extend(["-u", sudo_user])

        full_cmd = [
            "machinectl",
            "--quiet",  # prevent machinectl's own stderr output
            # Commands with long outputs (e.g. `dpkg -l`) may "helpfully" pipe into
            # `less` automatically, blocking our whole script.
            # Setting PAGER=cat prevents that.
            "--setenv=PAGER=cat",
            "shell",
            machine_name,
            *command_prefix,
            "/usr/bin/sh",
            "-c",
            str(command),
        ]

        if print_input:
            print(">>", full_cmd)

        proc = subprocess.run(full_cmd, capture_output=True, text=True)

        if print_output:
            print("<<", proc.stdout)

        success = proc.returncode == 0

        stdout = [
            OutputLine(buffer_name="stdout", line=line)
            for line in proc.stdout.splitlines()
        ]
        stderr = [
            OutputLine(buffer_name="stderr", line=line)
            for line in proc.stderr.splitlines()
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
        _, temp_filename = mkstemp()

        try:
            # Load our file or IO object and write it to the temporary file
            with get_file_io(filename_or_io) as file_io:
                with open(temp_filename, "wb") as temp_f:
                    data = file_io.read()

                    if isinstance(data, str):
                        data = data.encode()

                    temp_f.write(data)

            machine_name = self.host.data.machine_name

            full_cmd = [
                "machinectl",
                "copy-to",
                machine_name,
                temp_filename,
                remote_filename,
            ]

            if print_input:
                print(">>", full_cmd)

            proc = subprocess.run(full_cmd, capture_output=True, text=True)

            if print_output:
                print("<< stdout: ", proc.stdout)
                print("<< stderr: ", proc.stderr)

            success = proc.returncode == 0
            return success

        finally:
            os.remove(temp_filename)

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

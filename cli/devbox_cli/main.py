#!/usr/bin/env python

import socket
import os
import re
from typing import Callable
import click
import subprocess
from pathlib import Path


SCALEWAY_COMMAND = ["scw"]
SCALEWAY_INSTANCE_COMMAND = SCALEWAY_COMMAND + ["instance"]
PROJECT_ROOT_PATH: Path = (
    Path(os.path.dirname(os.path.realpath(__file__)))
    / ".." 
    / ".."
)

TERRAFORM_DEVBOX_DIR: Path = (
    PROJECT_ROOT_PATH 
    / "terraform"
    / "infrastructure"
    / "core"
    / "devbox"
)
TERRAFORM_COMMAND = ["terraform"]
STARTUP_TIMEOUT_SECONDS = 180
CONNECTION_TIMEOUT_SECONDS = 5
USER_HOST = "ubuntu"


@click.group()
def devbox_cli():
    ...


def _is_port_in_use(host: str, port: int, timeout_seconds: int = 10) -> bool:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(timeout_seconds)
        return s.connect_ex((host, port)) == 0


def _is_port_ready(host: str, port: int, timeout_seconds: int = 120) -> bool:
    check_timeout_seconds = 10
    iterations = timeout_seconds / check_timeout_seconds
    if iterations < 1:
        iterations = 1
    for i in range(int(iterations)):
        click.echo(
            click.style(
                f"Checking port {port} on {host}. (waiting {i*check_timeout_seconds} seconds)",
                fg="blue",
            )
        )
        if _is_port_in_use(host, port, check_timeout_seconds):
            return True
    return False


def _get_connection_address(output: str) -> str:
    """
    Get the connection address from the output of the terraform output command
    """
    # regex = r"IPv6\.Address\s+([0-9a-f:]+)"
    regex = "ID\s+([0-9a-f]{8}-[0-9a-f]{4}-[0-5][0-9a-f]{3}-[089ab][0-9a-f]{3}-[0-9a-f]{12})"
    click.echo(output)
    result = re.findall(regex, str(output))
    # return result[0]
    return f"{result[0]}.pub.instances.scw.cloud"


def _get_scaleway_devbox_terraform_output(output_name: str) -> str:
    """Get the Scaleway Devbox instance"""
    devbox_main_folder = TERRAFORM_DEVBOX_DIR / "01-devboxs"
    result = (
        subprocess.check_output(
            TERRAFORM_COMMAND
            + [
                f"-chdir={str(devbox_main_folder)}",
                "output",
                output_name,
            ],
            universal_newlines=True,
        )
        .strip()
        .strip('"')
    )
    return result


def _get_scaleway_devbox_id(tpid: str) -> str:
    """Get the Scaleway Devbox instance."""
    output = _get_scaleway_devbox_terraform_output(f"{tpid}_devbox_id")

    zone, instance_id = output.split("/")
    return zone, instance_id


def _remote_devbox_command(executor: Callable, instance: str, zone: str, command: str):
    """Execute a command using scw cli"""

    cmd = SCALEWAY_INSTANCE_COMMAND + ["server", command, instance, f"zone={zone}"]

    click.echo(" ".join(cmd))
    result = executor(cmd)
    return result


def _start_remote_devbox(instance: str, zone: str):
    """Start the Scaleway Devbox instance"""
    result = _remote_devbox_command(
        executor=subprocess.run, instance=instance, zone=zone, command="start"
    )
    return result


def _stop_remote_devbox(instance: str, zone: str):
    """Stop the Scaleway Devbox instance"""
    result = _remote_devbox_command(
        executor=subprocess.run, instance=instance, zone=zone, command="stop"
    )
    return result


def _wait_remote_devbox(instance: str, zone: str):
    """Wait for the Scaleway Devbox instance to be ready"""
    result = _remote_devbox_command(
        executor=subprocess.check_output, instance=instance, zone=zone, command="wait"
    )
    return result


def _connect_remote_devbox(address: str):
    """Connect to the Scaleway Devbox instance"""

    cmd = ["ssh", "-A", f"{USER_HOST}@{address}"]

    click.echo(" ".join(cmd))

    subprocess.run(cmd)


def _open_ide_remote_devbox(address: str):
    """Open the IDE connected to the Scaleway Devbox instance"""
    cmd = ["code", "--folder-uri", f"vscode-remote://ssh-remote+{USER_HOST}@{address}/home/{USER_HOST}"]

    click.echo(" ".join(cmd))

    subprocess.run(cmd)


def _copy_to_remote_devbox(origin: Path, destination: Path, address: str) -> None:
    """Copy a file to the Scaleway Devbox instance"""
    # If is a dir add -r to the cmd
    cmd = ["scp", "-r"] if origin.is_dir() else ["scp"]

    cmd += [str(origin), f"{USER_HOST}@{address}:{str(destination)}"]

    click.echo(click.style(" ".join(cmd), fg="green"))
    subprocess.run(cmd)

def _copy_local_files_to_remote_devbox(files_to_copy: list[Path]) -> None:
    """Copy local files to the Scaleway Devbox instance"""
    tpid = os.environ.get("TPID")
    zone, instance = _get_scaleway_devbox_id(tpid=tpid)

    click.echo(f"Connecting to {zone}/{instance}")
    output = _wait_remote_devbox(zone=zone, instance=instance)
    address = _get_connection_address(output)
    for origin, destination in files_to_copy:
        _copy_to_remote_devbox(origin=origin, destination=destination, address=address)

 
def _copy_to_workspace(origin: Path, destination: Path) -> None:
    """Copy local files to the Scaleway Devbox instance"""
    cmd = ["cp", "-r"] if origin.is_dir() else ["cp"]

    cmd += [str(origin), str(destination)]

    click.echo(click.style(" ".join(cmd), fg="green"))
    subprocess.run(cmd)

  

@devbox_cli.command()
def devbox_start_remote():
    """Start the Scaleway Devbox instance"""
    tpid = os.environ.get("TPID")
    zone, instance = _get_scaleway_devbox_id(tpid=tpid)
    _start_remote_devbox(zone=zone, instance=instance)


@devbox_cli.command()
def devbox_stop_remote():
    """Stop the Scaleway Devbox instance"""
    tpid = os.environ.get("TPID")
    zone, instance = _get_scaleway_devbox_id(tpid=tpid)
    _stop_remote_devbox(zone=zone, instance=instance)


@devbox_cli.command()
@click.option("--start", is_flag=True, help="Start the remote devbox")
def devbox_connect_remote(start):
    """Connect to the Scaleway Devbox instance"""
    tpid = os.environ.get("TPID")
    zone, instance = _get_scaleway_devbox_id(tpid=tpid)

    if start is True:
        _start_remote_devbox(zone=zone, instance=instance)

    click.echo(f"Connecting to {zone}/{instance}")
    output = _wait_remote_devbox(zone=zone, instance=instance)

    ipv6 = _get_connection_address(output)

    checking_timeout_seconds = (
        CONNECTION_TIMEOUT_SECONDS if start is False else STARTUP_TIMEOUT_SECONDS
    )

    server_ready = _is_port_ready(
        host=ipv6, port=22, timeout_seconds=checking_timeout_seconds
    )
    if server_ready is False:
        click.echo(click.style(f"Port 22 is not responding on {ipv6}", fg="red"))
        return

    _connect_remote_devbox(address=ipv6)


@devbox_cli.command()
@click.option("--start", is_flag=True, help="Start the remote devbox")
def devbox_open_remote_ide(start):
    """Open the IDE connected to the Scaleway Devbox instance"""
    tpid = os.environ.get("TPID")
    zone, instance = _get_scaleway_devbox_id(tpid=tpid)

    if start is True:
        _start_remote_devbox(zone=zone, instance=instance)

    click.echo(f"Connecting to {zone}/{instance}")
    output = _wait_remote_devbox(zone=zone, instance=instance)

    host = _get_connection_address(output)

    checking_timeout_seconds = (
        CONNECTION_TIMEOUT_SECONDS if start is False else STARTUP_TIMEOUT_SECONDS
    )

    server_ready = _is_port_ready(
        host=host, port=22, timeout_seconds=checking_timeout_seconds
    )

    if server_ready is False:
        click.echo(click.style(f"Port 22 is not responding on {host}", fg="red"))
        return

    _open_ide_remote_devbox(address=host)


@devbox_cli.command()
@click.option("--origin", "-o", help="Local path")
@click.option("--destination", "-d", help="Destination path")
def devbox_copy(origin, destination):
    """Copy a file or directory to the Scaleway Devbox instance"""
    tpid = os.environ.get("TPID")
    zone, instance = _get_scaleway_devbox_id(tpid=tpid)

    click.echo(f"Connecting to {zone}/{instance}")
    output = _wait_remote_devbox(zone=zone, instance=instance)
    address = _get_connection_address(output)
    _copy_to_remote_devbox(origin=origin, destination=destination, address=address)


@devbox_cli.command()
def devbox_copy_local_configs():
    """ Copy local configs to the Scaleway Devbox instance """

    files_to_copy = (
        (
            Path(".envrc"),
            Path("~/tlon/.envrc")
        ), (
            Path("terraform/infrastructure/core/devbox/01-devboxs/terraform.tfvars"),
            Path("~/tlon/terraform/infrastructure/core/devbox/01-devboxs/terraform.tfvars")
        ), (
            Path("terraform/infrastructure/core/registry/terraform.tfvars"),
            Path("~/tlon/terraform/infrastructure/core/registry/terraform.tfvars")
        ), (
            Path("terraform/infrastructure/development/k8s/01-main/terraform.tfvars"),
            Path("~/tlon/terraform/infrastructure/development/k8s/01-main/terraform.tfvars")
        ),
    )
    _copy_local_files_to_remote_devbox(files_to_copy)

@devbox_cli.command()
def dev_copy_to_workspace():
    """ Copy local configs to the workspace instance """

    files_to_copy = (
        (
            Path.home() / Path("tlon/.envrc"),
            PROJECT_ROOT_PATH / Path(".envrc")
        ), (
            Path.home() / Path("tlon/terraform/infrastructure/core/devbox/01-devboxs/terraform.tfvars"),
            PROJECT_ROOT_PATH / Path("terraform/infrastructure/core/devbox/01-devboxs/terraform.tfvars")
        ), (
            Path.home() / Path("tlon/terraform/infrastructure/core/registry/terraform.tfvars"),
            PROJECT_ROOT_PATH / Path("terraform/infrastructure/core/registry/terraform.tfvars")
        ), (
            Path.home() / Path("tlon/terraform/infrastructure/development/k8s/01-main/terraform.tfvars"),
            PROJECT_ROOT_PATH / Path("terraform/infrastructure/development/k8s/01-main/terraform.tfvars")
        ),
    )
    for origin, destination in files_to_copy:
        _copy_to_workspace(origin=origin, destination=destination)

if __name__ == "__main__":
    devbox_cli()

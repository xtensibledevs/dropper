
from __future__ import absolute_import, print_function, unicode_literals

from dropper_cli import pass_dropper_cli_env
from dropper_cli.api.build_api import DropBuilder, build_with_config
from .. import decorators, utils, validators
from ..utils import maybe_spinner

import click

'''
Build dropper services based of drops
Servicea re built once and then tagger, by default as `project_service`.
If the `Dropper.yaml` file specifies an image name, the image is tagger with that name, 
substututing any variables beforehand

If you change a service's `Dropper.yaml` or the contents of its build directory
repeate the command to rebuild it
'''
@click.command("build", short_help="Build or rebuild services from Dropper.yaml")
@click.argument("--build-arg", required=False, type=bool)
@click.argument("--no-cache", required=False, type=bool)
@click.argument("--progress", required=False, type=str)
@click.argument("--pull", required=False, type=str, short_help="Pull image before running")
@click.argument("-q", "--quiet", required=False, type=bool)
@click.argument("--ssh", required=False, type=str)
@pass_dropper_cli_env
def cmd_build(ctx, path):
	''' Build a drop from Dropper.yaml '''

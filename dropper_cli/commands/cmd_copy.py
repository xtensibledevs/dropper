from dropper_cli.dropper_cli import pass_dropper_cli_env

import click

'''
Copy files/folders between a service container and the local filesystem
'''
@click.command("copy")
@click.option("--archive", "-a", type=bool)
@click.option("--follow-link", "-L", type=bool)
@click.option("--index", required=False, type=int)
@pass_dropper_cli_env
def create_build_arg(build_arg: bool = False):
	pass

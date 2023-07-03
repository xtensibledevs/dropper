from dropper_cli.dropper_cli import pass_dropper_cli_env

import click

'''
Creates a drop for a service
'''
@click.command("create")
@click.option("--build", '-b', type=bool)
@click.option("--force-recreate", type=bool)
@click.option("--no-build", type=bool)
@click.option("--no-recreate", type=bool)
@click.option("--pull", type=str, short_help="Pull image before running")
@pass_dropper_cli_env
def cmd_create():
	pass

from dropper_cli.dropper_cli import pass_dropper_cli_env

import click

'''
Stop drops and removes drops, deallocates v-nets, volumes and deletes images created by create
By default only these are removed:
-> Drops for services defined in the Dropper.yaml file
-> Networks defined in the Dropper.yaml file
-> The default network used by the Dropper.yaml drops
'''
@click.command("stop")
@click.option("--remove-orphans", type=bool, required=False)
@click.option("--rmi", type=str, required=False)
@click.option("--timeout", "-t", type=int, required=False)
@click.option("-v", "--volumes", type=Sequence[str], required=False)
@pass_dropper_cli_env
def cmd_stop():
	pass

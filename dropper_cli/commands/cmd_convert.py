from dropper_cli.dropper_cli import pass_dropper_cli_env

import click

@click.command("convert", short_help="Convert the Dropper.yaml to canonical format")
@click.argument("--images", type=bool, required=False)
@click.argument("--hash", type=bool, required=False)
@click.argument("--services", type=bool, required=False)
@click.argument("--volumes", type=bool, required=False)
@click.argument("--format", required=False, type=click.Path(resovle_path=True))
@click.argument("--no-interpolate")
@pass_dropper_cli_env
def cmd_convert():
	pass
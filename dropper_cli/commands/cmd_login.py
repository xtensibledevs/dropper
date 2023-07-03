
from __future__ import absolute_import, print_function, unicode_literals

import collections
import stat

import click

from dropper_cli.api.user import get_user_token
from dropper_cli.utils import get_help_website
from dropper_cli import decorators
from dropper_cli.exceptions import handle_api_exceptions
from dropper_cli.dropper_cli import main

ConfigValues = collections.namedtuple("ConfigValues", ["reader", "present", "mode", "data"])

def validate_login(ctx, param, value):
	''' Ensure that the login is not blank '''
	value = value.strip()
	if not value:
		raise click.BadParameter("The value cannot be blank.", param=param)
	return value

@main.command(aliases=["token"])
@click.option("-l", "--login", required=True, callback=validate_login, prompt=True, help="Your XCloud ID")
@click.password_option("-p", "--password", help="Your XCLoud Login Credential")
@decorators.common_cli_config_opts
@decorators.common_cli_output_opts
@decorators.initialize_api
@click.pass_context
def login(ctx, opts, login, password):
	click.echo("Retriving API token for Dropper...")
	context_msg = "Failed to retrive API token"
	with handle_api_exceptions(ctx, opts=opts, context_msg=context_msg):
		with maybe_spinner(opts):
			api_key = get_user_token(login=login, password=password)

	click.secho("OK", fg="green")

	click.echo("Your API key/token is : %(token)s" % {"token": click.style(api_key, fg="magenta")})
	create, has_err = create_config_files(ctx, opts, api_key=api_key)

	if has_err:
		click.echo()
		click.secho("Oops, Error occured while creating config, try again!", fg="red")
		return

	if opts.api_key != api_key:
		click.echo()
		if opts.api_key:
			click.secho("Note : The above API key dosen't match what's already in the default config file", fg="yellow")
		elif not create:
			click.secho("Note : Don't forget to put the API key in a config file, export it to the env, or set it via -k.", fg="yellow")
		click.echo()

	click.secho("You're all set to rock!", fg="green")
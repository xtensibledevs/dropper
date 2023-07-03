class Dropper:
	def __init__(self):
		self.verbose = False
		self.dropper_home = os.getcwd()
		self.project_directory = None
		self.config = {}

	def log(self, msg, *args):
		if args:
			msg %= args
		click.echo(msg, file=sys.stderr)

	def set_config(self, key, value):
		self.config[key] = value
		if self.verbose:
			self.log(f"config [{key}] = {value}")

	def vlog(self, msg, *args):
		if self.verbose:
			self.log(msg, *args)

	def __repr__(self):
		return f"<Dropper {self.dropper_home}>"


pass_dropper_cli_env = click.make_pass_decorator(Dropper, ensure=True)

cmd_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), "commands"))

''' Dropper CLI application is a multicommand application '''
class DropperCLI(click.MultiCommand):
	def list_commands(self, ctx):
		rv = []
		for filename in os.listdir(cmd_folder):
			if filename.endswith(".py") and filename.startswith("cmd_"):
				rv.append(filename[4:-3])
		rv.sort()
		return rv

	def get_command(self, ctx, name):
		try:
			mod = __import__(f"complex.commands.cmd_{name}", None, None, ["cli"])
		except ImportError:
			return
		return mod.cli

@click.command(cls=DropperCLI, context_settings=CONTEXT_SETTINGS)
@click.option('--dropper-home', type=click.Path(exists=True, file_okay=False, resolve_path=True), help='Changes the folder to operate on')
@click.option('-v', '--verbose', is_flag=True, help="Enables verbose mode")
@click.argument('project-directory', is_flag=True, type=click.Path(exists=True, resolve_path=True), help='Set the project directory')
@click.argument('--config', type=click.Path(exists=True, resolve_path=True), help='The Dropper Config to load dropper with')
@pass_dropper_cli_env
def cli(ctx, verbose, dropper_home, project_directory):
	''' The entry point of the Dropper Cli Application '''
	ctx.verbose = verbose
	if dropper_home is not None:
		ctx.dropper_home = dropper_home
	if project_directory is not None:
		ctx.project_directory = project_directory

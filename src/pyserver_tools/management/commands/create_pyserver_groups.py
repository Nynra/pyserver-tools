from django.core.management.base import BaseCommand
from pyserver_tools.utils import create_group


class Command(BaseCommand):

    help = "Create the default groups for all install `pyserver_*` apps."

    def add_arguments(self, parser):
        parser.add_argument(
            "--force",
            type=bool,
            help="Whether to force the creation of the groups",
            default=False,
        )
        parser.add_argument(
            "--verbose",
            type=bool,
            help="Whether to print verbose output to the console",
            default=True,
        )

    def handle(self, *args, **options):
        verbose = options.get("verbose", True)
        # Check if the `pyserver_users` app is installed
        try:
            import pyserver_users

            self._run_pyserver_users_commands(options)
        except ImportError:
            if verbose:
                self.stdout.write(
                    "No `pyserver_users` app found. Skipping group creation."
                )

    def _run_pyserver_users_commands(self, options):
        # Run the django command to create the admin group
        verbose = options.get("verbose", True)
        if verbose:
            self.stdout.write("Creating the admin group")
        self.call_command("create_admin_group", **options)
        if verbose:
            self.stdout.write("Creating the user group")
        self.call_command("create_user_group", **options)
        if verbose:
            self.stdout.write("Creating the readonly group")
        self.call_command("create_readonly_group", **options)

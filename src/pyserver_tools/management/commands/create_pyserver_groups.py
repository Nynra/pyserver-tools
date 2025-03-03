from django.core.management.base import BaseCommand
from django.core.management import execute_from_command_line


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

        # Check if the `pyserver_cve_scraper` app is installed
        try:
            import pyserver_cve_scraper

            self._run_pyserver_cve_scraper_commands(options)
        except ImportError:
            if verbose:
                self.stdout.write(
                    "No `pyserver_cve_scraper` app found. Skipping group creation."
                )

    def _run_pyserver_users_commands(self, options):
        # Run the django command to create the admin group
        verbose = options.get("verbose", True)
        if options.get("force", False):
            force = ["--force", "True"]
        else:
            force = []
        if verbose:
            self.stdout.write("Creating the admin group")
        execute_from_command_line(["manage.py", "create_admin_group"] + force)

    def _run_pyserver_cve_scraper_commands(self, options):
        # Run the django command to create the scraping groups
        verbose = options.get("verbose", True)
        if options.get("force", False):
            force = ["--force", "True"]
        else:
            force = []
        if verbose:
            self.stdout.write("Creating the scraping groups")
        execute_from_command_line(["manage.py", "create_cve_scraper_groups"] + force)

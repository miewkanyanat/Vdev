from __future__ import unicode_literals

from optparse import make_option

from django import apps
from django.core import management


class Command(management.BaseCommand):
    help = 'Run all configured tests for the project.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--nomigrations', action='store_true', dest='nomigrations',
            default=False,
            help='Don\'t use migrations when creating the test database.'
        )

        parser.add_argument(
            '--reverse', action='store_true', dest='reverse', default=False,
            help='Reverses test cases order.'
        )

    def handle(self, *args, **options):
        kwargs = {}
        if options.get('nomigrations'):
            kwargs['nomigrations'] = True

        if options.get('reverse'):
            kwargs['reverse'] = True

        test_apps = [app.name for app in apps.apps.get_app_configs() if getattr(app, 'test', False)]

        print 'Testing: {}'.format(', '.join(test_apps))

        management.call_command('test', *test_apps, interactive=False, **kwargs)

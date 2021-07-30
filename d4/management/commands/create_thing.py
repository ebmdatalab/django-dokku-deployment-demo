from django.core.management import BaseCommand

from ...models import Thing


class Command(BaseCommand):
    help = "Create a Thing in the database"  # noqa: A003

    def add_arguments(self, parser):
        parser.add_argument("name")

    def handle(self, name, **options):
        Thing.objects.create(name=name)

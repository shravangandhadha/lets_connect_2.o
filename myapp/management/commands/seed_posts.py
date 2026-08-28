from django.core.management.base import BaseCommand
from myapp.models import Member, Post


class Command(BaseCommand):
    help = 'Create sample posts for development'

    def handle(self, *args, **options):
        author = Member.objects.filter(email__iexact='alice@example.com').first()
        if not author:
            self.stdout.write(self.style.NOTICE('No sample author found (alice@example.com). Run seed_profiles first.'))
            return

        samples = [
            {'title': 'Welcome to Let\'s Connect', 'content': 'This is a sample post to get the community started.'},
            {'title': 'Looking for collaborators', 'content': 'I am looking for frontend developers to build a demo app.'},
        ]
        created = 0
        for s in samples:
            if Post.objects.filter(title__iexact=s['title']).exists():
                self.stdout.write(self.style.NOTICE(f"Post '{s['title']}' exists; skipping."))
                continue
            Post.objects.create(author=author, title=s['title'], content=s['content'])
            created += 1
        self.stdout.write(self.style.SUCCESS(f'Created {created} posts.'))

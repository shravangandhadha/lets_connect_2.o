from django.core.management.base import BaseCommand
from django.contrib.auth.hashers import make_password
from myapp.models import Member


class Command(BaseCommand):
    help = 'Create sample Member records for development'

    def handle(self, *args, **options):
        samples = [
            {
                'name': 'Alice Johnson',
                'display_name': 'Alice',
                'email': 'alice@example.com',
                'password': 'password123',
                'avatar_url': 'https://i.pravatar.cc/150?img=1',
                'bio': 'Frontend developer and coffee lover.',
                'phone': '+1-555-0100',
                'city': 'Seattle',
                'state': 'WA',
                'country': 'USA',
                'interests': 'hiking, music, design',
            },
            {
                'name': 'Bob Smith',
                'display_name': 'Bob',
                'email': 'bob@example.com',
                'password': 'securepass',
                'avatar_url': 'https://i.pravatar.cc/150?img=2',
                'bio': 'Backend engineer, loves APIs.',
                'phone': '+1-555-0200',
                'city': 'Austin',
                'state': 'TX',
                'country': 'USA',
                'interests': 'programming, cycling',
            },
        ]

        created = 0
        for s in samples:
            if Member.objects.filter(email__iexact=s['email']).exists():
                self.stdout.write(self.style.NOTICE(f"Member {s['email']} already exists; skipping."))
                continue
            Member.objects.create(
                name=s['name'],
                display_name=s.get('display_name', ''),
                email=s['email'],
                password=make_password(s['password']),
                avatar_url=s.get('avatar_url', ''),
                bio=s.get('bio', ''),
                phone=s.get('phone', ''),
                city=s.get('city', ''),
                state=s.get('state', ''),
                country=s.get('country', ''),
                interests=s.get('interests', ''),
            )
            created += 1

        self.stdout.write(self.style.SUCCESS(f'Created {created} sample members.'))

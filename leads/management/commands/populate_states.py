"""
Management command to populate the State model with all US states.
Run with: python manage.py populate_states
"""

from django.core.management.base import BaseCommand
from leads.models import State, US_STATES


class Command(BaseCommand):
    help = 'Populate the State model with all US states'
    
    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Starting to populate states...'))
        
        created_count = 0
        updated_count = 0
        
        for code, name in US_STATES:
            state, created = State.objects.get_or_create(
                code=code,
                defaults={'name': name}
            )
            
            if created:
                created_count += 1
                self.stdout.write(f'Created: {name} ({code})')
            else:
                # Update the name if it's different
                if state.name != name:
                    state.name = name
                    state.save()
                    updated_count += 1
                    self.stdout.write(f'Updated: {name} ({code})')
        
        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully populated states! '
                f'Created: {created_count}, Updated: {updated_count}'
            )
        )

"""
Management command to test state filtering for lead subscribers.
Run with: python manage.py test_state_filtering <state_code>
"""

from django.core.management.base import BaseCommand
from leads.models import LeadsSubscriber, Lead
from django.db.models import Count, Q


class Command(BaseCommand):
    help = 'Test state filtering for lead subscribers'
    
    def add_arguments(self, parser):
        parser.add_argument('state_code', type=str, help='Two-letter state code to test (e.g., CA, NY)')
    
    def handle(self, *args, **options):
        state_code = options['state_code'].upper()
        
        self.stdout.write(f'Testing state filtering for state: {state_code}')
        self.stdout.write('-' * 50)
        
        # Show all subscribers
        all_subscribers = LeadsSubscriber.objects.filter(is_active=True)
        self.stdout.write(f'Total active subscribers: {all_subscribers.count()}')
        
        for subscriber in all_subscribers:
            states = list(subscriber.states.values_list('code', flat=True))
            states_str = ', '.join(states) if states else 'None (gets all states)'
            self.stdout.write(f'  - {subscriber.email}: {states_str}')
        
        self.stdout.write('')
        
        # Test the filtering logic
        filtered_subscribers = LeadsSubscriber.objects.filter(is_active=True).annotate(
            states_count=Count('states')
        ).filter(
            Q(states__code=state_code) | Q(states_count=0)
        ).distinct()
        
        self.stdout.write(f'Subscribers who would receive leads from {state_code}: {filtered_subscribers.count()}')
        
        for subscriber in filtered_subscribers:
            states = list(subscriber.states.values_list('code', flat=True))
            states_str = ', '.join(states) if states else 'None (gets all states)'
            self.stdout.write(f'  - {subscriber.email}: {states_str}')
        
        self.stdout.write('')
        self.stdout.write('Test completed!')

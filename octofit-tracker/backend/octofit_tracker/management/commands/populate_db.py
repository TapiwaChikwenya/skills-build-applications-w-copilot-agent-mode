from django.core.management.base import BaseCommand
from octofit_tracker.models import User, Team, Activity, Leaderboard, Workout
from django.db import connection

class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **options):
        self.stdout.write('Deleting old data...')
        User.objects.all().delete()
        Team.objects.all().delete()
        Activity.objects.all().delete()
        Leaderboard.objects.all().delete()
        Workout.objects.all().delete()

        self.stdout.write('Creating teams...')
        marvel = Team.objects.create(name='Marvel')
        dc = Team.objects.create(name='DC')

        self.stdout.write('Creating users...')
        ironman = User.objects.create(name='Iron Man', email='ironman@marvel.com', team=marvel)
        captain = User.objects.create(name='Captain America', email='cap@marvel.com', team=marvel)
        batman = User.objects.create(name='Batman', email='batman@dc.com', team=dc)
        superman = User.objects.create(name='Superman', email='superman@dc.com', team=dc)

        self.stdout.write('Creating activities...')
        Activity.objects.create(user=ironman, type='Running', duration=30, date='2026-02-25')
        Activity.objects.create(user=batman, type='Cycling', duration=45, date='2026-02-24')
        Activity.objects.create(user=superman, type='Swimming', duration=60, date='2026-02-23')
        Activity.objects.create(user=captain, type='Walking', duration=20, date='2026-02-22')

        self.stdout.write('Creating leaderboard...')
        Leaderboard.objects.create(team=marvel, points=100)
        Leaderboard.objects.create(team=dc, points=90)

        self.stdout.write('Creating workouts...')
        Workout.objects.create(name='Hero HIIT', description='High intensity workout for heroes', suggested_for='Marvel')
        Workout.objects.create(name='Power Yoga', description='Yoga for super strength', suggested_for='DC')

        self.stdout.write('Creating unique index on email for users...')
        db = connection.cursor().db_conn
        db.users.create_index([('email', 1)], unique=True)

        self.stdout.write(self.style.SUCCESS('Database populated with superhero test data!'))

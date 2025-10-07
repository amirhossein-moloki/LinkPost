import random
from django.core.management.base import BaseCommand
from django.db import transaction
from faker import Faker
import datetime

# Models
from django.contrib.auth.models import User
from content.models import (
    Campaign, Platform, PostType, PostStatus, Tag, Post, Comment, PostTag
)
from learning.models import Topic, Chapter, Lesson
from github.models import Repository, ChangeItem

class Command(BaseCommand):
    """
    Custom command to seed the database with sample data.
    Usage: python manage.py seed_data --number 100 --clean
    """
    help = 'Seeds the database with a specified number of posts and related data.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--number',
            type=int,
            default=50,
            help='The number of posts to create.'
        )
        parser.add_argument(
            '--clean',
            action='store_true',
            help='Clean the database before seeding.',
        )

    @transaction.atomic
    def handle(self, *args, **options):
        number_of_posts = options['number']
        clean_db = options['clean']
        fake = Faker()

        self.stdout.write(self.style.SUCCESS(f"Starting to seed the database with {number_of_posts} posts..."))

        if clean_db:
            self.stdout.write(self.style.WARNING("Cleaning the database..."))
            self._clean_database()

        self.stdout.write("Creating base data...")
        users = self._create_users(fake)
        campaigns = self._create_campaigns(fake)
        platforms = self._create_platforms()
        post_types = self._create_post_types(fake)
        statuses = self._create_post_statuses()
        tags = self._create_tags(fake)
        lessons = self._create_learning_items(fake)
        change_items = self._create_github_items(fake)
        self.stdout.write(self.style.SUCCESS("Base data created successfully."))

        self.stdout.write(f"Creating {number_of_posts} posts...")
        for i in range(number_of_posts):
            post = Post.objects.create(
                change_item=random.choice(change_items) if change_items else None,
                campaign=random.choice(campaigns),
                platform=random.choice(platforms),
                post_type=random.choice(post_types),
                status=random.choice(statuses),
                lesson=random.choice(lessons) if lessons else None,
                title=fake.sentence(nb_words=6),
                body=fake.paragraph(nb_sentences=5),
                scheduled_at=fake.date_time_this_year(after_now=True, tzinfo=datetime.timezone.utc),
            )

            # Add tags
            if tags:
                num_tags_to_add = random.randint(1, min(5, len(tags)))
                post_tags = random.sample(tags, k=num_tags_to_add)
                for tag in post_tags:
                    PostTag.objects.create(post=post, tag=tag)

            # Add comments
            for _ in range(random.randint(0, 7)):
                Comment.objects.create(
                    post=post,
                    author=random.choice(users),
                    text=fake.sentence(),
                )

            if (i + 1) % 10 == 0:
                self.stdout.write(f"  {i + 1}/{number_of_posts} posts created...")


        self.stdout.write(self.style.SUCCESS(f"Successfully seeded the database with {number_of_posts} posts."))

    def _clean_database(self):
        """Deletes all data from the relevant models."""
        Comment.objects.all().delete()
        PostTag.objects.all().delete()
        Post.objects.all().delete()
        Campaign.objects.all().delete()
        Platform.objects.all().delete()
        PostType.objects.all().delete()
        PostStatus.objects.all().delete()
        Tag.objects.all().delete()
        Lesson.objects.all().delete()
        Chapter.objects.all().delete()
        Topic.objects.all().delete()
        ChangeItem.objects.all().delete()
        Repository.objects.all().delete()
        User.objects.filter(is_superuser=False).delete()
        self.stdout.write(self.style.SUCCESS("Database cleaned successfully."))

    def _create_users(self, fake, count=10):
        users = []
        for _ in range(count):
            users.append(User.objects.create_user(username=fake.user_name(), email=fake.email(), password='password'))
        # Ensure at least one superuser
        if not User.objects.filter(is_superuser=True).exists():
            User.objects.create_superuser('admin', 'admin@example.com', 'admin')
        return list(User.objects.all())

    def _create_campaigns(self, fake, count=5):
        return [Campaign.objects.create(name=fake.company(), description=fake.catch_phrase()) for _ in range(count)]

    def _create_platforms(self):
        platform_names = ["LinkedIn", "Instagram", "Twitter", "Facebook", "Blog"]
        return [Platform.objects.get_or_create(name=name)[0] for name in platform_names]

    def _create_post_types(self, fake, count=3):
        return [PostType.objects.create(name=fake.word(), description=fake.sentence()) for _ in range(count)]

    def _create_post_statuses(self):
        statuses = [
            ('Draft', 1), ('In Review', 2), ('Approved', 3), ('Scheduled', 4), ('Published', 5)
        ]
        return [PostStatus.objects.get_or_create(name=name, defaults={'order': order})[0] for name, order in statuses]

    def _create_tags(self, fake, count=20):
        words = set()
        # Try to generate unique words, but with a limit to avoid infinite loops
        for _ in range(count * 2):
            if len(words) >= count:
                break
            words.add(fake.word().lower())
        return [Tag.objects.get_or_create(name=word)[0] for word in words]

    def _create_learning_items(self, fake, topics=3, chapters_per_topic=2, lessons_per_chapter=3):
        lessons = []
        for _ in range(topics):
            topic = Topic.objects.create(name=fake.bs(), description=fake.sentence())
            for _ in range(chapters_per_topic):
                chapter = Chapter.objects.create(topic=topic, name=fake.catch_phrase(), description=fake.sentence())
                for _ in range(lessons_per_chapter):
                    lesson = Lesson.objects.create(chapter=chapter, name=fake.job(), content=fake.text())
                    lessons.append(lesson)
        return lessons

    def _create_github_items(self, fake, repos=2, items_per_repo=5):
        change_items = []
        for _ in range(repos):
            repo = Repository.objects.create(
                owner=fake.user_name(),
                name=fake.slug(),
                full_name=fake.company(),
                default_branch='main'
            )
            for _ in range(items_per_repo):
                item = ChangeItem.objects.create(
                    repository=repo,
                    item_type=random.choice(['commit', 'pr', 'issue']),
                    source_item_id=fake.sha1(),
                    title=fake.sentence(),
                    summary=fake.text(),
                    url=fake.url(),
                    changed_at=fake.date_time_this_decade(tzinfo=datetime.timezone.utc),
                    raw_payload={'message': fake.text()}
                )
                change_items.append(item)
        return change_items
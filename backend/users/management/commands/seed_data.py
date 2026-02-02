from django.core.management.base import BaseCommand
from django.utils import timezone

from users.models import User
from posts.models import Tag, Post, Comment, Reaction


class Command(BaseCommand):
    help = "Seed database with realistic demo data."

    def handle(self, *args, **options):
        users_data = [
            ("alice", "alice@example.com"),
            ("bruno", "bruno@example.com"),
            ("chloe", "chloe@example.com"),
        ]
        created_users = []
        for username, email in users_data:
            user, created = User.objects.get_or_create(
                username=username,
                defaults={"email": email, "is_active": True},
            )
            if created:
                user.set_password("Password123!")
                user.save()
                created_users.append(username)

        tags = ["Django", "React", "DevOps", "UX", "Data"]
        tag_objs = {name: Tag.objects.get_or_create(name=name)[0] for name in tags}

        posts_data = [
            (
                "Lancer un blog avec Django",
                "Guide pas à pas pour démarrer un backend robuste avec Django REST Framework.",
                "alice",
                ["Django", "DevOps"],
            ),
            (
                "React + Vite en 2025",
                "Pourquoi Vite simplifie le développement frontend moderne et comment en profiter.",
                "bruno",
                ["React", "UX"],
            ),
            (
                "Authentification sécurisée",
                "Bonnes pratiques JWT, refresh tokens et cookies HTTP-only.",
                "chloe",
                ["Django"],
            ),
            (
                "Optimiser les performances",
                "Mise en cache, index DB et pagination pour une app fluide.",
                "alice",
                ["Data", "DevOps"],
            ),
            (
                "Design d’interface efficace",
                "Conseils UI/UX pour des interfaces claires et accessibles.",
                "bruno",
                ["UX"],
            ),
        ]

        created_posts = []
        for title, content, author_username, tag_list in posts_data:
            author = User.objects.get(username=author_username)
            post, created = Post.objects.get_or_create(
                title=title,
                defaults={
                    "content": content,
                    "author": author,
                    "published_at": timezone.now(),
                },
            )
            if created:
                post.tags.set([tag_objs[t] for t in tag_list])
                created_posts.append(title)

        comments_data = [
            ("Lancer un blog avec Django", "chloe", "Super clair, merci !"),
            ("React + Vite en 2025", "alice", "Vite est vraiment rapide, confirmé."),
            (
                "Authentification sécurisée",
                "bruno",
                "Les cookies HTTP-only sont indispensables.",
            ),
            (
                "Optimiser les performances",
                "chloe",
                "La pagination a tout changé chez moi.",
            ),
            (
                "Design d’interface efficace",
                "alice",
                "Très bon rappel sur l’accessibilité.",
            ),
        ]
        for post_title, author_username, content in comments_data:
            post = Post.objects.get(title=post_title)
            author = User.objects.get(username=author_username)
            if not Comment.objects.filter(
                post=post, author=author, content=content
            ).exists():
                Comment.objects.create(post=post, author=author, content=content)

        reactions_data = [
            ("Lancer un blog avec Django", "bruno", "LIKE"),
            ("React + Vite en 2025", "chloe", "LOVE"),
            ("Authentification sécurisée", "alice", "WOW"),
            ("Optimiser les performances", "bruno", "LIKE"),
            ("Design d’interface efficace", "chloe", "HAHA"),
        ]
        for post_title, username, emoji in reactions_data:
            post = Post.objects.get(title=post_title)
            user = User.objects.get(username=username)
            Reaction.objects.get_or_create(post=post, user=user, emoji=emoji)

        self.stdout.write(self.style.SUCCESS(f"Users created: {created_users}"))
        self.stdout.write(self.style.SUCCESS(f"Posts created: {created_posts}"))

from django.db import models
from django.conf import settings


class Contributors(models.Model):

    class Role(models.TextChoices):
        AUTHOR = 'auteur'
        CONTRIBUTOR = 'contributeur'

    class Permission(models.TextChoices):
        ALL = 'AUTHOR'
        READ = 'CONTRIBUTOR'

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='contributors')
    project = models.ForeignKey('Projects', on_delete=models.CASCADE, related_name='contributors')
    permission = models.CharField(choices=Permission.choices, max_length=30)
    role = models.CharField(choices=Role.choices, max_length=135)


class Projects(models.Model):

    class Type(models.TextChoices):
        BACK_END = 'back-end'
        FRONT_END = 'front-end'
        IOS = 'ios'
        ANDROID = 'android'

    title = models.CharField(max_length=135)
    description = models.CharField(default=False, max_length=135)
    type = models.CharField(choices=Type.choices, max_length=20)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='authors')

    def __str__(self):
        return self.title


class Issues(models.Model):

    class Priority(models.TextChoices):
        WEAK = 'faible'
        AVERAGE = 'moyenne'
        HIGH = 'eleve'

    class Tag(models.TextChoices):
        BUG = 'bug'
        IMPROVEMENT = 'amelioration'
        TASK = 'taches'

    class Status(models.TextChoices):
        TO_DO = 'a faire'
        IN_PROGRESS = 'en cours'
        FINISHED = 'termine'

    title = models.CharField(max_length=135)
    desc = models.CharField(max_length=135)
    tag = models.CharField(choices=Tag.choices, max_length=20)
    priority = models.CharField(choices=Priority.choices, max_length=20)
    project = models.ForeignKey('Projects', on_delete=models.CASCADE, related_name='issues')
    status = models.CharField(choices=Status.choices, max_length=20)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='issues')
    assignee = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='issues_assignee')
    created_time = models.DateTimeField(auto_now_add=True)


class Comments(models.Model):
    description = models.CharField(max_length=135)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='comments')
    issue = models.ForeignKey('Issues', on_delete=models.CASCADE, related_name='comments')
    created_time = models.DateTimeField(auto_now_add=True)

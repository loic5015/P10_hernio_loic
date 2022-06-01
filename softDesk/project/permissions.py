from rest_framework.permissions import BasePermission
from .models import Projects, Contributors, Issues, Comments


class IsAuthorize(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated)


class IsOwnerOrContributorProject(BasePermission):

    def has_object_permission(self, request, view, obj):
        if obj.author == request.user or request.user in obj.contributors.all():
            return True
        return False


class IsOwner(BasePermission):
    def has_permission(self, request, view):
        try:
            project = Projects.objects.get(id=view.kwargs['pk'])
        except Projects.DoesNotExist:
            return False
        if project.author == request.user:
            return True
        return False


class IsOwnerProject(BasePermission):
    def has_permission(self, request, view):
        try:
            project = Projects.objects.get(id=view.kwargs['project_pk'])
        except Projects.DoesNotExist:
            return False
        if project.author == request.user:
            return True
        return False


class IsOwnerOrContributorIssue(BasePermission):

    def has_permission(self, request, view):
        try:
            contributors = Contributors.objects.all().filter(project=view.kwargs['project_pk'])
        except Contributors.DoesNotExist:
            return False

        for contributor in contributors:
            if request.user == contributor.user:
                return True
        return False


class IsOwnerIssue(BasePermission):
    def has_permission(self, request, view):
        try:
            issue = Issues.objects.get(id=view.kwargs['pk'])
        except Issues.DoesNotExist:
            return False
        if issue.author == request.user:
            return True
        return False


class IsOwnerComment(BasePermission):
    def has_permission(self, request, view):
        try:
            comment = Comments.objects.get(id=view.kwargs['pk'])
        except Comments.DoesNotExist:
            return False
        if comment.author == request.user:
            return True
        return False

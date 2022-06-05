from rest_framework.permissions import BasePermission
from .models import Projects, Contributors, Issues, Comments


class IsAuthorize(BasePermission):
    """
    Grant permission for user authenticated
    """
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated)


class IsOwnerOrContributorProject(BasePermission):
    """
    Grant permission for user is author or contributors
    """

    def has_object_permission(self, request, view, obj):
        if obj.author == request.user or request.user in obj.contributors.all():
            return True
        return False


class IsOwner(BasePermission):
    """
    Grant permission for user is owner of the project
    """
    def has_permission(self, request, view):
        try:
            project = Projects.objects.get(id=view.kwargs['pk'])
        except Projects.DoesNotExist:
            return False
        if project.author == request.user:
            return True
        return False


class IsOwnerProject(BasePermission):
    """
       Grant permission for user is owner of the project
    """
    def has_permission(self, request, view):
        try:
            project = Projects.objects.get(id=view.kwargs['project_pk'])
        except Projects.DoesNotExist:
            return False
        if project.author == request.user:
            return True
        return False


class IsOwnerOrContributorIssue(BasePermission):
    """
       Grant permission for user is owner or contributor of the project
       """

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
    """
       Grant permission for user is owner of the issue
    """
    def has_permission(self, request, view):
        try:
            issue = Issues.objects.get(id=view.kwargs['pk'])
        except Issues.DoesNotExist:
            return False
        if issue.author == request.user:
            return True
        return False


class IsOwnerComment(BasePermission):
    """
       Grant permission for user is owner of the comment
    """
    def has_permission(self, request, view):
        try:
            comment = Comments.objects.get(id=view.kwargs['pk'])
        except Comments.DoesNotExist:
            return False
        if comment.author == request.user:
            return True
        return False

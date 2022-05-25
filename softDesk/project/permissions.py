from rest_framework.permissions import BasePermission
from .models import Projects


class IsAuthorize(BasePermission):
    def is_authenticated(self, request, view):
        return bool(request.user and request.user.is_authenticated)


class IsOwnerOrContributorProject(BasePermission):

    def is_authorize_project(self, request, view, obj):
        if obj.author == request.user or request.user in obj.contributors.all():
            return True
        return False


class IsOwner(BasePermission):
    def is_owner(self, request, view, obj):
        if obj.author == request.user:
            return True
        return False


class IsOwnerOrContributorIssue(BasePermission):

    def is_authorize_issue(self, request, view, obj):
        try:
            project = Projects.objects.get(id=view.kwargs['projects_pk'])
        except Projects.DoesNotExist:
            return False

        if project.author == request.user or request.user in project.contributors.all():
            return True
        return False

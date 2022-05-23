from django.shortcuts import render, get_object_or_404
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from .serializers import ProjectsListSerializer, \
    ContributorsDetailSerializer, IssuesListSerializer, CommentsListSerializer
from .models import Projects, Contributors, Issues, Comments
from .permissions import IsProjectAuthorize, IsOwnerOrContributorProject, IsOwner, IsOwnerOrContributorIssue
from authentication.models import Users



class MultipleSerializerMixin:
    # Un mixin est une classe qui ne fonctionne pas de façon autonome
    # Elle permet d'ajouter des fonctionnalités aux classes qui les étendent

    detail_serializer_class = None

    def get_serializer_class(self):
        # Notre mixin détermine quel serializer à utiliser
        # même si elle ne sait pas ce que c'est ni comment l'utiliser
        if self.action == 'retrieve' and self.detail_serializer_class is not None:
            # Si l'action demandée est le détail alors nous retournons le serializer de détail
            return self.detail_serializer_class
        return super().get_serializer_class()


class AdminProjectsViewset(ModelViewSet):

    serializer_class = ProjectsListSerializer

    def get_permissions(self):
        if self.action == 'list':
            permission_classes = [IsOwnerOrContributorProject]
        elif self.action == 'create':
            permission_classes = [IsProjectAuthorize]
        else:
            permission_classes = [IsOwner]

        return [permission() for permission in permission_classes]


    def list(self, request, *args, **kwargs):
        queryset = Projects.objects.all().filter(author=self.request.user.id)
        serializer = ProjectsListSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def create(self, request, *args, **kwargs):
        project = Projects(author=self.request.user)
        serializer = ProjectsListSerializer(project, data=request.data)
        if serializer.is_valid():
            serializer.save()
            contributor = Contributors.objects.create(
                project=project,
                user=request.user,
                role="auteur",
                permission="AUTHOR",
            )
            contributor.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None, *args, **kwargs):
        queryset = Projects.objects.all()
        project = get_object_or_404(queryset, pk=pk)
        serializer = ProjectsListSerializer(project, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def destroy(self, request, pk=None, *args, **kwargs):
        queryset = Projects.objects.all()
        project = get_object_or_404(queryset, pk=pk)
        project.delete()
        return Response(data={'reponse': 'project supprimé'}, status=status.HTTP_201_CREATED)


class UsersProjectlistViewset(ModelViewSet):

    queryset = Contributors.objects.all()
    serializer_class = ContributorsDetailSerializer

    def get_permissions(self):
        if self.action == 'list' or self.action == 'create':
            permission_classes = [IsOwnerOrContributorProject]
        else:
            permission_classes = [IsOwner]
        return [permission() for permission in permission_classes]

    def list(self, request, project_pk=None, *args, **kwargs):
        queryset = self.queryset.filter(project=project_pk)
        serializer = ContributorsDetailSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


    def create(self, request, project_pk=None, *args, **kwargs):
        projects = Projects.objects.all()
        project = get_object_or_404(projects, pk=project_pk)
        user = Users.objects.get(email=request.data['email'])
        if project is not None and user is not None:
            contributor = Contributors.objects.create(
                project=project,
                user=user,
                role="contributeur",
                permission="CONTRIBUTOR",
            )
            contributor.save()
            return Response(data={'success': 'utilisateur ajouté'}, status=status.HTTP_201_CREATED)
        else:
            return Response(data={'error': 'project inconnu ou utilisateur inconnu'}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, project_pk=None, pk=None, *args, **kwargs):
        contributors = get_object_or_404(self.queryset, pk=project_pk, user=pk)
        if contributors is not None:
            for contributor in queryset:
                contributor.delete()
            return Response(data={'success': 'utilisateur supprimé'}, status=status.HTTP_201_CREATED)
        else:
            return Response(data={'error': 'project inconnu ou utilisateur inconnu'}, status=status.HTTP_400_BAD_REQUEST)


class IssuesProjectlistViewset(ModelViewSet):
    queryset = Issues.objects.all()
    serializer_class = IssuesListSerializer

    def get_permissions(self):
        if self.action == 'list' or self.action == 'create':
            permission_classes = [IsOwnerOrContributorIssue]
        else:
            permission_classes = [IsOwner]
        return [permission() for permission in permission_classes]

    def list(self, request, project_pk=None, *args, **kwargs):
        queryset = self.queryset.filter(project=project_pk)
        serializer = IssuesListSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


    def create(self, request, project_pk=None, *args, **kwargs):
        projects = Projects.objects.all()
        project = get_object_or_404(projects, pk=project_pk)
        assignee = Users.objects.get(id=request.data['assignee'])
        if project is not None:
            issue = Issues(project=project, author=self.request.user, assignee=assignee)
            serializer = IssuesListSerializer(issue, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors,
                                status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(data={'error': 'project inconnu ou utilisateur inconnu'}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, project_pk=None, pk=None, *args, **kwargs):
        issue = get_object_or_404(self.queryset, pk=pk)
        assignee = Users.objects.get(id=request.data['assignee'])
        serializer = IssuesListSerializer(issue, data=request.data)
        if serializer.is_valid():
            serializer.save(assignee=assignee)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, project_pk=None, pk=None, *args, **kwargs):
        issue = get_object_or_404(self.queryset, pk=pk)
        if issue is not None:
            issue.delete()
            return Response(data={'reponse': 'problème supprimé'}, status=status.HTTP_201_CREATED)
        else:
            return Response(data={'error': 'problème inconnu'}, status=status.HTTP_400_BAD_REQUEST)


class CommentsProjectListViewset(ModelViewSet):
    queryset = Comments.objects.all()
    serializer_class = CommentsListSerializer

    def get_permissions(self):
        if self.action == 'list' or self.action == 'create' or self.action == 'retrieve':
            permission_classes = [IsOwnerOrContributorProject]
        else:
            permission_classes = [IsOwner]

        return [permission() for permission in permission_classes]

    def list(self, request, project_pk=None, issue_pk=None, *args, **kwargs):
        queryset = self.queryset.filter(issue=issue_pk)
        serializer = CommentsListSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


    def create(self, request, project_pk=None, issue_pk=None, *args, **kwargs):
        issues = Issues.objects.all()
        issue = get_object_or_404(issues, pk=issue_pk)
        if issue is not None:
            comment = Comments(issue=issue, author=self.request.user)
            serializer = CommentsListSerializer(comment, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors,
                                status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(data={'error': 'probleme inconnu'}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, project_pk=None, pk=None, *args, **kwargs):
        comment = get_object_or_404(self.queryset, pk=pk)
        serializer = CommentsListSerializer(comment, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, project_pk=None, pk=None, *args, **kwargs):
        comment = get_object_or_404(self.queryset, pk=pk)
        if comment is not None:
            comment.delete()
            return Response(data={'reponse': 'commentaire supprimé'}, status=status.HTTP_201_CREATED)
        else:
            return Response(data={'error': 'commentaire inconnu'}, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None, *args, **kwargs):
        comment = get_object_or_404(self.queryset, pk=pk)
        serializer = CommentsListSerializer(comment)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
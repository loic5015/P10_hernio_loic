from django.shortcuts import get_object_or_404
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from .serializers import ProjectsListSerializer,\
    ContributorsDetailSerializer, IssuesListSerializer, CommentsListSerializer, ProjectsDetailSerializer
from .models import Projects, Contributors, Issues, Comments
from .permissions import IsAuthorize, IsOwnerOrContributorProject, IsOwner, IsOwnerOrContributorIssue, IsOwnerProject, \
    IsOwnerIssue, IsOwnerComment

from authentication.models import Users


class AdminProjectsViewset(ModelViewSet):
    queryset = Projects.objects.all()
    serializer_class = ProjectsListSerializer

    def get_permissions(self):
        if self.action == 'list' or self.action == 'get':
            permission_classes = [IsAuthorize, IsOwnerOrContributorProject]
        elif self.action == 'create':
            permission_classes = [IsAuthorize]
        else:
            permission_classes = [IsAuthorize, IsOwner]

        return [permission() for permission in permission_classes]

    def list(self, request, *args, **kwargs):
        contributors = Contributors.objects.all().filter(user=self.request.user.id)
        project_id = [contributor.project.id for contributor in contributors]
        projects = []
        for id in project_id:
            project = get_object_or_404(self.queryset, id=id)
            projects.append(project)
        serializer = ProjectsListSerializer(projects, many=True)
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

    def get(self, request, pk=None, *args, **kwargs):
        queryset = get_object_or_404(self.queryset, pk=pk)
        print(queryset)
        if queryset is None:
            return Response({'error', 'project not  exists'}, status=status.HTTP_400_BAD_REQUEST)
        serializer = ProjectsDetailSerializer(queryset)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None, *args, **kwargs):
        project = get_object_or_404(self.queryset, pk=pk)
        if project is None:
            return Response({'error', 'project not  exists'}, status=status.HTTP_400_BAD_REQUEST)
        serializer = ProjectsListSerializer(project, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None, *args, **kwargs):
        project = get_object_or_404(self.queryset, pk=pk)
        project.delete()
        return Response(data={'response': 'project deleted'}, status=status.HTTP_201_CREATED)


class UsersProjectlistViewset(ModelViewSet):

    queryset = Contributors.objects.all()
    serializer_class = ContributorsDetailSerializer

    def get_permissions(self):
        if self.action == 'list' or self.action == 'create':
            permission_classes = [IsAuthorize, IsOwnerOrContributorIssue]
        else:
            permission_classes = [IsAuthorize, IsOwnerProject]
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
            return Response(data={'success': 'user added'}, status=status.HTTP_201_CREATED)
        else:
            return Response(data={'error': 'project unknow or user unknow'}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, project_pk=None, pk=None, *args, **kwargs):
        contributor = get_object_or_404(self.queryset, project=project_pk, user=pk)
        if contributor is not None:
            contributor.delete()
            return Response(data={'success': 'user deleted'}, status=status.HTTP_201_CREATED)
        else:
            return Response(data={'error': 'project unknow or user unknow'}, status=status.HTTP_400_BAD_REQUEST)


class IssuesProjectlistViewset(ModelViewSet):
    queryset = Issues.objects.all()
    serializer_class = IssuesListSerializer

    def get_permissions(self):
        if self.action == 'list' or self.action == 'create':
            permission_classes = [IsAuthorize, IsOwnerOrContributorIssue]
        else:
            permission_classes = [IsAuthorize, IsOwnerIssue]
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
            return Response(data={'error': 'project unknow ou user unknow'}, status=status.HTTP_400_BAD_REQUEST)

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
            return Response(data={'response': 'issue deleted'}, status=status.HTTP_201_CREATED)
        else:
            return Response(data={'error': 'issue unknow'}, status=status.HTTP_400_BAD_REQUEST)


class CommentsProjectListViewset(ModelViewSet):
    queryset = Comments.objects.all()
    serializer_class = CommentsListSerializer

    def get_permissions(self):
        if self.action == 'list' or self.action == 'create' or self.action == 'retrieve':
            permission_classes = [IsAuthorize, IsOwnerOrContributorIssue]
        else:
            permission_classes = [IsAuthorize, IsOwnerComment]

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
            return Response(data={'error': 'issue unknow'}, status=status.HTTP_400_BAD_REQUEST)

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
            return Response(data={'response': 'comment deleted'}, status=status.HTTP_201_CREATED)
        else:
            return Response(data={'error': 'comment unknow'}, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None, *args, **kwargs):
        comment = get_object_or_404(self.queryset, pk=pk)
        serializer = CommentsListSerializer(comment)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

from rest_framework.serializers import ModelSerializer
from .models import Projects, Contributors, Issues, Comments
from authentication.models import Users
from rest_framework import serializers


class UserSerializer(ModelSerializer):
    class Meta:
        model = Users
        fields = ['id', 'first_name', 'last_name', 'is_active', 'email']


class ProjectsListSerializer(ModelSerializer):
    author = UserSerializer(read_only=True)

    class Meta:
        model = Projects
        fields = ['id', 'title', 'type', 'description', 'author']


class ContributorsDetailSerializer(ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Contributors
        fields = ['project', 'role', 'permission', 'user']


class ProjectsDetailSerializer(ModelSerializer):
    author = UserSerializer(read_only=True)
    contributors = serializers.SerializerMethodField()

    class Meta:
        model = Projects
        fields = ['id', 'title', 'type', 'description', 'author', 'contributors']

    def get_contributors(self, request, instance):
        queryset = instance.contributors.all()
        serializer = ContributorsDetailSerializer(queryset, many=True)
        return serializer.data


class EmailSerializer(ModelSerializer):

    class Meta:
        model = Users
        fields = ['email']


class IssuesListSerializer(ModelSerializer):
    author = UserSerializer(read_only=True)
    project = ProjectsListSerializer(read_only=True)
    assignee = UserSerializer(read_only=True)

    class Meta:
        model = Issues
        fields = ['id', 'title', 'desc', 'tag', 'priority', 'status', 'assignee', 'author', 'project', 'created_time']


class CommentsListSerializer(ModelSerializer):
    author = UserSerializer(read_only=True)
    issue = IssuesListSerializer(read_only=True)

    class Meta:
        model = Comments
        fields = '__all__'

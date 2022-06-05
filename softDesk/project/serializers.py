from rest_framework.serializers import ModelSerializer
from .models import Projects, Contributors, Issues, Comments
from authentication.models import Users
from rest_framework import serializers


class UserSerializer(ModelSerializer):
    """
       Serialize the model Users
    """
    class Meta:
        model = Users
        fields = ['id', 'first_name', 'last_name', 'is_active', 'email']


class ProjectsListSerializer(ModelSerializer):
    """
       Serialize the model projects
    """
    author = UserSerializer(read_only=True)

    class Meta:
        model = Projects
        fields = ['id', 'title', 'type', 'description', 'author']


class ContributorsDetailSerializer(ModelSerializer):
    """
           Serialize the model Contributors
    """

    user = UserSerializer(read_only=True)

    class Meta:
        model = Contributors
        fields = ['project', 'role', 'permission', 'user']


class ProjectsDetailSerializer(ModelSerializer):
    """
           Serialize the model projects with all the fields
    """

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
    """
           Serialize the model Users with field email
    """

    class Meta:
        model = Users
        fields = ['email']


class IssuesListSerializer(ModelSerializer):
    """
           Serialize the model Issues with all the fields
    """
    author = UserSerializer(read_only=True)
    project = ProjectsListSerializer(read_only=True)
    assignee = UserSerializer(read_only=True)

    class Meta:
        model = Issues
        fields = ['id', 'title', 'desc', 'tag', 'priority', 'status', 'assignee', 'author', 'project', 'created_time']


class CommentsListSerializer(ModelSerializer):
    """
           Serialize the model Comments with all the fields
    """
    author = UserSerializer(read_only=True)
    issue = IssuesListSerializer(read_only=True)

    class Meta:
        model = Comments
        fields = '__all__'

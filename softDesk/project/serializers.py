from rest_framework.serializers import ModelSerializer, SerializerMethodField
from .models import Projects, Contributors, Issues, Comments
from authentication.models import Users

class UserSerializer(ModelSerializer):
    class Meta:
        model = Users
        fields = ['id', 'first_name', 'last_name', 'is_active', 'email']


class ProjectsListSerializer(ModelSerializer):
    author = UserSerializer(read_only=True)

    class Meta:
        model = Projects
        fields = ['id','title', 'type', 'description', 'author']



class ContributorsDetailSerializer(ModelSerializer):
    user = UserSerializer(read_only=True)


    class Meta:
        model = Contributors
        fields = ['project', 'role', 'permission', 'user']

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
        fields = ['id','title', 'desc', 'tag', 'priority', 'status', 'assignee', 'author', 'project', 'created_time' ]

    """def get_assignee(self, instance):
        queryset = Users.objects.all().filter(id=assignee)
        serializer = UserSerializer(queryset)
        return serializer.data"""

class CommentsListSerializer(ModelSerializer):
    author = UserSerializer(read_only=True)
    issue = IssuesListSerializer(read_only=True)

    class Meta:
        model = Comments
        fields = '__all__'
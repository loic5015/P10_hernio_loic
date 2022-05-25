"""softDesk URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from rest_framework import routers
from django.urls import path, include
from project.views import AdminProjectsViewset, UsersProjectlistViewset,\
    IssuesProjectlistViewset, CommentsProjectListViewset
from authentication.views import UsersCreateViewset, UsersListViewset
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_nested import routers


router = routers.SimpleRouter()
router.register('projects', AdminProjectsViewset, basename='admin-projects')
router.register('signup', UsersCreateViewset, basename='signup')
router.register('list', UsersListViewset, basename='list-users')

root_router = routers.NestedSimpleRouter(
    router,
    r'projects',
    lookup='project')
root_router.register(
    r'users',
    UsersProjectlistViewset,
    basename='users-project-list'
)
root_router.register(
    r'issues',
    IssuesProjectlistViewset,
    basename='issues-project-list'
)

issue_router = routers.NestedSimpleRouter(
    root_router,
    r'issues',
    lookup='issue')

issue_router.register(
    r'comments',
    CommentsProjectListViewset,
    basename='comments-project-list'
)


app_name = 'project'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
    path('', include(root_router.urls)),
    path('', include(issue_router.urls)),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh')
]

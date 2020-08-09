from django.conf.urls import url
from django.urls.conf import path
from registration.views import UserList, logout_view, UserDetail, UserMiniList, CandidateMiniList, \
    EmployerMiniList, Login

urlpatterns = [
    url(r'^api/users/$', view=UserList.as_view(), name='users'),
    url(r'^api/mini-users/$', view=UserMiniList.as_view(), name='mini-users'),
    url(r'^api/mini-candidates/$', view=CandidateMiniList.as_view(), name='mini-candidate'),
    url(r'^api/mini-employers/$', view=EmployerMiniList.as_view(), name='mini-employer'),
    path('api/users/<int:pk>/', view=UserDetail.as_view(), name='users_'),
    url(r'^api/login/', view=Login.as_view(), name='login'),
    url(r'^api/logout/', view=logout_view, name='logout'),
]

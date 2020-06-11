from django.conf.urls import url
from django.urls.conf import path

from joboffer.views import CompanyList

urlpatterns = [
    url(r'^api/companies/$', view=CompanyList.as_view(), name='company_list_create')
]

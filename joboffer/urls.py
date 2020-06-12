from django.conf.urls import url
from django.urls.conf import path

from joboffer.views import CompanyList, OfferList, ApplyList

urlpatterns = [
    url(r'^api/companies/$', view=CompanyList.as_view(), name='company_list_create'),
    url(r'^api/offers/$', view=OfferList.as_view(), name='offer_list_create'),
    url(r'^api/applies/$', view=ApplyList.as_view(), name='apply_list_create'),
]

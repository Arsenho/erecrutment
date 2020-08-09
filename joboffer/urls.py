from django.conf.urls import url
from django.urls.conf import path

from joboffer.views import CompanyList, OfferList, ApplyList, OfferCategoryList, OfferDetail, TestForOfferList

urlpatterns = [
    url(r'^api/companies/$', view=CompanyList.as_view(), name='company_list_create'),
    url(r'^api/offers/$', view=OfferList.as_view(), name='offer_list_create'),
    path('api/offers/<int:pk>', view=OfferDetail.as_view(), name='offer_update'),
    url(r'^api/offers-tests/$', view=TestForOfferList.as_view(), name='offers_tests'),
    url(r'^api/applies/$', view=ApplyList.as_view(), name='apply_list_create'),
    url(r'^api/offers/categories/$', view=OfferCategoryList.as_view(), name='offer_categories'),
]

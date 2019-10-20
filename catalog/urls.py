from django.urls import path, include
from .views import index, CompanyListView, CompanyDetailView, OwnerListView, OwnerDetailView, graph, ChartData, LoanedCompanysByUserListView, LoanedCompanysAllListView, renew_company_librarian, OwnerCreate, OwnerUpdate, OwnerDelete, CompanyCreate, CompanyUpdate, CompanyDelete


urlpatterns = [
    path('', index, name='index'),
    path('companys/', CompanyListView.as_view(), name='companys'),
    path('company/<int:pk>', CompanyDetailView.as_view(), name='company-detail'),
    path('owners/', OwnerListView.as_view(), name='owners'),
    path('owner/<int:pk>', OwnerDetailView.as_view(), name='owner-detail'),
    path('graph/', graph, name='graph'),
    path('catalog/graph/', ChartData.as_view(), name='catalog-graph'),
]


urlpatterns += [
    path('mycompanys/', LoanedCompanysByUserListView.as_view(), name='my-borrowed'),
    path('borrowed/', LoanedCompanysAllListView.as_view(), name='all-borrowed'),
]

urlpatterns += [
    path('company/<uuid:pk>/renew/', renew_company_librarian, name='renew-company-librarian'),
]


urlpatterns += [
    path('owner/create/', OwnerCreate.as_view(), name='owner_create'),
    path('owner/<int:pk>/update/', OwnerUpdate.as_view(), name='owner_update'),
    path('owner/<int:pk>/delete/', OwnerDelete.as_view(), name='owner_delete'),
]


urlpatterns += [
    path('company/create/', CompanyCreate.as_view(), name='company_create'),
    path('company/<int:pk>/update/', CompanyUpdate.as_view(), name='company_update'),
    path('company/<int:pk>/delete/', CompanyDelete.as_view(), name='company_delete'),
]


from django.contrib.staticfiles.urls import staticfiles_urlpatterns
urlpatterns += staticfiles_urlpatterns()

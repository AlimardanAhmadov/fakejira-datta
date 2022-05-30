from django.urls import path
from . import views


urlpatterns = [
    path('shippings/', views.main, name='fakejira_admin'),
    path('workflows/', views.workflows, name='workflows'),
    path('states/', views.states, name='states'),
    path('issue-tracking-flow/', views.all_issues, name='all_issues'),
    path('flow/<str:pk>/', views.shipping_flows, name='shipping_flows'),
    path('view-flow/<str:pk>/', views.view_flow, name='view_flow'),
    path('new-state/<str:pk>/', views.add_new_state, name='add_new_state'),
    path('manage-users/', views.manage_users, name='manage_users'),
    path('shippings/', views.shippings, name='shippings'),
    path('view_shipping/<str:pk>/', views.view_shipping, name='view_shipping'),
    path('create-shipping/', views.create_shipping, name='create_shipping'),
    path('add_new_shipping/', views.add_new_shipping, name='add_new_shipping'),
    path('update_shipping/<str:pk>/', views.update_shipping, name='update_shipping'),
    path('delete_shipping/<str:pk>/', views.delete_shipping, name='delete_shipping'),
    path('bulk_delete_shippings/', views.bulk_delete_shippings, name='bulk_delete_shippings'),
]
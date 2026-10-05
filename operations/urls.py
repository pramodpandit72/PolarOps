from django.urls import path
from . import views

app_name = 'operations'

urlpatterns = [
    # Dashboard
    path('dashboard/', views.dashboard_view, name='dashboard'),

    # Expeditions
    path('expeditions/', views.expedition_list, name='expedition_list'),
    path('expeditions/new/', views.expedition_create, name='expedition_create'),
    path('expeditions/<str:pk>/', views.expedition_detail, name='expedition_detail'),
    path('expeditions/<str:pk>/edit/', views.expedition_edit, name='expedition_edit'),
    path('expeditions/<str:pk>/delete/', views.expedition_delete, name='expedition_delete'),

    # Personnel
    path('personnel/', views.personnel_list, name='personnel_list'),
    path('personnel/new/', views.personnel_create, name='personnel_create'),
    path('personnel/<str:pk>/edit/', views.personnel_edit, name='personnel_edit'),
    path('personnel/<str:pk>/delete/', views.personnel_delete, name='personnel_delete'),

    # Assets
    path('assets/', views.asset_list, name='asset_list'),
    path('assets/new/', views.asset_create, name='asset_create'),
    path('assets/<str:pk>/', views.asset_detail, name='asset_detail'),
    path('assets/<str:pk>/edit/', views.asset_edit, name='asset_edit'),
    path('assets/<str:pk>/delete/', views.asset_delete, name='asset_delete'),

    # Supplies
    path('supplies/', views.supply_list, name='supply_list'),
    path('supplies/new/', views.supply_create, name='supply_create'),
    path('supplies/<str:pk>/edit/', views.supply_edit, name='supply_edit'),
    path('supplies/<str:pk>/delete/', views.supply_delete, name='supply_delete'),

    # Logistics
    path('logistics/', views.logistics_list, name='logistics_list'),
    path('logistics/new/', views.logistics_create, name='logistics_create'),
    path('logistics/<str:pk>/edit/', views.logistics_edit, name='logistics_edit'),
    path('logistics/<str:pk>/delete/', views.logistics_delete, name='logistics_delete'),

    # Maintenance
    path('maintenance/', views.maintenance_list, name='maintenance_list'),
    path('maintenance/new/', views.maintenance_create, name='maintenance_create'),
    path('maintenance/<str:pk>/edit/', views.maintenance_edit, name='maintenance_edit'),
    path('maintenance/<str:pk>/delete/', views.maintenance_delete, name='maintenance_delete'),

    # Tasks
    path('tasks/', views.task_list, name='task_list'),
    path('tasks/new/', views.task_create, name='task_create'),
    path('tasks/<str:pk>/edit/', views.task_edit, name='task_edit'),
    path('tasks/<str:pk>/toggle/', views.task_toggle_complete, name='task_toggle_complete'),
    path('tasks/<str:pk>/delete/', views.task_delete, name='task_delete'),

    # Locations
    path('locations/', views.location_list, name='location_list'),
    path('locations/new/', views.location_create, name='location_create'),
    path('locations/<str:pk>/', views.location_detail, name='location_detail'),
    path('locations/<str:pk>/edit/', views.location_edit, name='location_edit'),
    path('locations/<str:pk>/delete/', views.location_delete, name='location_delete'),
]

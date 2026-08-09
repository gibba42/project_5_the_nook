from django.urls import path

from . import views


urlpatterns = [
    path(
        'dashboard/',
        views.author_dashboard,
        name='author_dashboard'
    ),
    path(
        'profile/create/',
        views.create_author_profile,
        name='create_author_profile'
    ),
    path(
        'profile/edit/',
        views.edit_author_profile,
        name='edit_author_profile'
    ),
]
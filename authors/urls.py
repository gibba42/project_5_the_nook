from django.urls import path

from . import views


urlpatterns = [
    path(
        '',
        views.author_list,
        name='author_list'
    ),

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

    path(
        'selling/',
        views.selling_info,
        name='selling_info'
    ),

    path(
        'profile/image/delete/',
        views.delete_author_image,
        name='delete_author_image'
    ),
]

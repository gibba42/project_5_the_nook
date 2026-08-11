from django.urls import path

from . import views


urlpatterns = [
    path(
        '',
        views.book_list,
        name='book_list'
    ),

    path(
        'manage/create/',
        views.create_book,
        name='create_book'
    ),
    path(
        'manage/<int:book_id>/edit/',
        views.edit_book,
        name='edit_book'
    ),
    path(
        'manage/<int:book_id>/delete/',
        views.delete_book,
        name='delete_book'
    ),
    path(
        'manage/<int:book_id>/submit/',
        views.submit_book,
        name='submit_book'
    ),

    path(
        'manage/approvals/',
        views.approval_dashboard,
        name='approval_dashboard'
    ),
    path(
        'manage/approvals/<int:book_id>/',
        views.approval_detail,
        name='approval_detail'
    ),
    path(
        'manage/approvals/<int:book_id>/approve/',
        views.approve_book,
        name='approve_book'
    ),
    path(
        'manage/approvals/<int:book_id>/reject/',
        views.reject_book,
        name='reject_book'
    ),

    path(
        '<int:book_id>/',
        views.book_detail,
        name='book_detail'
    ),
]
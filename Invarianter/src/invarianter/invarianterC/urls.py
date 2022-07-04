from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('new/directory', views.DirectoryCreateView.as_view(), name='new directory'),
    path('new/file', views.FileCreateView.as_view(), name='new file'),
    path('delete', views.delete, name='delete'),
    path('recover', views.recoverFiles, name='recover'),
    path('delete/<str:name>', views.deleteCurrent, name='delete current'),
    path('uploads/<str:name>', views.getFile, name='file'),
    path('templates/invarinaterC/dirs', views.dirsView, name='dirs template'),
    path('templates/invarinaterC/delete_dirs', views.dirsViewDelete, name='dirs delete template'),
    path('success', views.success, name='success'),
    path('sections/<str:name>', views.getSections, name='sections'),
    path('<str:name>', views.fileInfo, name='file info'),
]

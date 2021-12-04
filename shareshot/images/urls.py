from django.urls import path
from . import views


app_name='images'
urlpatterns=[
    #image create view
    path('create/',views.image_create,name='create'),
    #image detail view
    path('detail/<int:id>/<slug:slug>/',views.image_detail,name='detail'),

    #like
    path('like/',views.image_like,name='like'),
    #homepage
    path('',views.image_list,name='list'),

    
]
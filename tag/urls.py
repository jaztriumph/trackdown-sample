from django.conf.urls import url
from . import views

# app_name = 'tag'
urlpatterns = [
    url(r'^$', views.log_in, name='log_in'),
    url(r'^form/', views.form, name='form'),
    url(r'^logout/$', views.log_out, name='log_out'),
    url(r'^tag-generator/$', views.tag_generator, name='tag_generator'),
    url(r'^image/', views.image, name='image'),
    url(r'^index/$',views.index,name='index')
]

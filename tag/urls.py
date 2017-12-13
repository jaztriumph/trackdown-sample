from django.conf.urls import url

from . import views

# app_name = 'tag'
urlpatterns = [
    url(r'^$', views.log_in, name='log_in'),
    url(r'^form/', views.form, name='form'),
    url(r'^logout/$', views.log_out, name='log_out'),
    url(r'^tag-generator/', views.tag_generator, name='tag_generator'),
    url(r'^image/', views.image, name='image'),
    url(r'^all-tags/', views.all_tags, name='all_tags'),
    url(r'^seen-tags/', views.seen_tags, name='seen_tags'),
    url(r'^mail-seen-tags/', views.mail_seen_tags, name='mail_seen_tags'),
    url(r'^instructions/$', views.instructions, name='instructions'),

]

from . import views
from django.conf.urls import url

urlpatterns = [
    url(r'^report/<uuid:report_id>/', views.report, name='report'),
    url(r'^submit-sim/', views.submit_sim, name='submit_sim'),
    url(r'^get_spells/', views.get_spells, name='get_spells'),
    url(r'^$', views.index, name='index'),
]

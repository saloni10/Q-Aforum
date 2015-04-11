from django.conf.urls import patterns, include, url
from django.conf import settings
from django.conf.urls.static import static

from QAforum import views

urlpatterns = patterns('',

	
	url(r'^question/', views.question),
	url(r'^home/', views.home,name='home' ),
	#url(r'^main/', views.main,name='main' ),
	#url(r'^qaform/', views.display,name='post' ),
	url(r'^register/', views.register,name='registration' ),
	url(r'^login/$', views.user_login, name='login'),
	url(r'^logout/$', views.user_logout, name='logout'),
	url(r'^profile/$', views.profile, name='profile'),
	url(r'^changepwd/$', views.changepwd, name='changepwdform'),
    url(r'^changepassword/$', views.changepassword),
    url(r'^update_profile/$', views.update_profile, name='update_profile'),
    url(r'^search/$', views.search_new, name='search'),
    url(r'^ansform/(?P<ques_id>\d+)/', views.writeans),
    url(r'^answer/(?P<ques_id>\d+)/', views.answer),
    url(r'^recent/$', views.recent_activity, name='recent_activity'),
    url(r'^delete_ques/(?P<ques_id>\d+)/', views.delete_ques),
	

	)
urlpatterns+=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

	

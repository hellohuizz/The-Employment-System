
from django.conf.urls import url


from webpro import views

urlpatterns = [
    url(r'^get_jobinfo/',views.get_jobinfo),
    url(r'^home_page',views.home_page,name='home_page'),
    url(r'^register',views.register,name='register'),
    url(r'^save_user',views.save_user,name='save_user'),
    url(r'^register_success',views.register_success,name='register_success'),
    url(r'^login_user',views.login_user,name='login_user'),
    url(r'^login_admin',views.login_admin,name='login_admin'),

]

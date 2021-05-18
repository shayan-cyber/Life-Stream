from django.urls import path, include
from . import views
urlpatterns = [

    path('', views.home, name="home"),
    path('full_details/<int:pk>', views.fullDetails,name='fulldetails'),
    path('profile/<int:pk>', views.profile, name='profile'),
    path('delupdt/<int:pk>', views.delupdt, name='delupdt'),
    path("sign_up", views.sign_up, name="sign_up"),
    path('login_donor_home', views.login_donor_home, name="login_donor_home"),
    path('login_donor_del', views.login_donor_del, name="login_donor_del"),
    path("add_updt", views.add_updt, name="add_updt"),
    path("chat/<str:userchat>", views.talkmain, name="talk"),
    path("donors_list", views.donors_list, name="donors_list"),
    path("log_out",views.log_out, name="log_out")

]
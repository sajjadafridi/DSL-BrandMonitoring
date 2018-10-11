from django.conf.urls import url, include
from django.contrib.auth import views as auth_views
from django.contrib import admin
from django.urls import path
from .import views as core_views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
urlpatterns = [
    url(r'^login/$', auth_views.login, {'template_name': 'SMM/login.html'}, name='login'),
    url(r'^home/$', core_views.home, name='home'),
    url(r'^dashboard1/$', core_views.insert_value, name='dashboard'),
    url(r'^influencers/$',core_views.influenser,name='influencers'),
    url(r'^profile_edit/$', core_views.update_profile, name='profile_edit'),
    url(r'^(?P<alert_id>[0-9]+)/$', core_views.display_feed, name='display_feed'),

    url(r'^(?P<sentiment>[0-9]+)/$', core_views.update_sentiment, name='update_sentiment'),

    # url( r'^login/$',auth_views.LoginView.as_view(template_name="SMM/login.html"), name="login"),
    url(r'^logout/$', auth_views.logout, {'next_page': 'login'}, name='logout'),
    url(r'^signup/$', core_views.signup, name='signup'),
    url(r'^forgetpassword/$', core_views.load_forgetpassword_page, name='forgetpassword'),
    url(r'^account_activation_sent/$', core_views.account_activation_sent, name='account_activation_sent'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        core_views.activate, name='activate'),
    url(r'^reset/$',auth_views.PasswordResetView.as_view(template_name='SMM/password_reset.html',email_template_name='SMM/password_reset_email.html',subject_template_name='SMM/password_reset_subject.txt'),name='password_reset'),
    url(r'^reset/done/$',auth_views.PasswordResetDoneView.as_view(template_name='SMM/password_reset_done.html'),name='password_reset_done'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',auth_views.PasswordResetConfirmView.as_view(template_name='SMM/password_reset_confirm.html'),name='password_reset_confirm'),
    url(r'^reset/complete/$',auth_views.PasswordResetCompleteView.as_view(template_name='SMM/password_reset_complete.html'), name='password_reset_complete'),
    url(r'', core_views.index, name='index'),

]

# urlpatterns += staticfiles_urlpatterns()
from django.conf.urls import url
from django.contrib.auth import views as auth_views

import SMM
from SMM import views
from .import views as core_views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import logout_then_login


urlpatterns = [
    url(r'^SMM/login/$', core_views.remember_me_login,
        name='remember_me_login'),
    # url(r'^SMM/login/$', core_views.login_user,
    #     {'template_name': 'SMM/login.html'}, name='login'),
    url(r'^SMM/redirect_login/$', core_views.redirect_login, name='redirect_login'),
    url(r'^SMM/new_alert/$', core_views.new_alert, name='new_alert'),
    url(r'^SMM/feeds/$', core_views.feeds, name='feeds'),
    url(r'^SMM/influencers/$', core_views.influencers, name='influencers'),
    url(r'^SMM/update_profile/$', core_views.update_profile, name='update_profile'),
    url(r'^account_delete/$', core_views.account_delete, name='account_delete'),
    url(r'^(?P<alert_id>[0-9]+)/$',
        core_views.display_feed, name='display_feed'),
    url(r'display_feed_angular/$', core_views.display_feed_angular,
        name='display_feed_angular'),
    url(r'update_sentiment/$', core_views.update_sentiment,
        name='update_sentiment'),
    url(r'^SMM/report/$', core_views.report, name='report'),
    url(r'get_user_keywords/$', core_views.get_user_keywords,
        name='get_user_keywords'),
    url(r'check_user_keyword/$', core_views.check_user_keyword,
        name='check_user_keyword'),
    url(r'display_feed_badge/$', core_views.display_feed_badge,
        name='display_feed_badge'),
    url(r'get_user_sentiment/$', core_views.get_user_sentiment,
        name='get_user_sentiment'),
    url(r'^SMM/logout/$', auth_views.logout,
        {'next_page': 'remember_me_login'}, name='logout'),
    url(r'^SMM/signup/$', core_views.signup, name='signup'),
    url(r'^account_activation_sent/$', core_views.account_activation_sent,
        name='account_activation_sent'),
    url(r'^SMM/account_reactivate/$', core_views.account_reactivation,
        name='account_reactivate'),
    url(r'^SMM/account_reactivation_sent/$', core_views.account_reactivation_sent,
        name='account_reactivation_sent'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        core_views.activate, name='activate'),
    url(r'^reset/$', auth_views.PasswordResetView.as_view(template_name='SMM/password_reset.html',
                                                          email_template_name='SMM/password_reset_email.html', subject_template_name='SMM/password_reset_subject.txt'), name='password_reset'),
    url(r'^reset/done/$', auth_views.PasswordResetDoneView.as_view(
        template_name='SMM/password_reset_done.html'), name='password_reset_done'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', auth_views.PasswordResetConfirmView.as_view(
        template_name='SMM/password_reset_confirm.html'), name='password_reset_confirm'),
    url(r'^reset/complete/$', auth_views.PasswordResetCompleteView.as_view(
        template_name='SMM/password_reset_complete.html'), name='password_reset_complete'),
    url(r'^SMM/$', core_views.index, name='index'),
    url(r'^$', core_views.index, name='index'),
]

# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL,
#                           document_root=settings.MEDIA_ROOT)
#     urlpatterns += static(settings.STATIC_URL,
#                           document_root=settings.STATIC_ROOT)
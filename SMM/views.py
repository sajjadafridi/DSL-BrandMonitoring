from functools import wraps

from django.contrib.auth import login, update_session_auth_hash
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import render, redirect, render_to_response
from django.urls import resolve
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.core.mail import EmailMessage, send_mail, BadHeaderError
from django.contrib.auth import views as auth_views
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth import REDIRECT_FIELD_NAME
from SMM.forms import AuthenticationRememberMeForm
from SMM.tasks import scheduling_script
from django.template import RequestContext, loader, Context
from BrandMonitoring import settings
from SMM.tokens import account_activation_token
from SMM.forms import SignUpForm, KeywordForm, ContactForm, UserProfileForm, UserEditForm, RemoveUser
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from SMM.models import Keyword, Post, PostUser, Profile
from .PostMessage import Message
from _datetime import datetime, timedelta
import asyncio
import time
from django.forms.utils import ErrorList
from django.contrib.auth import login as auth_login
from validate_email import validate_email
from SMM.TwintThread import TwintThread
import os
import json
from SMM.models import User as ModelUser

template_name = "feeds"
keyword = ' '

def load_forgetpassword_page(request):
    return render(request, 'SMM/password_reset.html')


def index(request):
    # handle the contact form
    if request.method == 'POST':
        contactform = ContactForm(data=request.POST)
        if contactform.is_valid():
            subject = contactform.cleaned_data['subject']
            from_email = contactform.cleaned_data['email_address']
            message = contactform.cleaned_data['message']
            try:
                send_mail(subject, message, from_email, [
                          'muhammad.sajjad@kics.edu.pk'])
                message = 'Your message has been send successfully!'
                messages.info(request, message)
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            return redirect('index')
        else:
            return render(request, "SMM/index.html", {'contact_form': contactform})
    else:
        contactform = ContactForm()
        return render(request, "SMM/index.html", {'contact_form': contactform})

def handler404(request,exception):
    return render(request, 'SMM/404.html',status=404)

def handler500(request):
    return render(request, 'SMM/500.html', status=500)

def redirect_login(request):
    if request.user.is_authenticated:
        if not check_existing_keyword(request):
            return redirect('new_alert')
        else:
            request.session['search_keyword'] = None
            redirect_view=request.session['view_name'];
            if redirect_view=='None':
                return redirect('feeds')
            else:
                return redirect(redirect_view)
    else:
        return redirect('remember_me_login')


@csrf_protect
@never_cache
def remember_me_login(request, template_name='SMM/login.html',
                      redirect_field_name=REDIRECT_FIELD_NAME,
                      authentication_form=AuthenticationRememberMeForm):

    redirect_to = request.POST.get(redirect_field_name, '')

    try:
        view_name = resolve(request.GET.get('next')).view_name
        request.session['view_name'] = view_name
    except:
        request.session['view_name'] = 'None'

    if request.method == "POST":
        form = authentication_form(data=request.POST)
        if form.is_valid():
            # Light security check -- make sure redirect_to isn't garbage.
            if not redirect_to or ' ' in redirect_to:
                redirect_to = settings.LOGIN_REDIRECT_URL

            # Heavier security check -- redirects to http://example.com should
            # not be allowed, but things like /view/?param=http://example.com
            # should be allowed. This regex checks if there is a '//' *before* a
            # question mark.
            elif '//' in redirect_to and re.match(r'[^\?]*//', redirect_to):
                redirect_to = settings.LOGIN_REDIRECT_URL

            if not form.cleaned_data.get('remember_me'):
                request.session.set_expiry(0)

            # Okay, security checks complete. Log the user in.
            auth_login(request, form.get_user())

            if request.session.test_cookie_worked():
                request.session.delete_test_cookie()

            return redirect(redirect_to)

        # elif 'activateAccountLink' in request.POST:
        #     username=request.POST.get('username_active')
        #     user=User.objects.filter(username=username)[0]
        #     subject = 'Social Media Brand Monitoring'
        #     message = render_to_string('SMM/account_activation_email.html', {
        #         'user': user,
        #         'domain': current_site.domain,
        #         'uid': urlsafe_base64_encode(force_bytes(user.pk)).decode(),
        #         'token': account_activation_token.make_token(user),
        #     })
        #     user.email_user(subject, message, user.email)
        #     return redirect('account_activation_sent')
        #
        # try:
        #     is_active = request.POST.get('is_active')
        #     user=User.objects.filter(form.cleaned_data.get('username'))
        # except:
        #     request.session['view_name'] = 'None'

    else:
        form = authentication_form(request)

    is_active=False;

    try:
        if form.cleaned_data.get('username') != None:
            is_active = not User.objects.filter(username=form.cleaned_data.get('username'))[0].is_active
    except:
        is_active=False

    request.session.set_test_cookie()

    current_site = get_current_site(request)

    return render(request, template_name, {
        'form': form,
        'is_active':is_active,
        redirect_field_name: redirect_to,
        'site': current_site,
        'site_name': current_site.name,
    })



@login_required
def new_alert(request):
    if request.user.is_authenticated:
        keyword = ''
        if request.user.is_authenticated:
            if request.method == "POST":
                keyword_form = KeywordForm(request.POST)
                # current user information
                user_id = request.POST.get('user_id')
                user_fname = request.POST.get('user_fist_name')
                user_lname = request.POST.get('user_last_name')
                user_email = request.POST.get('user_email')
                user_status = request.POST.get('user_status')
                user_econform = request.POST.get('user_email_conform')
                search_input = request.POST.get('search_keyword')
                keyword_input = request.POST.get('keyword_input')
                if(keyword_input == ''):
                    keyword = search_input
                else:
                    keyword = keyword_input

                request.session['search_keyword'] = keyword
                if keyword_form.is_valid():
                    keyword_form = KeywordForm()
                    model_instance = keyword_form.save(commit=False)
                    model_instance.alert_name = keyword
                    model_instance.User_id = user_id
                    model_instance.save()
                    return redirect(template_name)
                    # if check_user_keyword(request,keyword):
                    #     keyword_form = KeywordForm()
                    #     model_instance = keyword_form.save(commit=False)
                    #     model_instance.alert_name = keyword
                    #     model_instance.User_id = user_id
                    #     model_instance.save()
                    #     return redirect(template_name)
                    # else:
                    #     messages.error(request,'Keyword Already Present')
                    #     return render(request, "SMM/new_alert.html", {'form': keyword_form})
            else:
                keyword_form = KeywordForm()
                return render(request, "SMM/new_alert.html", {'form': keyword_form})
        else:
            return redirect('remember_me_login')
    else:
        return redirect('remember_me_login')


def check_email(email):
    if User.objects.filter(email=email).exists():
        return True
    else:
        return False

def validate_reg_email(email):
    is_valid = validate_email(email,verify=True)
    return is_valid

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            if check_email(form.cleaned_data.get('email')):
                errors = form._errors.setdefault("email", ErrorList())
                errors.append("Email already exists!")
                return render(request, 'SMM/signup.html', {'form': form})
            elif not validate_reg_email(form.cleaned_data.get('email')):
                errors = form._errors.setdefault("email", ErrorList())
                errors.append("Email is not valid!")
                return render(request, 'SMM/signup.html', {'form': form})
            else:
                user = form.save(commit=False)
                user.is_active = False
                user.save()
                current_site = get_current_site(request)
                subject = 'Social Media Brand Monitoring'
                message = render_to_string('SMM/account_activation_email.html', {
                    'user': user,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)).decode(),
                    'token': account_activation_token.make_token(user),
                })
                user.email_user(subject, message, user.email)
                return redirect('account_activation_sent')
        else:
            return render(request, 'SMM/signup.html', {'form': form})
    else:
        form = SignUpForm()
    return render(request, 'SMM/signup.html', {'form': form})


def account_activation_sent(request):
    return render(request, 'SMM/account_activation_sent.html')

def account_reactivation_sent(request):
    return render(request, 'SMM/account_reactivation_sent.html')

def account_reactivation(request):
    error="";
    errors=False;
    email="";
    if request.method == "POST":
        email=request.POST.get('reactivate_email')
        if not validate_reg_email(email):
            error="Not a valid email address!"
            errors = True
        elif not check_email(email):
            error="Email does not exists!"
            errors = True
        else:
            user=User.objects.filter(email=email)[0]
            if user.is_active:
                error="The user with this email address is already active!"
                errors = True
            else:
                subject = 'Social Media Brand Monitoring: User Account Reactivation'
                message = render_to_string('SMM/account_reactivation_email.html', {
                    'user': user,
                    'domain':get_current_site(request),
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)).decode(),
                    'token': account_activation_token.make_token(user),
                })
                user.email_user(subject, message, user.email)
                return redirect('account_reactivation_sent')

    return render(request, "SMM/account_reactivate.html", {
        'error':error,
        'errors':errors,
        'email':email
    })

def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.profile.email_confirmed = True
        user.save()
        login(request, user)
        return redirect('redirect_login')
    else:
        return render(request, 'SMM/account_activation_invalid.html')

@login_required
def feeds(request,  alert_keyword=None):

    kwd_to_search = ''
    if 'search_keyword' not in request.session:
        request.session['search_keyword'] = None

    kwd_to_search = request.session['search_keyword']
    request.session['search_keyword'] = None
    if not kwd_to_search == None:
        latest_keyword = Keyword.objects.order_by('-id')[:1]
        for kwd in latest_keyword:
            obj = TwintThread()
            obj.startThreadTwitterFeeds(kwd_to_search, kwd.id)
        time.sleep(3)
        keywords = {}
        posts = {}
        current_user = request.user
        Keyword_table = Keyword.objects.filter(User_id=current_user.id)
        for kwd in Keyword_table:
            keywords[kwd.id] = kwd.alert_name
        Posts = []
        list_of_data = {
            "post_data": Posts,
            "keyword_list": keywords
        }
        return render_to_response('SMM/feeds.html', list_of_data)
    return render(request, 'SMM/feeds.html')



@login_required
def get_search(request):
    if request.method == 'GET':
        keyword = request.GET.get('Search')
    error = ''
    if not keyword:
        error = "error message"
    return render(request, template_name, {'error': error})


@login_required
def influencers(request):
    selectedkwd = 0
    selectedtime = 'Time'
    if request.method == "GET":
        data = request.GET
        selectedkwd = data.get('selected_kwd')
        selectedtime = data.get('selected_time')
        print(data)

    if selectedkwd:
        selectedkwd = int(selectedkwd)
    if not selectedtime:
        selectedtime = 'Time'

    keywords = {}
    if selectedkwd and selectedtime:
        date_to_select = get_time(selectedtime)
        Posts = []
        post_table = Post.objects.select_related('PostUser').filter(
            Keyword_id=selectedkwd, CreatedAt__gte=date_to_select)
        print(len(post_table))
        for post in post_table:
            message = Message()
            message.set_ID(post.id)
            message.set_statusID(post.StatusID)
            message.set_Sentiment(post.Sentiment)
            message.set_Content(post.Content)
            message.set_CreatedAt(post.CreatedAt)
            message.set_ResharerCount(post.ResharerCount)
            message.set_DisplayName(post.PostUser.DisplayName)
            message.set_DisplayPicture(post.PostUser.DisplayPicture)
            message.set_UserID(post.PostUser.UserID)
            Posts.append(message)

    current_user = request.user
    Keyword_table = Keyword.objects.filter(User_id=current_user.id)
    for kwd in Keyword_table:
        keywords[kwd.id] = kwd.alert_name
    keywords = {
        "keyword_list": keywords,
        "set_keyword": selectedkwd,
        'set_time': selectedtime
    }
    return render_to_response('SMM/influencers.html', keywords)


@login_required
def update_profile(request):
    if request.user.is_authenticated:
        if request.method == 'POST' and 'profileupdatebtn' in request.POST:
            user_form = UserEditForm(instance=request.user, data=request.POST)
            profile_form = UserProfileForm(
                instance=request.user.profile, data=request.POST, files=request.FILES, )
            if profile_form.is_valid() and user_form.is_valid():
                profile_form.save(commit=False)
                profile_form.instance.full_name = request.user.first_name + \
                    " " + request.user.last_name
                # profile = Profile.objects.get(request.user.id)
                usr_profile = Profile.objects.get(user_id=request.user.id)
                profile = usr_profile.profile_image.file.name
                if usr_profile.profile_image.name != "default_profile_image.png" :
                    if os.path.exists(profile):
                        os.remove(profile)
                user_form.save()
                profile_form.save()
                messages.success(
                    request, 'Your profile is successfully updated!')
                return HttpResponseRedirect(request.path)
        elif request.method == 'POST' and 'updatepasswordbtn' in request.POST:
            change_password = PasswordChangeForm(
                data=request.POST, user=request.user)
            if change_password.is_valid():
                user = change_password.save()
                login(request, user,
                      backend='django.contrib.auth.backends.ModelBackend')
                update_session_auth_hash(request, user)
                messages.success(
                    request, 'Your password is successfully updated!')
                return redirect('index')
            else:
                user_form = UserEditForm(instance=request.user)
                profile_form = UserProfileForm(instance=request.user.profile)
                userdelform = RemoveUser()
                return render(request, 'SMM/update_profile.html',
                              {'user_form': user_form, 'profile_form': profile_form, 'change_password': change_password, 'removeuser_form': userdelform})
        elif request.method == 'POST' and 'deactivateconfirmbtn' in request.POST:
            user_record = User.objects.get(id=request.user.id)
            user_record.is_active=False
            user_record.save()
        elif request.method == 'POST' and 'deleteconfirmbtn' in request.POST:
            userdelform = RemoveUser(request.POST)
            if userdelform.is_valid():
                delete_account(request)
                return redirect('account_delete')
        else:
            change_password = PasswordChangeForm(user=request.user)
            user_form = UserEditForm(instance=request.user)
            profile_form = UserProfileForm(instance=request.user.profile)
            userdelform = RemoveUser(request.POST)

            return render(request, 'SMM/update_profile.html',
                          {'user_form': user_form, 'profile_form': profile_form, 'change_password': change_password, 'removeuser_form': userdelform})
        return redirect('remember_me_login')


@login_required
def load_profile(user):
    try:
        return user.profile
    except:  # this is not great, but trying to keep it simple
        profile = UserProfileForm.objects.create(user=user)
        return profile


@login_required
def update_sentiment(request):
    is_updated="False"
    try:
        Post.objects.filter(id=request.GET.get('post_id')).update(
        Sentiment=request.GET.get('sentiment'))
        is_updated="True"
    except:
        is_updated="False"

    return JsonResponse('{"is_updated":"'+is_updated+'"}', safe=False)


def temp(request, alert_id):

    return HttpResponse(alert_id)


@login_required
def display_feed_badge(request):
    keywords = []
    current_user = request.user
    Keyword_table = Keyword.objects.filter(
        User_id=current_user.id).order_by('-id')
    for kwd in Keyword_table:
        keyword = {}
        keyword['alert_id'] = kwd.id
        keyword['alert_name'] = kwd.alert_name
        keyword['alert_badge_count'] = Post.objects.select_related(
            'PostUser').filter(Keyword_id=kwd.id).count()
        keywords.append(json.dumps(keyword))
    return JsonResponse(keywords, safe=False)

@login_required
def display_feed_angular(request):
    keywords = {}
    Posts = []
    init = False
    current_user = request.user
    alert_id = request.GET.get("alert_id")
    if alert_id == "init":
        init = True

    no_of_feeds = request.GET.get("no_of_feeds")
    print(no_of_feeds)
    print(alert_id)
    Keyword_table = Keyword.objects.filter(User_id=current_user.id)
    for kwd in Keyword_table:
        keywords[kwd.id] = kwd.alert_name
        if(init):
            alert_id = kwd.id
    post_table = Post.objects.select_related(
        'PostUser').filter(Keyword_id=alert_id).order_by('-CreatedAt')
    print(post_table.count)
    if int(no_of_feeds) > post_table.count():
        no_of_feeds = post_table.count()
    else:
        post_table = post_table[:int(no_of_feeds)]

    jsonResult = []
    for post in post_table:
        message = Message()
        message.set_ID(post.id)
        message.set_statusID(post.StatusID)
        message.set_Sentiment(post.Sentiment)
        message.set_Content(post.Content)
        message.set_CreatedAt((str(post.CreatedAt)).split("+")[0])
        message.set_DisplayName(post.PostUser.DisplayName)
        message.set_DisplayPicture(post.PostUser.DisplayPicture)
        message.set_UserID(post.PostUser.UserID)
        message.set_EscapedContent(post.Content.replace(
            "'", "\'").replace('"', "&#34;"))
        jsonResult.append(message.toJSON())
        Posts.append(message)

    list_of_data = {
        "post_data": Posts,
        "keyword_list": keywords
    }
    return JsonResponse(jsonResult, safe=False)

@login_required
def display_feed(request, alert_id):
    keywords = {}
    Posts = []
    current_user = request.user
    Keyword_table = Keyword.objects.filter(User_id=current_user.id)
    for kwd in Keyword_table:
        keywords[kwd.id] = kwd.alert_name

    post_table = Post.objects.select_related(
        'PostUser').filter(Keyword_id=alert_id)
    for post in post_table:

        message = Message()
        message.set_ID(post.id)
        message.set_statusID(post.StatusID)
        message.set_Sentiment(post.Sentiment)
        message.set_Content(post.Content)
        message.set_CreatedAt(post.CreatedAt)
        message.set_DisplayName(post.PostUser.DisplayName)
        message.set_DisplayPicture(post.PostUser.DisplayPicture)
        message.set_UserID(post.PostUser.UserID)
        message.set_EscapedContent(post.Content.replace(
            "'", "\\'").replace('"', "&quot;"))
        Posts.append(message)

    list_of_data = {
        "post_data": Posts,
        "keyword_list": keywords
    }
    return render_to_response('SMM/feeds.html', list_of_data)


def get_time(time_string):
    dates = 0
    if time_string == "Today":
        dates = datetime.now()
        return dates.date()
    elif time_string == "Yesterday":
        dates = datetime.now() - timedelta(days=1)
        return dates.date()
    elif time_string == "7 days":
        dates = datetime.now() - timedelta(days=6)
        return dates.date()
    elif time_string == "Last Week":
        dates = datetime.now() - timedelta(days=13)
        return dates.date()
    elif time_string == "Last 30 Days":
        dates = datetime.now() - timedelta(days=29)
        return dates.date()
    elif time_string == "Last Month":
        dates = datetime.now() - timedelta(days=59)
        return dates.date()

@login_required
def check_existing_keyword(user_request):
    user_id = user_request.user.id
    keyword_count = Keyword.objects.filter(User_id=user_id).count()
    if keyword_count > 0:
        return True
    else:
        return False

@login_required
def check_user_keyword(request):
    keyword = request.GET.get('keyword')
    keyword_count = Keyword.objects.filter(
        User_id=request.user.id, alert_name=keyword).count()
    if keyword_count > 0:
        return JsonResponse('{"Exists":"Yes"}', safe=False)
    return JsonResponse('{"Exists":"No"}', safe=False)

@login_required
def get_user_keywords(request):
    user_keywords = Keyword.objects.filter(
        User_id=request.user.id)
    keywords = []
    for kwd in user_keywords:
        keywords.append(kwd.alert_name.lower())
    return JsonResponse(keywords, safe=False)

@login_required
def delete_account(user_request):
    user_id = user_request.user.id
    keyword_list = list(Keyword.objects.filter(User_id=user_id))
    for key in keyword_list:
        posts = list(Post.objects.filter(Keyword_id=key.id))
        postuser_id = [post for post in posts]
        for posts in postuser_id:
            PostUser.objects.filter(id=posts.id).delete()
        Post.objects.filter(Keyword_id=key.id).delete()
    Keyword.objects.filter(User_id=user_id).delete()
    profile = Profile.objects.get(user_id=user_request.user.id)
    if profile.profile_image.name != "profile_image/default_profile_image.png":
        if os.path.exists(profile.profile_image.file.name):
            os.remove(profile.profile_image.file.name)
    User.objects.get(id=user_id).delete()


def account_delete(request):
    return render(request, 'SMM/account_delete.html')

@login_required
def report(request):
    user_id = request.user.id
    keywords = list(Keyword.objects.filter(User_id=user_id).order_by('-id'))
    return render_to_response('SMM/report.html', {'keyword_list': keywords})

@login_required
def get_user_sentiment(request):
    keyword = request.GET.get('alert_name')
    keyword_id = Keyword.objects.filter(
        User_id=request.user.id, alert_name=keyword).values_list('id', flat=True)
    positive_count = Post.objects.filter(Keyword_id=keyword_id[0], Sentiment=1).count()
    negative_count = Post.objects.filter(
        Keyword_id=keyword_id[0], Sentiment=-1).count()
    neutral_count = Post.objects.filter(
        Keyword_id=keyword_id[0], Sentiment=0).count()

    post_sentiment_counts = {'positive':positive_count,'negative':negative_count,'neutral':neutral_count}
    return JsonResponse(post_sentiment_counts, safe=False)

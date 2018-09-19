from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import render, redirect
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from SMM.forms import SignUpForm
from SMM.forms import KeywordForm
from SETMOK_API.SETMOKE_API import SETMOKE_API
from SMM.tokens import account_activation_token
from django.shortcuts import render_to_response
template_name = "dashboard"
Search_keyword = ''

def load_forgetpassword_page(request):
    return render(request,'SMM/forgetpassword.html')


@login_required
def home(request):
    if request.user.is_authenticated:
        print("authentic user")
        if request.method == "POST":
            keyword_form = KeywordForm(request.POST)

            # current user information

            user_id = request.POST.get('user_id')
            user_fname=request.POST.get('user_fist_name')
            user_lname=request.POST.get('user_last_name')
            user_email=request.POST.get('user_email')
            user_status=request.POST.get('user_status')
            user_econform=request.POST.get('user_email_conform')
            global Search_keyword
            Search_keyword=request.POST.get('search_keyword')

            # create or get the user_id already exist
            # user, _ = User.objects.get_or_create(Userid=request.POST.get('user_id'))

# updating the current form and then post
            # updated_request = request.POST.copy()
            # updated_request.update({'alert_name': key_word})
            # updated_request.update({'Userid_id': user_id})
            # keyword_form= KeywordForm(data=updated_request)
            if keyword_form.is_valid():
                keyword_form = KeywordForm()
                model_instance = keyword_form.save(commit=False)
                model_instance.alert_name = Search_keyword
                model_instance.Userid_id = user_id
                model_instance.save()
                return redirect('dashboard')
        else:
            keyword_form = KeywordForm()
            return render(request, "SMM/home.html", {'form': keyword_form})
    else:
        return render(request, 'SMM/home.html',{})


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()

            current_site = get_current_site(request)
            subject = 'Activate Your MySite Account'
            message = render_to_string('SMM/account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)).decode(),
                'token': account_activation_token.make_token(user),
            })
            user.email_user(subject, message,user.email)
            mail_subject = 'Activate your SMM account.'
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(mail_subject, message, to=[to_email])
            email.send()
            return redirect('account_activation_sent')
    else:
        form = SignUpForm()
    return render(request, 'SMM/signup.html', {'form': form})


def account_activation_sent(request):
    return render(request, 'SMM/account_activation_sent.html')


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
        return redirect('home')
    else:
        return render(request, 'SMM/account_activation_invalid.html')


def fetch_posts(keyword_to_search):
    setmoke_api = SETMOKE_API(keyword_to_search, "/home/rehab/PycharmProjects/conf/config.ini")
    list = setmoke_api.get_data()
    setmoke_api.add_to_database(list, 'localhost', 'root', 'rehab105', 'SMM_DB3')
    list_of_data = {
        "list_of_data": list
    }
    return list_of_data


def insert_value(request):
    if request.method == "POST":
        print("I am here django")


    form = KeywordForm(request.POST)
    # if form.is_valid():

    # setmoke_api.add_to_database(list, 'localhost', 'root', 'rehab105', 'SMM_DB3')
    # post = form.save(commit=False)
    # post.author = request.user
    # post.published_date = timezone.now()
    # post.save()
    print(Search_keyword)
    return render_to_response('SMM/dashboard1.html', fetch_posts(Search_keyword))
    # return render(request, 'SMM/dashboard1.html',)

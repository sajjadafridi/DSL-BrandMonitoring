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
keyword = ''

def load_forgetpassword_page(request):
    return render(request,'SMM/forgetpassword.html')


@login_required
def home(request):
    return render(request, 'SMM/home.html')


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


def insert_value(request):
    if request.method == "POST":
        print("I am here django")

        form = KeywordForm(request.POST)
        # if form.is_valid():
        keyword_to_search = 'Imran Khan'
            #  keyword_to_search="Nawaz Sharif"
        setmoke_api = SETMOKE_API(keyword_to_search, "/home/rehab/PycharmProjects/conf/config.ini",3)
        list = setmoke_api.get_data()
        # setmoke_api.add_to_database(list, 'localhost', 'root', 'rehab105', 'SMM_DB3')
            # post = form.save(commit=False)
            # post.author = request.user
            # post.published_date = timezone.now()
            # post.save()
        list_of_data = {
            "list_of_data": list
        }
        return render_to_response('SMM/dashboard1.html', list_of_data)
    #        return render(request, 'SMM/dashboard1.html', {'form': form})
    #
    # else:
    #     form = KeywordForm()
    #     return render(request, 'SMM/dashboard1.html', {'form': form})

         # return render(request, 'blog/post_edit.html', {'form': form})
        # if form.is_valid():
        #     alert_name = request.POST['alert_name']
        #     form.optional_keywords = request.POST.get('fourth', '')
        #     form.required_keywords = request.POST.get('fourth', '')
        #     form.excluded_keywords = request.POST.get('fourth', '')


# def get_search(request):
#     if request.method == 'GET':
#         keyword = request.GET.get('Search')
#     error = ''
#     if not keyword:
#         error = "error message"
#     return render(request, template_name, {'error': error})

# def keyword_module(request):
#     if request.method == 'GET':
#         form = keyword_module(request.GET)
#         if form.is_valid():
#             keyword = request.GET.get('ajax-input')
#             return render(request, 'SMM/dashboard.html', {'form': form})

    # rendered = render_to_string('my_template.html', {'foo': 'bar'})
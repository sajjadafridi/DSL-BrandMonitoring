from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import render, redirect, render_to_response
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.http import HttpResponse, HttpResponseRedirect
from django.core.mail import EmailMessage,send_mail, BadHeaderError
from SMM.tokens import account_activation_token
from SMM.forms import SignUpForm,KeywordForm,ContactForm,UserProfileForm,UserEditForm
from SETMOK_API.SETMOKE_API import SETMOKE_API
from django.contrib import messages
from Analysis.SentimentAnalysis import SentimentAnalysis
from SMM.Sentiment import Sentiment
from SMM.models import Keyword, Post, PostUser
from .PostMessage import Message
template_name = "dashboard"
keyword = ''

def load_forgetpassword_page(request):
    return render(request,'SMM/forgetpassword.html')


def index(request):
    # handle the contact form
    if request.method == 'GET':
        contactform = ContactForm()
    else:
        contactform = ContactForm(data=request.POST)
        if contactform.is_valid():
            subject = contactform.cleaned_data['subject']
            from_email = contactform.cleaned_data['email_address']
            message = contactform.cleaned_data['message']
            try:
                send_mail(subject, message, from_email, ['muhammad.sajjad@kics.edu.pk'])
                message = 'Your message has been send successfully!'
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            messages.info(request, message)
        else:
            return render(request, "SMM/index.html", {'contact_form': contactform})
    return render(request, "SMM/index.html", {'contact_form': contactform})

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

            key_word=request.POST.get('search_keyword')

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
                model_instance.alert_name = key_word
                model_instance.User_id = user_id
                model_instance.save()
                return redirect('dashboard')
        else:
            keyword_form = KeywordForm()
            return render(request, "SMM/home.html", {'form': keyword_form})
    else:
        return redirect('login')


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
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
            user.email_user(subject, message,user.email)
            mail_subject = subject
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
    setmoke_api = SETMOKE_API(keyword_to_search, "D:/config.ini")
    list = setmoke_api.get_data()
    setmoke_api.add_to_database(list, 'localhost', 'root', 'sajjadafridi', 'SMM_DB')
    setmoke_api.add_to_database(list, 'localhost', 'root', 'rehab105', 'SMM_DB')
    list_of_data = {
        "list_of_data": list
    }
    return list_of_data


def insert_value(request,alert_keyword=None):
    keywords = {}
    current_user = request.user
    Keyword_table=Keyword.objects.filter(User_id=current_user.id)
    for kwd in Keyword_table:
        keywords[kwd.id] = kwd.alert_name


    if request.method == "POST":
        print("I am here django")



    form = KeywordForm(request.POST)
    # if form.is_valid():'
    # return_5.delay()

    keyword_to_search = 'Imran'
    #  keyword_to_search="Nawaz Sharif"
    # setmoke_api = SETMOKE_API(keyword_to_search, "D:/config.ini")
    # list = setmoke_api.get_data()
    # setmoke_api.add_to_database(list, 'localhost', 'root', 'rehab105', 'SMM_DB3')
    setmoke_api = SETMOKE_API(keyword_to_search, "/home/rehab/PycharmProjects/conf/config.ini", 2, source="googlePlus")
    list = setmoke_api.get_data()

    sent_list=[]
    analysis=SentimentAnalysis()

    for mention in list:
        sentiment = Sentiment()

        sentiment.set_list(mention)
        sent=analysis.analysis(mention.get_text(), "NLTK",
                          "/home/rehab/PycharmProjects/PYPI package/SentimentAnalysis/my_classifier.pickle")

        if sent=='Negative':
            sentiment.set_sentiment(0)
        else:
            sentiment.set_sentiment(1)
        sent_list.append(sentiment)

    # setmoke_api.add_to_database(sent_list, 'localhost', 'root', 'rehab105', 'SMM_DB', current_user.id)
    # post = form.save(commit=False)
    # post.author = request.user
    # post.published_date = timezone.now()
    # post.save()
    Posts=[]
    list_of_data = {
        "post_data": Posts,
        "keyword_list": keywords
    }
    return render_to_response('SMM/dashboard1.html', list_of_data)
    # return render(request, 'SMM/dashboard1.html',)


def get_search(request):
    if request.method == 'GET':
        keyword = request.GET.get('Search')
    error = ''
    if not keyword:
        error = "error message"
    return render(request, template_name, {'error': error})

def influenser(request):
    return render(request, 'SMM/influencers.html')

def update_profile(request):
    profile = load_profile(request.user)
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user,data=request.POST,)
        profile_form = UserProfileForm(instance=profile,data=request.POST,files=request.FILES,)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()

    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = UserProfileForm(instance=profile)

    return render(request,'SMM/profile_edit.html',{'user_form': user_form,'profile_form':profile_form })

def load_profile(user):
  try:
    return user.profile
  except:  # this is not great, but trying to keep it simple
    profile = UserProfileForm.objects.create(user=user)
    return profile

def update_sentiment(request, sentiment):
    print(sentiment)
    return HttpResponse("Succeefully updated")


def display_feed(request, alert_id):
    keywords = {}
    current_user = request.user
    Keyword_table = Keyword.objects.filter(User_id=current_user.id)
    for kwd in Keyword_table:
        keywords[kwd.id] = kwd.alert_name
    Posts=[]
    PostUsers=[]
    post_table= Post.objects.select_related('PostUser').filter(Keyword_id=alert_id)
    # post_table=Post.objects.filter(Keyword_id=alert_id)
    for post in post_table:
        message=Message()
        message.set_ID(post.id)
        message.set_statusID(post.StatusID)
        message.set_Sentiment(post.Sentiment)
        message.set_Content(post.Content)
        message.set_CreatedAt(post.CreatedAt)
        message.set_ResharerCount(post.ResharerCount)
        message.set_Source(post.Source)
        message.set_DisplayName(post.PostUser.DisplayName)
        message.set_DisplayPicture(post.PostUser.DisplayPicture)
        message.set_UserID( post.PostUser.UserID)


        Posts.append(message)

    list_of_data = {
        "post_data": Posts,
        "keyword_list": keywords
    }
    return render_to_response('SMM/dashboard1.html', list_of_data)

class PostInfo:
    def __init__(self, post, post_user):
        self.post=post
        self.post_user=post_user
    def get_post(self):
        return self.post
    def get_post_user(self):
        return self.post_user
    def set_post(self,post):
        self.post=post
    def set_post_user(self, post_user):
        self.post_user=post_user
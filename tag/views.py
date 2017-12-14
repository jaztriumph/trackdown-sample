# import simplejson as json
import os
import uuid

from PIL import Image
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.utils import timezone
from django.views.decorators.cache import cache_page
from google.auth.transport import requests
from google.oauth2 import id_token
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import User1, UserInfo, ClientInfo
from .serializers import UserInfoSerializer

# import string

CLIENT_ID = os.environ["CLIENT_ID"]

BASE_TAG_URL = "https://trackdown.herokuapp.com/image?image_tag="


# tag_link = ""
# user_tag = ""


class UserInfoApi(APIView):
    @staticmethod
    def get(request):
        email = request.GET.get('email')
        # user = authenticate(email=email, password="password")
        print(email)
        try:
            user_info = UserInfo.objects.filter(user=request.user)
        except Exception:
            raise Http404("does")
        serializer = UserInfoSerializer(user_info, many=True)
        return Response(serializer.data)


def log_in(request):
    # global user_tag
    # global tag_link
    # tag_link = ""
    # user_tag = ""
    # times = os.environ['tick']
    # print (times)
    # print request.get_full_path()
    token = request.GET.get('token')
    if (request.method == "GET") & (token is not None):
        # token = request.GET.get('token')
        # print(token)
        try:
            idinfo = id_token.verify_oauth2_token(token, requests.Request(), CLIENT_ID)
            # print("iss")
            # print(idinfo['iss'])
            # Or, if multiple clients access the backend server:
            # idinfo = id_token.verify_oauth2_token(token, requests.Request())
            # if idinfo['aud'] not in [CLIENT_ID_1, CLIENT_ID_2, CLIENT_ID_3]:
            #     raise ValueError('Could not verify audience.')

            if idinfo['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
                raise ValueError('Wrong issuer.')

            # If auth request is from a G Suite domain:
            # if idinfo['hd'] != GSUITE_DOMAIN_NAME:
            #     raise ValueError('Wrong hosted domain.')

            # ID token is valid. Get the user's Google Account ID from the decoded token.
            userid = idinfo['sub']

        except ValueError:
            print ("error")
            return redirect('tag:log_in')
            # Invalid token

        # response = requests.get('https://www.googleapis.com/oauth2/v3/tokeninfo?id_token=' + token)
        # data = json.loads(response.content)

        print(idinfo["email"])
        user = authenticate(email=idinfo["email"], password="cameocomuf")
        if user is not None:
            user.first_name = idinfo["given_name"]
            user.last_name = idinfo["family_name"]
            user.picture_url = idinfo["picture"]
            user.save()
            login(request, user)
        else:
            user = User1.objects.create_user(idinfo["email"], "cameocomuf")
            user.first_name = idinfo["given_name"]
            user.last_name = idinfo["family_name"]
            user.picture_url = idinfo["picture"]
            user.save()
            user = authenticate(email=idinfo["email"], password="cameocomuf")
            login(request, user)
        return redirect('tag:tag_generator')

    if not request.user.is_authenticated():
        return render(request, 'login.html')
    # user = request.user
    # context = {'name': user.first_name, 'picture': user.picture_url}
    request.session['user_tag'] = ""
    request.session['tag_link'] = ""
    return redirect('tag:tag_generator')


def log_out(request):
    # print request.get_full_path()
    # global user_tag
    # global tag_link
    # tag_link = ""
    # user_tag = ""
    logout(request)
    return redirect('tag:log_in')


@login_required
def form(request):
    # global user_tag
    user_tag = request.GET.get('tagname')
    print(user_tag)
    if (request.method == "GET") & (user_tag is not None):
        generated_tag = str(uuid.uuid4())
        # global tag_link
        # tag_link = generated_tag
        request.session['user_tag'] = user_tag
        request.session['tag_link'] = generated_tag
        now = timezone.now().strftime('%H:%M:%S')
        print (now)
        userinfo = UserInfo()
        userinfo.user = request.user
        userinfo.user_tag = user_tag.strip()
        userinfo.generated_tag = generated_tag
        userinfo.time = timezone.now()
        userinfo.save()
    return redirect('tag:tag_generator')


@login_required
def tag_generator(request):
    now = timezone.now().strftime("Time:  %H:%M:%S, Day:  %d:%b:%y")
    print (now)
    user = request.user
    print(user.first_name)
    context = {'name': user.first_name, 'picture': user.picture_url, 'email_id': user.email, }
    # userIn = UserInfo.objects.filter(user=request.user)
    # if len(userIn) > 0:
    #     tag = userIn[len(userIn) - 1]
    #     link = BASE_TAG_URL + tag.generated_tag
    # else:
    #     link = ""
    user_tag = request.session.get('user_tag')
    tag_link = request.session.get('tag_link')
    if (tag_link != "") & (tag_link is not None):
        link = BASE_TAG_URL + tag_link
    else:
        link = ""
    context.update({'generated_tag': link, 'prev_tag': user_tag})

    return render(request, 'tag.html', context)


def trim(agent):
    agent = agent.split('/')
    last = agent[2].strip()
    last = last.split(' ')[0]
    agent[2] = last
    agent = "/".join(agent)
    print agent
    return agent


def useful_meta(meta):
    list_keys = ['LOGNAME', 'USER', 'HTTP_USER_AGENT', 'HTTP_HOST', 'SERVER_NAME', 'REMOTE_HOST', 'REMOTE_USER',
                 'SERVER_PORT', 'HTTP_X_FORWARDED_FOR', 'REMOTE_ADDR']
    data = {}
    for key in list_keys:
        try:
            data.update({key: meta[key]})
        except Exception:
            pass
    print(data)
    return data


@cache_page(0)
def image(request):
    print(request.user_agent)
    tag = request.GET.get('image_tag')
    user_info = UserInfo.objects.filter(generated_tag=tag)
    print request.META
    print(user_info)
    if len(user_info) > 0:
        current_user_agent = trim(request.user_agent.__str__())
        current_IP = request.META['HTTP_X_FORWARDED_FOR']
        client_info = user_info[0].client_info.filter(client_agent=current_user_agent).filter(
            client_meta__REMOTE_ADDR=current_IP)

        if len(client_info) == 0:
            client = ClientInfo()
            client.user_info = user_info[0]
            client.client_agent = trim(request.user_agent.__str__())
            client.times_seen = 1
        else:
            client = client_info[0]
            client.times_seen += 1

        client.time = timezone.now()
        client.client_meta = useful_meta(request.META)
        client.save()
        img = Image.new("RGB", (10, 10), "#faebd7")
        # serialize to HTTP response
        response = HttpResponse(content_type="image/png")
        img.save(response, "PNG")
        return response
    raise Http404


@login_required
def all_tags(request):
    user = request.user
    user_info = UserInfo.objects.filter(user=user)
    context = {'name': user.first_name, 'picture': user.picture_url, 'email_id': user.email, }
    context.update({'user_info': user_info, 'BASE_TAG_URL': BASE_TAG_URL})
    return render(request, "allTags.html", context)


@login_required
def seen_tags(request):
    user = request.user
    clients = ClientInfo.objects.filter(user_info__user=user)
    newlist = sorted(clients, key=lambda k: k.client_time, reverse=True)
    context = {'name': user.first_name, 'picture': user.picture_url, 'email_id': user.email, }
    context.update({'client_info': newlist, 'BASE_TAG_URL': BASE_TAG_URL})
    return render(request, "seenTags.html", context)


def check_for_mail_proxy(agent):
    agent = agent.split('/')
    if agent[2] == 'GmailImageProxy':
        return True
    return False


@login_required
def mail_seen_tags(request):
    user = request.user
    # clients = ClientInfo.objects.filter(user_info__user=user)
    user_info = UserInfo.objects.filter(user=user)
    clients = []
    for info in user_info:
        times = 0
        client_info = ClientInfo.objects.filter(user_info=info)
        for client in client_info:
            if check_for_mail_proxy(client.client_agent):
                times += client.times_seen
            if times > 2:
                clients.append(client)
                break
    context = {'name': user.first_name, 'picture': user.picture_url, 'email_id': user.email, }
    context.update({'client_info': clients, 'BASE_TAG_URL': BASE_TAG_URL})
    return render(request, "gmailtracked.html", context)


@login_required
def instructions(request):
    user = request.user
    context = {'name': user.first_name, 'picture': user.picture_url, 'email_id': user.email, }
    return render(request, "instructions.html", context)

# import google as google
from PIL import Image, ImageDraw, ImageOps
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import redirect, render
# from django.urls import reverse
from django.views.decorators.cache import cache_page
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.csrf import ensure_csrf_cookie
from google.auth.transport import requests
from google.oauth2 import id_token
import uuid
from .models import User1, UserInfo, ClientInfo
import datetime
from django.utils import timezone

# import string
# from rest_framework import serializers

CLIENT_ID = '642931691711-njc9uv4lt3lhnnqeh6bq26crdacqpt29.apps.googleusercontent.com'

BASE_TAG_URL = "https://trackdown.herokuapp.com/image?image_tag="
tag_link = ""


def log_in(request):
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
        user = authenticate(email=idinfo["email"], password="password")
        if user is not None:
            user.first_name = idinfo["given_name"]
            user.last_name = idinfo["family_name"]
            user.picture_url = idinfo["picture"]
            user.save()
            login(request, user)
        else:
            user = User1.objects.create_user(idinfo["email"], "password")
            user.first_name = idinfo["given_name"]
            user.last_name = idinfo["family_name"]
            user.picture_url = idinfo["picture"]
            user.save()
            user = authenticate(email=idinfo["email"], password="password")
            login(request, user)
        return redirect('tag:form')

    if not request.user.is_authenticated():
        return render(request, 'login.html')
    # user = request.user
    # context = {'name': user.first_name, 'picture': user.picture_url}
    return redirect('tag:tag_generator')


def log_out(request):
    # print request.get_full_path()
    logout(request)
    return redirect('tag:log_in')


@login_required
def form(request):
    user_tag = request.GET.get('tagname')
    print(user_tag)
    if (request.method == "GET") & (user_tag is not None):
        generated_tag = str(uuid.uuid4())
        global tag_link
        tag_link = generated_tag
        now = timezone.now().strftime('%H:%M:%S')
        print (now)
        # link = BASE_TAG_URL + generated_tag
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
    context = {'name': user.first_name, 'picture': user.picture_url}
    # userIn = UserInfo.objects.filter(user=request.user)
    # if len(userIn) > 0:
    #     tag = userIn[len(userIn) - 1]
    #     link = BASE_TAG_URL + tag.generated_tag
    # else:
    #     link = ""
    if tag_link != "":
        link = BASE_TAG_URL + tag_link
    else:
        link = ""
    context.update({'generated_tag': link})

    return render(request, 'tag.html', context)


# Create your views here.
# @ensure_csrf_cookie
# @csrf_exempt
# def tags(request):
#     token = request.GET.get('token')
#     # print(token)
#     try:
#         idinfo = id_token.verify_oauth2_token(token, google.auth.transport.requests.Request(), CLIENT_ID)
#         # print("iss")
#         # print(idinfo['iss'])
#         # Or, if multiple clients access the backend server:
#         # idinfo = id_token.verify_oauth2_token(token, requests.Request())
#         # if idinfo['aud'] not in [CLIENT_ID_1, CLIENT_ID_2, CLIENT_ID_3]:
#         #     raise ValueError('Could not verify audience.')
#
#         if idinfo['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
#             raise ValueError('Wrong issuer.')
#
#         # If auth request is from a G Suite domain:
#         # if idinfo['hd'] != GSUITE_DOMAIN_NAME:
#         #     raise ValueError('Wrong hosted domain.')
#
#         # ID token is valid. Get the user's Google Account ID from the decoded token.
#         userid = idinfo['sub']
#
#     except ValueError:
#         # Invalid token
#         return redirect('tag:log_in')
#     response = requests.get('https://www.googleapis.com/oauth2/v3/tokeninfo?id_token=' + token)
#     data = json.loads(response.content)
#     print(data["email"])
#     user = authenticate(email=data["email"], password="password")
#     if user is not None:
#         login(request, user)
#     else:
#         user = User1.objects.create_user(data["email"], "password")
#         user.save()
#         user = authenticate(email=data["email"], password="password")
#         login(request, user)
#     return redirect('tag:form')


@cache_page(0)
def image(request):
    print(request.user_agent)
    tag = request.GET.get('image_tag')
    user_info = UserInfo.objects.filter(generated_tag=tag)
    print(user_info)
    if len(user_info) > 0:
        client_info = ClientInfo()
        client_info.user_info = user_info[0]
        client_info.time = timezone.now()
        # meta = tuple(request.META)
        # print meta
        print(type(request.META))
        # client_info.client_meta = request.META
        client_info.client_agent = request.user_agent.__str__()
        client_info.save()
    img = Image.new("RGB", (10, 10), "#faebd7")
    # serialize to HTTP response
    response = HttpResponse(content_type="image/png")
    img.save(response, "PNG")
    return response


@login_required
def all_tags(request):
    user = request.user
    user_info = UserInfo.objects.filter(user=user)
    context = {'name': user.first_name, 'picture': user.picture_url}
    context.update({'user_info': reversed(user_info), 'BASE_TAG_URL': BASE_TAG_URL})
    return render(request, "allTags.html", context)


@login_required
def seen_tags(request):
    user = request.user
    user_info = UserInfo.objects.filter(user=user)
    clients = []
    for info in user_info:
        client_info = ClientInfo.objects.filter(user_info=info)
        if len(client_info) > 2:
            count = 0
            index = 0
            for client in client_info:
                if client.client_agent.split('/')[0].strip() == 'PC':
                    count += 1
                if count > 2:
                    clients.append(client_info[index])
                    break
                index += 1

    context = {'name': user.first_name, 'picture': user.picture_url}
    context.update({'client_info': reversed(clients), 'BASE_TAG_URL': BASE_TAG_URL})
    return render(request, "seenTags.html", context)

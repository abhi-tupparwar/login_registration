import ast
import json
import os

import jwt
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib import messages
from MaterializedDjango.settings import SECRET_KEY
from django.template import loader
from django.template.loader import get_template
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode
from django.views.decorators.cache import cache_control
from django.views.decorators.csrf import csrf_exempt

from material.models import MyUsers, Gallery


def index(request):
    if request.session.get('email', None):
        print(1212)
        return render(request, 'material/LoggedHome.html')
    else:
        print(11111111)
        return render(request, 'material/Home.html')


def login(request):
    if request.session.get('email', None):
            return redirect('/account/')
    else:
        return render(request, 'material/login.html')


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def account(request):
    if request.session.get('email', None):

        email = request.session['email']
        result = MyUsers.objects.get(email=email)

        if request.method == 'POST' and request.POST.get('register') == 'Upload':
            image = request.FILES.get('image')
            os.remove(result.pic.file.name)
            result.pic = image
            result.save()
            return redirect('/account')
        if request.method == 'POST' and request.POST.get('gallery') == 'Upload':
            for afile in request.FILES.getlist('images'):
                gallery = Gallery.objects.create(email=email, pic=afile)


        all_result = MyUsers.objects.exclude(email=email)
        pics = Gallery.objects.filter(email=email)

        context = {'details': result,
                   'gallery': pics,
                   'all_members': all_result,
                   'domain': 'href= //mail.'+email.split('@')[1]}
        return render(request, 'material/profile.html', context)
    else:
        return HttpResponse('<script>if (window.confirm("Please Login Again !!!")) { window.location.href = "/login"; }else { window.location.href = "/login"; } </script>')


def logout(request):
    if request.session.get('email', None):
        del request.session['email']
    return HttpResponseRedirect("/")


def signup(request):

    if request.session.get('email', None):
            return redirect('/account/')
    else:
        try:
            if request.method == 'POST':
                name = request.POST.get("name")
                email = request.POST.get("email")
                password = request.POST.get("password")
                gender = request.POST.get("gender")
                dob = request.POST.get("birthday")
                city = request.POST.get("city")
                image = request.FILES.get('image')
                current_site = get_current_site(request)

                template = get_template('material/contact_template.txt')
                context = {
                    'contact_name': name,
                    'contact_email': email,
                    'domain': current_site.domain,
                    'token': jwt.encode({"email": email}, SECRET_KEY, algorithm='HS256').decode("utf-8"),
                }
                content = template.render(context)

                print('1')
                send_mail(subject='Hello', message=content, from_email='abhitupparwar@gmail.com', recipient_list=[email], fail_silently=False)
                user = MyUsers.objects.create(uname=name, email=email, password=password, gender=gender, city=city,
                                              dob=dob, pic=image)
                request.session['email'] = email
                print('2')
                return redirect('/login')
            else:
                return render(request, 'material/register.html')

        except Exception as e:
            user.delete()
            return render(request, 'material/404.html')


def validate_user(request):
    email = request.GET.get("email")
    password = request.GET.get("password")
    print(email)
    print(password)
    request.session['email'] = email
    data = {
        'is_taken': MyUsers.objects.filter(email=email, password=password).exists()
    }
    print(data)
    return JsonResponse(data)


def validate_emai(request):
    print(1)
    email = request.GET.get('email')
    print(email)
    data = {
        'is_taken': MyUsers.objects.filter(email=email).exists()
    }
    return JsonResponse(data)


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def activate(request, token):
    try:
        token_decoded = jwt.decode(token, SECRET_KEY, algorithms='HS256');
        data = json.loads(json.dumps(ast.literal_eval(json.dumps(token_decoded, ensure_ascii=False))))
        print(data['email'])
        valid_user = MyUsers.objects.get(email=data['email'])
    except Exception as e:
        user = None
        return render(request, 'material/404.html')

    if valid_user != None:
        valid_user.verified = True
        valid_user.save()
        request.session['email'] = data['email']
        messages.info(request, 'Thankyou , Your email is now verified!!')
        return HttpResponseRedirect('/account/')
    else:
        return HttpResponse('Activation link is invalid!')


def editprofile(request):
    if request.session.get('email', None):
        try:
            if request.method == 'POST':
                newname = request.POST.get("name")
                newemail = request.POST.get("email")
                dob = request.POST.get("dob")
                city = request.POST.get("city")
                edit_user = MyUsers.objects.get(email=request.session['email'])

                if newname != edit_user.uname:
                    edit_user.uname = newname

                if dob != edit_user.dob:
                    edit_user.dob = dob

                if city != edit_user.city:
                    edit_user.city = city

                if newemail != request.session['email']:
                    edit_user.email = newemail
                    current_site = get_current_site(request)
                    template = get_template('material/contact_template.txt')
                    context = {
                        'contact_name': newname,
                        'contact_email': newemail,
                        'domain': current_site.domain,
                        'token': jwt.encode({"email": newemail}, SECRET_KEY, algorithm='HS256').decode("utf-8"),
                    }
                    content = template.render(context)
                    send_mail(subject='Hello', message=content, from_email='abhitupparwar@gmail.com',
                              recipient_list=[newemail], fail_silently=False)
                    edit_user.verified = False

                edit_user.save()
                print(1)
                request.session['email'] = newemail
                return redirect('/account/')

            email = request.session['email']
            result = MyUsers.objects.get(email=email)
            context = {'details': result}
            return render(request, 'material/editprofile.html', context)
        except Exception as e:
            del request.session['email']
            return render(request, 'material/404.html')
    else:
        return render(request, 'material/Home.html')


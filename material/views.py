import ast
import json

import jwt
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.template import loader
from django.template.loader import get_template
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode
from django.views.decorators.cache import cache_control
from django.views.decorators.csrf import csrf_exempt

from material.models import MyUsers


def index(request):
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
        all_result = MyUsers.objects.exclude(email=email)
        context = {'details': result,
                   'all_members': all_result}
        return render(request, 'material/profile.html', context)
    else:
        return HttpResponse('<script>if (window.confirm("Please Login Again !!!")) { window.location.href = "/login"; }else { window.location.href = "login"; } </script>')


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
                current_site = get_current_site(request)
                template = get_template('material/contact_template.txt')
                context = {
                    'contact_name': name,
                    'contact_email': email,
                    'domain': current_site.domain,
                    'token': jwt.encode({"email": email}, '810910', algorithm='HS256').decode("utf-8"),
                }
                content = template.render(context)

                print('1')
                send_mail(subject='Hello', message=content, from_email='abhitupparwar@gmail.com', recipient_list=[email],
                          fail_silently=False)
                user = MyUsers.objects.create(uname=name, email=email, password=password)
                request.session['email'] = email
                print('2')
                return redirect('/')
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


def activate(request,token):
    try:
        token_decoded = jwt.decode(token, '810910', algorithms='HS256');
        #data = json.dumps(ast.literal_eval(json.dumps(token_decoded, ensure_ascii=False)))
        data = json.loads(json.dumps(ast.literal_eval(json.dumps(token_decoded, ensure_ascii=False))))
        print(data['email'])
        valid_user = MyUsers.objects.get(email=data['email'])

    except(TypeError, ValueError, OverflowError, MyUsers.DoesNotExist):
        user = None
    if valid_user != None:
        valid_user.verified = True
        valid_user.save()
        return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    else:
        return HttpResponse('Activation link is invalid!')
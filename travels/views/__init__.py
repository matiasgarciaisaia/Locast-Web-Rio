import codecs
import settings
from django.utils import simplejson
import sys

from django.contrib.auth import authenticate, login, REDIRECT_FIELD_NAME
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.template.loader import render_to_string

from locast import get_model

from locast.auth.decorators import require_http_auth, optional_http_auth

from social.apps.django_app.default.models import UserSocialAuth

from travels import forms, models
from travels.models import Cast

import travels.social_networks as socials

@require_http_auth
def my_account(request):
    social_networks = socials.SocialNetworks(request.user)

    facebook_username = social_networks.facebook_username()
    twitter_username = social_networks.twitter_username()

    if request.method == 'POST':
        form = forms.MyAccountForm(request.POST, instance=request.user)

        if form.is_valid():            
            form.save()
            return render_to_response('my_account.django.html', locals(), context_instance = RequestContext(request))
    else:
        form = forms.MyAccountForm(instance=request.user)
    
    return render_to_response('my_account.django.html', locals(), context_instance = RequestContext(request))

def frontpage(request):
    fragment = request.GET.get('_escaped_fragment_')
    if fragment:
        return content_page(request, fragment)

    login_form = AuthenticationForm(request)
    register_form = forms.RegisterForm()

    urgency_rank = Cast.urgency_rank()

    urgency_rank_casts = zip(range(1,11), urgency_rank)

    return render_to_response('frontpage.django.html', locals(), context_instance = RequestContext(request))


def content_page(request, fragment):
    fragment = fragment.split('/');
    if len(fragment) < 2:
        raise Http404

    model = get_model(fragment[0])
    if not model or (not model == models.Cast):
        raise Http404

    try:
        id = int(fragment[1])
    except ValueError:
        raise Http404

    cast = get_object_or_404(model, id=id)

    return render_to_response('cast_view.django.html', locals(), context_instance = RequestContext(request))


def register(request):
    form = None

    if request.method == 'POST':
        form = forms.RegisterForm(request.POST)
        if form.is_valid():
            u = form.save()

            user_image = request.FILES.get('user_image', None)
            if user_image:
                u.user_image.save(user_image.name, user_image, save=True)

            models.UserActivity.objects.create_activity(u, u, 'joined')

            # Auto login the new user and redirect her to the home
            user = authenticate(username=u.username, password=request.POST['password'])
            login(request, user)

            return HttpResponseRedirect('/')

    elif request.method == 'GET':
        form = forms.RegisterForm()

    return render_to_response('registration/register.django.html', locals(), context_instance = RequestContext(request))

def travels_js(request):
    boundry_obj = models.Boundry.objects.get_default_boundry()
    boundry = 'null';

    if boundry_obj:
        boundry = boundry_obj.bounds.geojson

    return render_to_response('travels.django.js', locals(),
        context_instance = RequestContext(request), mimetype='text/javascript')


def templates_js(request):
    root = settings.STATIC_ROOT

    if settings.STATIC_ROOT == '':
        root = settings.DEV_STATIC_ROOT

    template_dir = root + 'js/templates/'

    template_files = [
        'castAddForm.js.html',
        'castClusterPopup.js.html',
        'castComments.js.html',
        'castHeaderList.js.html',
        'castPopup.js.html',
        'eventHeaderList.js.html',
        'eventPopup.js.html',
        'eventOpen.js.html',
        'itinHeaderList.js.html',
        'itinPopup.js.html',
        'mapCastList.js.html',
        'mapItinInfo.js.html',
        'searchResults.js.html',
        'userOpen.js.html'
    ]

    templates = {}
    for tf in template_files:
        try:
            ofile = codecs.open(template_dir + tf, encoding='utf8')
            templates[tf] = ofile.read()
        except IOError:
            pass

    content = 'var templates = ' + simplejson.dumps(templates);

    return HttpResponse(status=200, mimetype='application/json; charset=utf-8', content=content)


def iphone_welcome(request):
    json = render_to_string('mobile_static/iphone_welcome.django.json', locals(),
        context_instance = RequestContext(request))

    return HttpResponse(status=200, mimetype='application/json; charset=utf-8', content=json)


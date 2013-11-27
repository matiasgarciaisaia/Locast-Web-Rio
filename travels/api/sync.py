import sys
import traceback
import json

from django.contrib.gis.db import models as gismodels

from locast.api import *
from locast.api import rest, qstranslate, exceptions
from locast.auth.decorators import require_http_auth, optional_http_auth

from travels import models, forms
from travels.models import Itinerary
from travels.models import Cast
from travels.models import TravelsUser
from travels.models import Tag

from django.views.decorators.csrf import csrf_exempt

import travels.social_networks as socials

from travels.tasks import post_to_facebook
from travels.tasks import post_to_twitter

@csrf_exempt
class SyncAPI(rest.ResourceView):
    @require_http_auth    
    def post_spike(request):
        obj = json.loads(request.POST['parameters'])

        author = request.user

        itinerary = ensure_just_uploaded_itinerary(author)

        # Now we check whether the cast already exists. If that's the case, we return OK without
        # doing anything else, since this endpoint intends to be idempotent.
        try: 
            cast = Cast.objects.prefetch_related('media_set').get(guid=obj['_id'])

            image_syncd = (cast.prefetch_optimized_preview_image() != None)
            itinerary_syncd = cast.itinerary_set.all().count() > 0

            if image_syncd and itinerary_syncd:
                return HttpResponse(status=200)
            
            if not image_syncd:
                sync_media(author, cast, request)
            
            if not itinerary_syncd:
                add_to_itinerary(cast, itinerary)

        except Cast.DoesNotExist:
            print >> sys.stderr, "Cast didn't exist, creating it"
            create_cast(obj, author, itinerary, request)

        except Exception:
            print >> sys.stderr, sys.exc_info()[0]
            print >> traceback.print_exc()
            return HttpResponse(status=500)

        return APIResponseOK(content="success")

def sync_media(author, cast, request):
    #Media metadata
    media_data = {}
    #This is just for backwards compatibility, should eventually disappear unless we actually use title, description, etc.
    media_data['language'] = 'en'
    media_data['author'] = author.id
    media_data['title'] = 'image'
    media_data['description'] = 'image'

    form_model = forms.ImageMediaForm

    media = form_validate(form_model, media_data)
    cast.media_set.add(media)

    #Media content
    filename, files = request.FILES.popitem()            

    media.content.file.save(files[0].name, files[0], save=True)
    mime_type = media.path_to_mimetype(files[0].name, media.content.MIME_TYPES)
    
    media.content.mime_type = mime_type
    media.content.content_state = models.Media.STATE_COMPLETE
    media.content.save()

def add_to_itinerary(cast, itinerary):
    #Itinerary             
    itinerary.related_casts.add(cast)

def ensure_just_uploaded_itinerary(author):
    # We'll store uploaded reports to a default category 'Just uploaded'.
    # Here, we take care of creating it before continuing
    try:
        itinerary = Itinerary.objects.get(title="Just uploaded")
    except Itinerary.DoesNotExist:
        print >> sys.stderr, "-Just uploaded- category didn't exist, creating it"
        itinerary = Itinerary(title="Just uploaded", author_id=author.id)
        itinerary.save()

    return itinerary

def create_cast(json_dict, author, itinerary, request):
    title = json_dict['title']
    guid = json_dict['_id']
    cell_image = json_dict['imageUri']
    cell_timestamp = json_dict['timestamp']
    cell_revision = json_dict['_rev']
    attempts = json_dict['attempts']
    post_to_twitter = json_dict.get('postToTwitter', False)
    post_to_facebook = json_dict.get('postToFacebook', False)

    cast = Cast(title=title, title_en=title, guid=guid, author_id=author.id, cell_image=cell_image, cell_timestamp=cell_timestamp, cell_revision=cell_revision, attempts=attempts, post_to_twitter=post_to_twitter, post_to_facebook=post_to_facebook)

    cast.set_location(json_dict['longitude'], json_dict['latitude'])
    cast.save()            
    
    #Tags            
    cast.set_tags(','.join(json_dict.get('tags', [])))
    cast.save()    

    sync_media(author, cast, request)        
    add_to_itinerary(cast, itinerary)

    if author.can_post_to_social_networks:
        post_to_social_networks(cast, author, request)
        
def post_to_social_networks(cast, author, request):
    cast_uri = request.build_absolute_uri(cast.get_absolute_url())   
    thumbnail_uri = request.build_absolute_uri(cast.preview_image)     

    social_networks = socials.SocialNetworks(author)

    if cast.post_to_facebook:
        user_facebook_id = social_networks.facebook_user_id()

        if user_facebook_id:
            access_token = social_networks.facebook_access_token()
            post_to_facebook.delay(user_facebook_id, access_token, cast_uri, thumbnail_uri, cast.title)

    if cast.post_to_twitter:
        post_to_twitter.delay(author.id, cast.guid, cast_uri, social_networks.twitter_access_token(), social_networks.twitter_token_secret())



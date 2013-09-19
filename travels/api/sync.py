import sys

import json

from django.contrib.gis.db import models as gismodels

from locast.api import *
from locast.api import rest, qstranslate, exceptions
from locast.auth.decorators import require_http_auth, optional_http_auth

from travels import models
from travels.models import Itinerary
from travels.models import Cast
from travels.models import TravelsUser
from travels.models import Tag

class SyncAPI(rest.ResourceView):
    @optional_http_auth
    def post_spike(request):
        print >> sys.stderr, request.raw_post_data

        obj = json.loads(request.raw_post_data)

        # For this proof of concept, we'll use the admin user as author of the itinerary and cast
        try:
            author = TravelsUser.objects.get(email="unicef.gis.program@gmail.com")
        except TravelsUser.DoesNotExist:
            print >> sys.stderr, "Admin user does not exist"
            return HttpResponse(status=500)

        # We'll store uploaded reports to a default category 'Just uploaded'.
        # Here, we take care of creating it before continuing
        try:
            itinerary = Itinerary.objects.get(title="Just uploaded")
        except Itinerary.DoesNotExist:
            print >> sys.stderr, "-Just uploaded- category didn't exist, creating it"
            itinerary = Itinerary(title="Just uploaded", author_id=author.id)
            itinerary.save()

        # Now we check whether the cast already exists. If that's the case, we return OK without
        # doing anything else, since this endpoint intends to be idempotent.
        try: 
            cast = Cast.objects.get(guid=obj['_id'])
        except Cast.DoesNotExist:
            print >> sys.stderr, "Cast didn't exist, creating it"
            cast = Cast(title=obj['title'], title_en=obj['title'], guid=obj['_id'], author_id=author.id, cell_image=obj['imageUri'], cell_timestamp=obj['timestamp'], cell_revision=obj['_rev'], attempts=obj['attempts'])

            cast.set_location(obj['longitude'], obj['latitude'])
            cast.save()
            
            cast.set_tags(','.join(obj['tags']))
            cast.save()
            
            itinerary.related_casts.add(cast)

        return APIResponseOK(content="success")



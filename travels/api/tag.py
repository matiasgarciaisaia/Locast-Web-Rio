from locast.api import *
from locast.api import rest, qstranslate, exceptions
from locast.auth.decorators import optional_http_auth, require_http_auth

from travels.models import TravelsUser
from travels.models import Tag

class TagAPI(rest.ResourceView):
    def get_all(request):
        try:
            tags = Tag.objects.order_by('name').all()
        except qstranslate.InvalidParameterException, e:
            raise exceptions.APIBadRequest(e.message)

        tag_arr = [t.name for t in tags]

        return APIResponseOK(content=tag_arr)

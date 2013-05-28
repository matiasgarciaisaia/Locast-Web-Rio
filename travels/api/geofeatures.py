from locast.api import *
from locast.api import qstranslate, exceptions

from django.contrib.gis.geos import Polygon
from django.db.models import Q
from django.views.decorators.cache import cache_page

from locast.api import cache

from travels import cache_control, models
from travels.api.cast import CastAPI
from time import time

def get_geofeatures(request):
    t_start = time()

    cache_key = _generate_cache_key(request)
    cache_val = cache.get(cache_key, cache_control.GEOFEATURES_CACHE_GROUP)
    if cache_val:
        return APIResponseOK(content=cache_val)

    bounds_param = get_param(request.GET, 'within')
    query = request.GET.copy()

    if bounds_param:
        pnts = bounds_param.split(',')

        bbox = (float(pnts[0]), float(pnts[1]),
                float(pnts[2]), float(pnts[3]))

        poly = Polygon.from_bbox(bbox)
        poly.set_srid(4326)

        del query['within']

    base_query = Q()
    if bounds_param:
        base_query = base_query & Q(location__within=poly)

    # cast within bounds
    cast_base_query = models.Cast.get_privacy_q(request) & base_query

    q = qstranslate.QueryTranslator(models.Cast, CastAPI.ruleset, cast_base_query)

    try:
        casts = q.filter(query).select_related('author').prefetch_related('media_set')
    except qstranslate.InvalidParameterException, e:
        raise exceptions.APIBadRequest(e.message)

    t_filter = time()

    cast_arr = []

    t_total_serialization = 0

    for c in casts:
        if c.location:
            t_0 = time()
            s = geojson_serialize(c, c.location, request)
            t_total_serialization += (time() - t_0)

            cast_arr.append(s)

    t_final_cast = time()

    #event within bounds
    events = models.Event.objects.filter(base_query)

    event_arr = []
    for e in events:
        if e.location:
            event_arr.append(geojson_serialize(e, e.location, request))

    # itinerary intersects bounds
    if bounds_param:
        base_query = Q(path__intersects = poly)

    itins = models.Itinerary.objects.filter(base_query)

    itin_arr = []
    for i in itins:
        if i.path:
            itin_arr.append(geojson_serialize(i, i.path, request))

    features_dict = {}
    features_dict['casts'] = dict(type='FeatureCollection', features=cast_arr)
    features_dict['events'] = dict(type='FeatureCollection', features=event_arr)
    features_dict['itineraries'] = dict(type='FeatureCollection', features=itin_arr)

    cache.set(_generate_cache_key(request), features_dict, cache_control.GEOFEATURES_CACHE_GROUP)

    t_final = time()

    print "Total time %f" %(t_final - t_start)
    print "Time append location %f" %(t_final_cast - t_filter)
    print "Time spent in serializing %f" %(t_total_serialization)

    from django.db import connection
    for query in connection.queries:
        print query['sql']

    return APIResponseOK(content=features_dict)

# Should vary on the authenticated user and the query string
def _generate_cache_key(request):
    qd = request.GET.copy()

    # Removing the client cache parameter
    if '_' in qd:
        del qd['_']
    key = qd.urlencode() + '_'

    if request.user.is_authenticated():
        key = key + str(request.user.id)

    return key


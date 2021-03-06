import cgi
import httplib
import settings
import urllib
import urlparse

from django.core import cache
from django.core.urlresolvers import reverse
from django.db import models
from django.db.models import Sum
from django.contrib.gis.db import models as gismodels
from django.contrib.gis.db.models.manager import GeoManager
from django.utils import simplejson
from django.utils.translation import ugettext_lazy as _

from locast.api import datetostr, cache
from locast.models import interfaces, modelbases, managers
from locast.models import ModelBase

from sorl.thumbnail import get_thumbnail

from datetime import datetime


# DEPENDENCIES

class Tag(interfaces.Tag):
    urgency_score = models.IntegerField("Urgency Score", blank=False, default=0)

class Comment(interfaces.Comment,
        interfaces.Flaggable):

    # TODO: this should be more generic incase anything else becomes commentable
    @models.permalink
    def get_api_uri(self):
        return ('cast_comments_api_single', [self.content_object.id, self.id])

    def get_absolute_url(self):
        return self.content_object.get_absolute_url()

class Flag(interfaces.Flag): pass

class UserActivity(modelbases.UserActivity): pass

class Boundry(modelbases.Boundry): pass

# MAIN MODELS

class Settings(ModelBase, interfaces.Locatable):
    project_title = models.CharField("Project's title, displayed on initial splash screen", max_length=256, blank=True, default="Welcome to UNICEF's Youth Led Digital Mapping")
    project_description = models.TextField("Project's description, a more detailed paragraph describing the project", blank=True, default="This project explores tools to help youth build impactful, communicative digital maps using mobile and web technologies. A phone application allows youth to produce a realtime portrait of their community through geo-located photos and videos, organized in thematic maps.")
    window_title = models.CharField("Window title, it appears on the browsers top bar or tab, so it should be short and to the point", max_length=256, blank=True, default="UNICEF's Youth Led Digital Mapping")

class TravelsUserManager(GeoManager,
        managers.LocastUserManager,
        managers.FacebookUserManager): pass

class TravelsUser(modelbases.LocastUser,
        interfaces.FacebookUser,
        interfaces.Locatable):

    @models.permalink
    def get_api_uri(self):
        return ('user_api_single', [str(self.id)])

    def __unicode__(self):
        if self.email:
            return u'%s' % self.email
        else:
            return u'%s' % self.username

    def api_serialize(self, request):
        d = {}

        if self.is_facebook_user():
            d['user_image'] = 'http://graph.facebook.com/%s/picture?type=large' % self.facebook_id
        elif self.user_image:
            d['user_image'] = self.user_image.url

        if self.profile:
            d['profile'] = self.profile

        if self.personal_url:
            d['personal_url'] = self.personal_url

        if self.hometown:
            d['hometown'] = self.hometown

        return d

    objects = TravelsUserManager()

    user_image = models.ImageField(upload_to='user_images/%Y/%m/', null=True, blank=True)

    personal_url = models.URLField(null=True, blank=True)

    hometown = models.CharField(max_length=128, null=True, blank=True)

    can_post_to_social_networks = models.BooleanField(default=False)


class Itinerary(ModelBase,
        interfaces.Authorable,
        interfaces.Titled,
        interfaces.Taggable,
        interfaces.Favoritable):

    @models.permalink
    def get_api_uri(self):
        return ('itinerary_api_single', [str(self.id)])

    class Meta:
        verbose_name = _('itinerary')
        verbose_name_plural = _('itineraries')

    def __unicode__(self):
        return u'(id: %s) %s' % (str(self.id), self.title)

    def api_serialize(self, request):
        d = {}
        if self.path:
            d['path'] = self.path.coords
        d['casts'] = reverse('itinerary_cast_api', kwargs={'itin_id':self.id})

        d['casts_ids'] = []
        for c in self.related_casts.all():
            d['casts_ids'].append(c.id)

        d['casts_count'] = self.related_casts.count()
        if self.preview_image:
            d['preview_image'] = self.preview_image.url
            d['thumbnail'] = self.thumbnail.url

        return d

    def geojson_properties(self, request):
        d = {}
        d['id'] = self.id
        d['title'] = self.title
        d['casts_count'] = self.related_casts.count()
        d['favorites'] = self.favorited_by.count()

        if self.preview_image:
            d['preview_image'] = self.preview_image.url
            d['thumbnail'] = self.thumbnail.url

        return d

    objects = GeoManager()

    related_casts = models.ManyToManyField('Cast', null=True, blank=True)

    path = gismodels.LineStringField(null=True,blank=True,srid=4326)

    preview_image = models.ImageField(upload_to='content_images', null=True, blank=True)

    @property
    def thumbnail(self):
        try:
            return get_thumbnail(self.preview_image, '600', quality=75)
        except: 
            return get_thumbnail(settings.PLACEHOLDER_PATH, '600', quality=75)


class Event(ModelBase,
        interfaces.Locatable,
        interfaces.Authorable,
        interfaces.Taggable,
        interfaces.Titled):

    class Meta:
        verbose_name = _('event')

    def __unicode__(self):
        return u'%s (%s)' % (self.title, self.start_date)

    @models.permalink
    def get_api_uri(self):
        return ('event_api_single', [str(self.id)])

    objects = GeoManager()

    def api_serialize(self, request):
        d = {}
        d['start_date'] = datetostr(self.start_date)
        d['end_date'] = datetostr(self.end_date)

        return d

    def geojson_properties(self, request):
        d = {}
        d['id'] = self.id
        d['title'] = self.title
        d['start_date'] = datetostr(self.start_date)
        d['end_date'] = datetostr(self.end_date)

        return d

    start_date = models.DateTimeField('start_date')
    end_date = models.DateTimeField('end_date')


class Cast(ModelBase,
        interfaces.PrivatelyAuthorable,
        interfaces.Titled,
        interfaces.Commentable,
        interfaces.Favoritable,
        interfaces.Flaggable,
        interfaces.Locatable,
        interfaces.Taggable):

    attempts = models.IntegerField(null=True, default=0)
    cell_image = models.TextField(blank=True)
    cell_timestamp = models.CharField(max_length=32, blank=True)
    guid = models.CharField(max_length=64, blank=True)
    cell_revision = models.CharField(max_length=64, blank=True)
    post_to_twitter = models.BooleanField(default=False)
    post_to_facebook = models.BooleanField(default=False)

    @models.permalink
    def get_api_uri(self):
        return ('cast_api_single', [str(self.id)])

    def get_absolute_url(self):
        return reverse('frontpage') + '#!cast/' + str(self.id) + '/'

    def absolute_url_with_host(self):
        return settings.FULL_BASE_URL + self.get_absolute_url()

    class Meta:
        verbose_name = _('cast')

    def __unicode__(self):
        return u'%s (id: %s)' % (self.title, str(self.id))

    objects = GeoManager()

    def api_serialize(self, request):
        d = {}

        d['itineraries_ids'] = []
        for i in self.itinerary_set.all():
            d['itineraries_ids'].append(i.id)

        d['media'] = reverse('cast_media_api', kwargs={'cast_id':self.id})
        d['comments'] = reverse('cast_comments_api', kwargs={'cast_id':self.id})

        d['featured'] = self.is_featured
        d['promotional'] = self.is_promotional
        d['official'] = self.author.is_staff

        if self.preview_image:
            d['preview_image'] = self.preview_image

        d['primary_image'] = self.prefetched_primary_image()

        return d

    def geojson_properties(self, request):
        d = {}
        d['id'] = self.id
        d['title'] = self.title
        d['author'] = {'id' : self.author.id, 'display_name' : self.author.display_name }
        d['official'] = self.author.is_staff
        d['urgency_level'] = self.urgency_level()

        if self.prefetch_optimized_preview_image:
            d['preview_image'] = self.prefetch_optimized_preview_image()

        return d

    def urgency_rank_serialize(self, request, rank=0):
        d = {}
        d['id'] = self.id
        d['title'] = self.title
        d['urgency_level'] = self.urgency_level()

        d['thumbnail'] = self.prefetch_optimized_preview_image()
        d['rank'] = rank

        d['created'] = self.created.strftime("%b %d, %Y")

        categories = self.itinerary_set.all()

        if len(categories) > 0:
            d['category'] = categories[0].title
        else:
            d['category'] = 'None'

        d['tags'] = [tag.name for tag in self.tags.all()]

        return d

    def urgency_level(self):
        urgency_score = sum([tag.urgency_score for tag in self.tags.all()])
        return urgency_score / 50


    @property
    def is_featured(self):
        return (not self.get_tag_by_name('_featured') == None)

    @property
    def is_promotional(self):
        return (not self.get_tag_by_name('_promotional') == None)

    # Use this methods instead of 'preview_image' when you know the related media has been
    # prefetched
    def prefetch_optimized_preview_image(self):
        images = [i for i in self.media_set.all() if i.content_type_model == 'imagemedia']
        videos = [v for v in self.media_set.all() if v.content_type_model == 'videomedia']
        links = [l for l in self.media_set.all() if l.content_type_model == 'linkedmedia']

        return self.preview_image_from_given_media(images, videos, links)

    def prefetched_primary_image(self):
        images = [i for i in self.media_set.all() if i.content_type_model == 'imagemedia']

        for image_base in images:
            image = image_base.content
            if image and image.file and image.medium_file:
                return image.medium_file.url

        return None

    def preview_image_from_given_media(self, images, videos, links):
        for image_base in images:
          image = image_base.content
          if image and image.file:
            return image.thumbnail.url

        for video_base in videos:
          vid = video_base.content
          if vid and vid.screenshot:
            return vid.screenshot.url

        for link_base in links:
          vid = link_base.content
          if vid and vid.screenshot:
            return vid.screenshot

        return None

    @property
    def preview_image(self):
        return self.preview_image_from_given_media(self.imagemedia, self.videomedia, self.linkedmedia)

    @property
    def videomedia(self):
        return self.media_set.filter(content_type_model='videomedia')

    @property
    def imagemedia(self):
        return self.media_set.filter(content_type_model='imagemedia')

    @property
    def linkedmedia(self):
        return self.media_set.filter(content_type_model='linkedmedia')

    @staticmethod
    def urgency_rank():
        return Cast.objects.prefetch_related('itinerary_set').select_related('author').prefetch_related('media_set').prefetch_related('tags').annotate(urgency_score=Sum('tags__urgency_score')).filter(urgency_score__gt=0).order_by('-urgency_score')[:10]


class Media(modelbases.LocastContent,
        interfaces.Authorable,
        interfaces.Titled,
        interfaces.Locatable):

    @models.permalink
    def get_api_uri(self):
        return ('cast_media_api_single', [str(self.cast.id), str(self.id)])

    def api_serialize(self, request):
        d = {}
        d['language'] = self.language
        if self.cast:
            d['cast'] = self.cast.get_api_uri()

        return d

    objects = GeoManager()

    language = models.CharField(max_length=90,choices=settings.LANGUAGES, default='en')

    cast = models.ForeignKey(Cast, null=True, blank=True)


class VideoMedia(Media,
        modelbases.VideoContent):

    class Meta:
        verbose_name = _('video')

    def pre_save(self):
        if self.content_state == Media.STATE_INCOMPLETE:
            if self.file and self.file.size:
                self.content_state = Media.STATE_COMPLETE

    def process(self, force_update=False, verbose=False):
        if self.content_state == Media.STATE_COMPLETE or force_update:
            self.content_state = Media.STATE_PROCESSING
            self.generate_screenshot(force_update=force_update, verbose=verbose)
            self.generate_web_stream(force_update=force_update, verbose=verbose)
            self.make_mobile_streamable()


class ImageMedia(Media,
        modelbases.ImageContent):

    class Meta:
        verbose_name = _('photo')

    # Overwrite the ImageContent._content_api_serialize method to provide
    # thumbnails
    def _content_api_serialize(self, request=None):
        d = {}
        if self.file:
            d['resources'] = {}
            d['resources']['primary'] = self.serialize_resource(self.file.url)
            d['resources']['medium'] = self.serialize_resource(self.medium_file.url)
            d['resources']['thumbnail'] = self.serialize_resource(self.thumbnail.url)

        return d

    def primary_url(self):
        if self.file:
            self.serialize_resource(self.file.url)

    @property
    def thumbnail(self):
        try:
            return get_thumbnail(self.file, '150', quality=75)
        except: 
            return get_thumbnail(settings.PLACEHOLDER_PATH, '150', quality=75)

    @property
    def medium_file(self):
        try:
            return get_thumbnail(self.file, '600', quality=75)
        except: 
            return get_thumbnail(settings.PLACEHOLDER_PATH, '600', quality=75)

    def process(self):
        pass


CONTENT_PROVIDERS = (
    ('youtube.com', 'YouTube'),
    ('vimeo.com', 'Vimeo')
)

class LinkedMedia(Media):

    class Meta:
        verbose_name = _('link')

    url = models.URLField()

    screenshot = models.URLField(null=True, blank=True)

    content_provider = models.CharField(max_length=32, choices=CONTENT_PROVIDERS)

    video_id = models.CharField(max_length=32)

    def _content_api_serialize(self, request=None):
        d = dict(url=self.url)

        if self.screenshot:
            d['resources'] = {
                'screenshot' : self.serialize_resource(self.screenshot)
            }

        if self.content_provider:
            d['content_provider'] = self.content_provider

        return d

    def pre_save(self):
        if self.url and not self.video_id:
            self.process()

    def process(self):

        # Check if the link exists
        url_data = urlparse.urlparse(self.url)
        conn = httplib.HTTPConnection(url_data.hostname)

        full_path = url_data.path
        if url_data.query:
            full_path += '?' + url_data.query

        conn.request('HEAD', full_path)
        r1 = conn.getresponse()
        conn.close()

        # it exists! (302 is a redirect for sharing links i.e. youtu.be)
        if r1.status == 200 or r1.status == 302:
            self.content_provider = url_data.hostname.lstrip('www.')
            query = cgi.parse_qs(url_data.query)

            # youtube
            if self.content_provider == 'youtube.com' or self.content_provider == 'youtu.be':
                if self.content_provider == 'youtube.com':
                    self.video_id = query['v'][0]

                else:
                    self.video_id = self.url.split('/').pop()
                    self.content_provider = 'youtube.com'
                    self.url = 'http://www.youtube.com/watch?v=' + self.video_id

                data_url = 'http://gdata.youtube.com/feeds/api/videos/' + self.video_id + '?v=2&alt=json'
                youtube_data = simplejson.load(urllib.urlopen(data_url))

                thumbs = youtube_data['entry']['media$group']['media$thumbnail']
                if len(thumbs) > 1:
                    self.screenshot = thumbs[1]['url']
                elif len(thumbs):
                    self.screenshot = thumbs[0]['url']

                self.title = youtube_data['entry']['title']['$t']

            # vimeo
            elif self.content_provider == 'vimeo.com':
                self.video_id = url_data.path.lstrip('/')
                data_url = 'http://vimeo.com/api/v2/video/' + self.video_id + '.json'
                vimeo_data = simplejson.load(urllib.urlopen(data_url))

                self.screenshot = vimeo_data[0]['thumbnail_large']
                self.title = vimeo_data[0]['title']

# CACHE CONROLER
import cache_control


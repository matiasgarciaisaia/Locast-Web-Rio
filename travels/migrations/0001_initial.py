# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Tag'
        db.create_table(u'travels_tag', (
            ('name', self.gf('django.db.models.fields.CharField')(max_length=32, primary_key=True)),
            ('system_tag', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'travels', ['Tag'])

        # Adding model 'Comment'
        db.create_table(u'travels_comment', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('author', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['travels.TravelsUser'])),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('object_id', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('content_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['contenttypes.ContentType'])),
            ('body', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal(u'travels', ['Comment'])

        # Adding model 'Flag'
        db.create_table(u'travels_flag', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('object_id', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('content_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['contenttypes.ContentType'])),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['travels.TravelsUser'])),
            ('reason', self.gf('django.db.models.fields.CharField')(max_length=64)),
        ))
        db.send_create_signal(u'travels', ['Flag'])

        # Adding model 'UserActivity'
        db.create_table(u'travels_useractivity', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['travels.TravelsUser'])),
            ('time', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('action', self.gf('django.db.models.fields.CharField')(max_length=140, blank=True)),
            ('object_id', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('content_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['contenttypes.ContentType'])),
        ))
        db.send_create_signal(u'travels', ['UserActivity'])

        # Adding model 'Boundry'
        db.create_table(u'travels_boundry', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=160)),
            ('bounds', self.gf('django.contrib.gis.db.models.fields.PolygonField')()),
            ('default', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'travels', ['Boundry'])

        # Adding model 'TravelsUser'
        db.create_table(u'travels_travelsuser', (
            (u'user_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['auth.User'], unique=True, primary_key=True)),
            ('location', self.gf('django.contrib.gis.db.models.fields.PointField')(null=True, blank=True)),
            ('facebook_id', self.gf('django.db.models.fields.BigIntegerField')(null=True, blank=True)),
            ('display_name', self.gf('django.db.models.fields.CharField')(max_length=32, null=True, blank=True)),
            ('profile', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('language', self.gf('django.db.models.fields.CharField')(default='en', max_length=90)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('user_image', self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True, blank=True)),
            ('personal_url', self.gf('django.db.models.fields.URLField')(max_length=200, null=True, blank=True)),
            ('hometown', self.gf('django.db.models.fields.CharField')(max_length=128, null=True, blank=True)),
        ))
        db.send_create_signal(u'travels', ['TravelsUser'])

        # Adding model 'Itinerary'
        db.create_table(u'travels_itinerary', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('author', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['travels.TravelsUser'])),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=160)),
            ('title_en', self.gf('django.db.models.fields.CharField')(max_length=160, null=True, blank=True)),
            ('title_fr', self.gf('django.db.models.fields.CharField')(max_length=160, null=True, blank=True)),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('description_en', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('description_fr', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('path', self.gf('django.contrib.gis.db.models.fields.LineStringField')(null=True, blank=True)),
            ('preview_image', self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True, blank=True)),
        ))
        db.send_create_signal(u'travels', ['Itinerary'])

        # Adding M2M table for field favorited_by on 'Itinerary'
        db.create_table(u'travels_itinerary_favorited_by', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('itinerary', models.ForeignKey(orm[u'travels.itinerary'], null=False)),
            ('travelsuser', models.ForeignKey(orm[u'travels.travelsuser'], null=False))
        ))
        db.create_unique(u'travels_itinerary_favorited_by', ['itinerary_id', 'travelsuser_id'])

        # Adding M2M table for field tags on 'Itinerary'
        db.create_table(u'travels_itinerary_tags', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('itinerary', models.ForeignKey(orm[u'travels.itinerary'], null=False)),
            ('tag', models.ForeignKey(orm[u'travels.tag'], null=False))
        ))
        db.create_unique(u'travels_itinerary_tags', ['itinerary_id', 'tag_id'])

        # Adding M2M table for field related_casts on 'Itinerary'
        db.create_table(u'travels_itinerary_related_casts', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('itinerary', models.ForeignKey(orm[u'travels.itinerary'], null=False)),
            ('cast', models.ForeignKey(orm[u'travels.cast'], null=False))
        ))
        db.create_unique(u'travels_itinerary_related_casts', ['itinerary_id', 'cast_id'])

        # Adding model 'Event'
        db.create_table(u'travels_event', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('author', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['travels.TravelsUser'])),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=160)),
            ('title_en', self.gf('django.db.models.fields.CharField')(max_length=160, null=True, blank=True)),
            ('title_fr', self.gf('django.db.models.fields.CharField')(max_length=160, null=True, blank=True)),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('description_en', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('description_fr', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('location', self.gf('django.contrib.gis.db.models.fields.PointField')(null=True, blank=True)),
            ('start_date', self.gf('django.db.models.fields.DateTimeField')()),
            ('end_date', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal(u'travels', ['Event'])

        # Adding M2M table for field tags on 'Event'
        db.create_table(u'travels_event_tags', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('event', models.ForeignKey(orm[u'travels.event'], null=False)),
            ('tag', models.ForeignKey(orm[u'travels.tag'], null=False))
        ))
        db.create_unique(u'travels_event_tags', ['event_id', 'tag_id'])

        # Adding model 'Cast'
        db.create_table(u'travels_cast', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('author', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['travels.TravelsUser'])),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('privacy', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=2, null=True, blank=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=160)),
            ('title_en', self.gf('django.db.models.fields.CharField')(max_length=160, null=True, blank=True)),
            ('title_fr', self.gf('django.db.models.fields.CharField')(max_length=160, null=True, blank=True)),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('description_en', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('description_fr', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('location', self.gf('django.contrib.gis.db.models.fields.PointField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'travels', ['Cast'])

        # Adding M2M table for field favorited_by on 'Cast'
        db.create_table(u'travels_cast_favorited_by', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('cast', models.ForeignKey(orm[u'travels.cast'], null=False)),
            ('travelsuser', models.ForeignKey(orm[u'travels.travelsuser'], null=False))
        ))
        db.create_unique(u'travels_cast_favorited_by', ['cast_id', 'travelsuser_id'])

        # Adding M2M table for field tags on 'Cast'
        db.create_table(u'travels_cast_tags', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('cast', models.ForeignKey(orm[u'travels.cast'], null=False)),
            ('tag', models.ForeignKey(orm[u'travels.tag'], null=False))
        ))
        db.create_unique(u'travels_cast_tags', ['cast_id', 'tag_id'])

        # Adding model 'Media'
        db.create_table(u'travels_media', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('author', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['travels.TravelsUser'])),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=160)),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('location', self.gf('django.contrib.gis.db.models.fields.PointField')(null=True, blank=True)),
            ('content_type_model', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('content_state', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=1)),
            ('mime_type', self.gf('django.db.models.fields.CharField')(max_length=90, null=True, blank=True)),
            ('language', self.gf('django.db.models.fields.CharField')(default='en', max_length=90)),
            ('cast', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['travels.Cast'], null=True, blank=True)),
        ))
        db.send_create_signal(u'travels', ['Media'])

        # Adding model 'VideoMedia'
        db.create_table(u'travels_videomedia', (
            (u'media_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['travels.Media'], unique=True, primary_key=True)),
            ('file', self.gf('django.db.models.fields.files.FileField')(max_length=100, blank=True)),
            ('compressed_file', self.gf('django.db.models.fields.files.FileField')(max_length=100, blank=True)),
            ('web_stream_file', self.gf('django.db.models.fields.files.FileField')(max_length=100, blank=True)),
            ('screenshot', self.gf('django.db.models.fields.files.ImageField')(max_length=100, blank=True)),
            ('animated_preview', self.gf('django.db.models.fields.files.FileField')(max_length=100, blank=True)),
            ('duration', self.gf('django.db.models.fields.TimeField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'travels', ['VideoMedia'])

        # Adding model 'ImageMedia'
        db.create_table(u'travels_imagemedia', (
            (u'media_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['travels.Media'], unique=True, primary_key=True)),
            ('file', self.gf('django.db.models.fields.files.FileField')(max_length=100, blank=True)),
        ))
        db.send_create_signal(u'travels', ['ImageMedia'])

        # Adding model 'LinkedMedia'
        db.create_table(u'travels_linkedmedia', (
            (u'media_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['travels.Media'], unique=True, primary_key=True)),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('screenshot', self.gf('django.db.models.fields.URLField')(max_length=200, null=True, blank=True)),
            ('content_provider', self.gf('django.db.models.fields.CharField')(max_length=32)),
            ('video_id', self.gf('django.db.models.fields.CharField')(max_length=32)),
        ))
        db.send_create_signal(u'travels', ['LinkedMedia'])


    def backwards(self, orm):
        
        # Deleting model 'Tag'
        db.delete_table(u'travels_tag')

        # Deleting model 'Comment'
        db.delete_table(u'travels_comment')

        # Deleting model 'Flag'
        db.delete_table(u'travels_flag')

        # Deleting model 'UserActivity'
        db.delete_table(u'travels_useractivity')

        # Deleting model 'Boundry'
        db.delete_table(u'travels_boundry')

        # Deleting model 'TravelsUser'
        db.delete_table(u'travels_travelsuser')

        # Deleting model 'Itinerary'
        db.delete_table(u'travels_itinerary')

        # Removing M2M table for field favorited_by on 'Itinerary'
        db.delete_table('travels_itinerary_favorited_by')

        # Removing M2M table for field tags on 'Itinerary'
        db.delete_table('travels_itinerary_tags')

        # Removing M2M table for field related_casts on 'Itinerary'
        db.delete_table('travels_itinerary_related_casts')

        # Deleting model 'Event'
        db.delete_table(u'travels_event')

        # Removing M2M table for field tags on 'Event'
        db.delete_table('travels_event_tags')

        # Deleting model 'Cast'
        db.delete_table(u'travels_cast')

        # Removing M2M table for field favorited_by on 'Cast'
        db.delete_table('travels_cast_favorited_by')

        # Removing M2M table for field tags on 'Cast'
        db.delete_table('travels_cast_tags')

        # Deleting model 'Media'
        db.delete_table(u'travels_media')

        # Deleting model 'VideoMedia'
        db.delete_table(u'travels_videomedia')

        # Deleting model 'ImageMedia'
        db.delete_table(u'travels_imagemedia')

        # Deleting model 'LinkedMedia'
        db.delete_table(u'travels_linkedmedia')


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 5, 15, 19, 57, 33, 409422)'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 5, 15, 19, 57, 33, 408439)'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'travels.boundry': {
            'Meta': {'object_name': 'Boundry'},
            'bounds': ('django.contrib.gis.db.models.fields.PolygonField', [], {}),
            'default': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '160'})
        },
        u'travels.cast': {
            'Meta': {'object_name': 'Cast'},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['travels.TravelsUser']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'description_en': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'description_fr': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'favorited_by': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'favorite_cast'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['travels.TravelsUser']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.contrib.gis.db.models.fields.PointField', [], {'null': 'True', 'blank': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'privacy': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '2', 'null': 'True', 'blank': 'True'}),
            'tags': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'tag_cast'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['travels.Tag']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '160'}),
            'title_en': ('django.db.models.fields.CharField', [], {'max_length': '160', 'null': 'True', 'blank': 'True'}),
            'title_fr': ('django.db.models.fields.CharField', [], {'max_length': '160', 'null': 'True', 'blank': 'True'})
        },
        u'travels.comment': {
            'Meta': {'object_name': 'Comment'},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['travels.TravelsUser']"}),
            'body': ('django.db.models.fields.TextField', [], {}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {})
        },
        u'travels.event': {
            'Meta': {'object_name': 'Event'},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['travels.TravelsUser']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'description_en': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'description_fr': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'end_date': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.contrib.gis.db.models.fields.PointField', [], {'null': 'True', 'blank': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'start_date': ('django.db.models.fields.DateTimeField', [], {}),
            'tags': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'tag_event'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['travels.Tag']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '160'}),
            'title_en': ('django.db.models.fields.CharField', [], {'max_length': '160', 'null': 'True', 'blank': 'True'}),
            'title_fr': ('django.db.models.fields.CharField', [], {'max_length': '160', 'null': 'True', 'blank': 'True'})
        },
        u'travels.flag': {
            'Meta': {'object_name': 'Flag'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'reason': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['travels.TravelsUser']"})
        },
        u'travels.imagemedia': {
            'Meta': {'object_name': 'ImageMedia', '_ormbases': [u'travels.Media']},
            'file': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'blank': 'True'}),
            u'media_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['travels.Media']", 'unique': 'True', 'primary_key': 'True'})
        },
        u'travels.itinerary': {
            'Meta': {'object_name': 'Itinerary'},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['travels.TravelsUser']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'description_en': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'description_fr': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'favorited_by': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'favorite_itinerary'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['travels.TravelsUser']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'path': ('django.contrib.gis.db.models.fields.LineStringField', [], {'null': 'True', 'blank': 'True'}),
            'preview_image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'related_casts': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['travels.Cast']", 'null': 'True', 'blank': 'True'}),
            'tags': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'tag_itinerary'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['travels.Tag']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '160'}),
            'title_en': ('django.db.models.fields.CharField', [], {'max_length': '160', 'null': 'True', 'blank': 'True'}),
            'title_fr': ('django.db.models.fields.CharField', [], {'max_length': '160', 'null': 'True', 'blank': 'True'})
        },
        u'travels.linkedmedia': {
            'Meta': {'object_name': 'LinkedMedia', '_ormbases': [u'travels.Media']},
            'content_provider': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            u'media_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['travels.Media']", 'unique': 'True', 'primary_key': 'True'}),
            'screenshot': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'video_id': ('django.db.models.fields.CharField', [], {'max_length': '32'})
        },
        u'travels.media': {
            'Meta': {'object_name': 'Media'},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['travels.TravelsUser']"}),
            'cast': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['travels.Cast']", 'null': 'True', 'blank': 'True'}),
            'content_state': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '1'}),
            'content_type_model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language': ('django.db.models.fields.CharField', [], {'default': "'en'", 'max_length': '90'}),
            'location': ('django.contrib.gis.db.models.fields.PointField', [], {'null': 'True', 'blank': 'True'}),
            'mime_type': ('django.db.models.fields.CharField', [], {'max_length': '90', 'null': 'True', 'blank': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '160'})
        },
        u'travels.tag': {
            'Meta': {'object_name': 'Tag'},
            'name': ('django.db.models.fields.CharField', [], {'max_length': '32', 'primary_key': 'True'}),
            'system_tag': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        u'travels.travelsuser': {
            'Meta': {'object_name': 'TravelsUser'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'display_name': ('django.db.models.fields.CharField', [], {'max_length': '32', 'null': 'True', 'blank': 'True'}),
            'facebook_id': ('django.db.models.fields.BigIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'hometown': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'language': ('django.db.models.fields.CharField', [], {'default': "'en'", 'max_length': '90'}),
            'location': ('django.contrib.gis.db.models.fields.PointField', [], {'null': 'True', 'blank': 'True'}),
            'personal_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'profile': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'user_image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            u'user_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['auth.User']", 'unique': 'True', 'primary_key': 'True'})
        },
        u'travels.useractivity': {
            'Meta': {'object_name': 'UserActivity'},
            'action': ('django.db.models.fields.CharField', [], {'max_length': '140', 'blank': 'True'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'time': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['travels.TravelsUser']"})
        },
        u'travels.videomedia': {
            'Meta': {'object_name': 'VideoMedia', '_ormbases': [u'travels.Media']},
            'animated_preview': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'blank': 'True'}),
            'compressed_file': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'blank': 'True'}),
            'duration': ('django.db.models.fields.TimeField', [], {'null': 'True', 'blank': 'True'}),
            'file': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'blank': 'True'}),
            u'media_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['travels.Media']", 'unique': 'True', 'primary_key': 'True'}),
            'screenshot': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            'web_stream_file': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'blank': 'True'})
        }
    }

    complete_apps = ['travels']

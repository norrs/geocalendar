# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'CalendarEntry'
        db.create_table('geocal_calendarentry', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('entry_date', self.gf('django.db.models.fields.DateField')()),
            ('keyword', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('picture', self.gf('filebrowser.fields.FileBrowseField')(max_length=500)),
        ))
        db.send_create_signal('geocal', ['CalendarEntry'])


    def backwards(self, orm):
        
        # Deleting model 'CalendarEntry'
        db.delete_table('geocal_calendarentry')


    models = {
        'geocal.calendarentry': {
            'Meta': {'object_name': 'CalendarEntry'},
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'entry_date': ('django.db.models.fields.DateField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'keyword': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'picture': ('filebrowser.fields.FileBrowseField', [], {'max_length': '500'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['geocal']

# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Blog'
        db.create_table('goblog_blog', (
            ('name', self.gf('django.db.models.fields.SlugField')(max_length=100, primary_key=True)),
            ('title', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('goblog', ['Blog'])

        # Adding model 'Article'
        db.create_table('goblog_article', (
            ('id', self.gf('django.db.models.fields.CharField')(max_length=32, primary_key=True)),
            ('blog', self.gf('django.db.models.fields.related.ForeignKey')(related_name='articles', to=orm['goblog.Blog'])),
            ('author', self.gf('django.db.models.fields.related.ForeignKey')(related_name='+', to=orm['auth.User'])),
            ('title', self.gf('django.db.models.fields.TextField')()),
            ('published', self.gf('django.db.models.fields.DateTimeField')(default=None, null=True, blank=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2012, 5, 26, 0, 0))),
            ('compiler_name', self.gf('django.db.models.fields.CharField')(default='cleanhtml', max_length=255)),
        ))
        db.send_create_signal('goblog', ['Article'])

        # Adding model 'ArticleEdit'
        db.create_table('goblog_articleedit', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('article', self.gf('django.db.models.fields.related.ForeignKey')(related_name='edits', to=orm['goblog.Article'])),
            ('editor', self.gf('django.db.models.fields.related.ForeignKey')(related_name='+', to=orm['auth.User'])),
            ('date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2012, 5, 26, 0, 0))),
        ))
        db.send_create_signal('goblog', ['ArticleEdit'])

        # Adding model 'ArticleContent'
        db.create_table('goblog_articlecontent', (
            ('article', self.gf('django.db.models.fields.related.OneToOneField')(related_name='content', unique=True, primary_key=True, to=orm['goblog.Article'])),
            ('raw', self.gf('django.db.models.fields.TextField')()),
            ('text_start', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('text_end', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal('goblog', ['ArticleContent'])


    def backwards(self, orm):
        # Deleting model 'Blog'
        db.delete_table('goblog_blog')

        # Deleting model 'Article'
        db.delete_table('goblog_article')

        # Deleting model 'ArticleEdit'
        db.delete_table('goblog_articleedit')

        # Deleting model 'ArticleContent'
        db.delete_table('goblog_articlecontent')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'goblog.article': {
            'Meta': {'object_name': 'Article'},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['auth.User']"}),
            'blog': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'articles'", 'to': "orm['goblog.Blog']"}),
            'compiler_name': ('django.db.models.fields.CharField', [], {'default': "'cleanhtml'", 'max_length': '255'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 5, 26, 0, 0)'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '32', 'primary_key': 'True'}),
            'published': ('django.db.models.fields.DateTimeField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.TextField', [], {})
        },
        'goblog.articlecontent': {
            'Meta': {'object_name': 'ArticleContent'},
            'article': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'content'", 'unique': 'True', 'primary_key': 'True', 'to': "orm['goblog.Article']"}),
            'raw': ('django.db.models.fields.TextField', [], {}),
            'text_end': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'text_start': ('django.db.models.fields.TextField', [], {'blank': 'True'})
        },
        'goblog.articleedit': {
            'Meta': {'object_name': 'ArticleEdit'},
            'article': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'edits'", 'to': "orm['goblog.Article']"}),
            'date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 5, 26, 0, 0)'}),
            'editor': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['auth.User']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'goblog.blog': {
            'Meta': {'object_name': 'Blog'},
            'name': ('django.db.models.fields.SlugField', [], {'max_length': '100', 'primary_key': 'True'}),
            'title': ('django.db.models.fields.TextField', [], {})
        }
    }

    complete_apps = ['goblog']
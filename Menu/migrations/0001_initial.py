# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Item'
        db.create_table(u'Menu_item', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=150)),
            ('restaurant', self.gf('django.db.models.fields.CharField')(max_length=35)),
            ('meal', self.gf('django.db.models.fields.CharField')(max_length=35)),
            ('category', self.gf('django.db.models.fields.CharField')(default='n/a', max_length=35)),
            ('month', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('day', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('year', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('calories', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('fat_calories', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('total_fat', self.gf('django.db.models.fields.DecimalField')(default=0.0, max_digits=8, decimal_places=2)),
            ('total_fat_units', self.gf('django.db.models.fields.CharField')(default='n/a', max_length=3)),
            ('total_fat_dv', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('saturated_fat', self.gf('django.db.models.fields.DecimalField')(default=0.0, max_digits=8, decimal_places=2)),
            ('saturated_fat_units', self.gf('django.db.models.fields.CharField')(default='n/a', max_length=3)),
            ('saturated_fat_dv', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('trans_fat', self.gf('django.db.models.fields.DecimalField')(default=0.0, max_digits=8, decimal_places=2)),
            ('trans_fat_units', self.gf('django.db.models.fields.CharField')(default='n/a', max_length=15)),
            ('cholesterol', self.gf('django.db.models.fields.DecimalField')(default=0.0, max_digits=8, decimal_places=2)),
            ('cholesterol_units', self.gf('django.db.models.fields.CharField')(default='n/a', max_length=3)),
            ('cholesterol_dv', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('sodium', self.gf('django.db.models.fields.DecimalField')(default=0.0, max_digits=8, decimal_places=2)),
            ('sodium_units', self.gf('django.db.models.fields.CharField')(default='n/a', max_length=3)),
            ('sodium_dv', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('total_carbs', self.gf('django.db.models.fields.DecimalField')(default=0.0, max_digits=8, decimal_places=2)),
            ('total_carbs_units', self.gf('django.db.models.fields.CharField')(default='n/a', max_length=3)),
            ('total_carbs_dv', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('dietary_fiber', self.gf('django.db.models.fields.DecimalField')(default=0.0, max_digits=8, decimal_places=2)),
            ('dietary_fiber_units', self.gf('django.db.models.fields.CharField')(default='n/a', max_length=3)),
            ('dietary_fiber_dv', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('sugars', self.gf('django.db.models.fields.DecimalField')(default=0.0, max_digits=8, decimal_places=2)),
            ('sugars_units', self.gf('django.db.models.fields.CharField')(default='n/a', max_length=3)),
            ('protein', self.gf('django.db.models.fields.DecimalField')(default=0.0, max_digits=8, decimal_places=2)),
            ('protein_units', self.gf('django.db.models.fields.CharField')(default='n/a', max_length=3)),
            ('vitamin_A_dv', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=8, decimal_places=2)),
            ('vitamin_C_dv', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=8, decimal_places=2)),
            ('calcium_dv', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=8, decimal_places=2)),
            ('iron_dv', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=8, decimal_places=2)),
        ))
        db.send_create_signal(u'Menu', ['Item'])

        # Adding model 'Profile'
        db.create_table(u'Menu_profile', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['auth.User'], unique=True)),
            ('gender', self.gf('django.db.models.fields.CharField')(default='Male', max_length=6)),
            ('age', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('weight', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('height', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('activity_level', self.gf('django.db.models.fields.CharField')(max_length=15)),
            ('weight_goal', self.gf('django.db.models.fields.CharField')(max_length=15)),
            ('calories_limit', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('calories_eaten', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('calories_remaining', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('total_fat_limit', self.gf('django.db.models.fields.DecimalField')(default=65, max_digits=8, decimal_places=2)),
            ('total_fat_eaten', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=8, decimal_places=2)),
            ('total_fat_remaining', self.gf('django.db.models.fields.DecimalField')(default=65, max_digits=8, decimal_places=2)),
            ('total_fat_units', self.gf('django.db.models.fields.CharField')(default='g', max_length=3)),
            ('sodium_limit', self.gf('django.db.models.fields.DecimalField')(default=2300, max_digits=8, decimal_places=2)),
            ('sodium_eaten', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=8, decimal_places=2)),
            ('sodium_remaining', self.gf('django.db.models.fields.DecimalField')(default=2300, max_digits=8, decimal_places=2)),
            ('sodium_units', self.gf('django.db.models.fields.CharField')(default='mg', max_length=3)),
            ('dietary_fiber_limit', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=8, decimal_places=2)),
            ('dietary_fiber_eaten', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=8, decimal_places=2)),
            ('dietary_fiber_remaining', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=8, decimal_places=2)),
            ('dietary_fiber_units', self.gf('django.db.models.fields.CharField')(default='g', max_length=3)),
            ('cholesterol_limit', self.gf('django.db.models.fields.DecimalField')(default=300, max_digits=8, decimal_places=2)),
            ('cholesterol_eaten', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=8, decimal_places=2)),
            ('cholesterol_remaining', self.gf('django.db.models.fields.DecimalField')(default=300, max_digits=8, decimal_places=2)),
            ('cholesterol_units', self.gf('django.db.models.fields.CharField')(default='mg', max_length=3)),
            ('total_carbs_limit', self.gf('django.db.models.fields.DecimalField')(default=130, max_digits=8, decimal_places=2)),
            ('total_carbs_eaten', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=8, decimal_places=2)),
            ('total_carbs_remaining', self.gf('django.db.models.fields.DecimalField')(default=130, max_digits=8, decimal_places=2)),
            ('total_carbs_units', self.gf('django.db.models.fields.CharField')(default='g', max_length=3)),
            ('protein_limit', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=8, decimal_places=2)),
            ('protein_eaten', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=8, decimal_places=2)),
            ('protein_remaining', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=8, decimal_places=2)),
            ('protein_units', self.gf('django.db.models.fields.CharField')(default='g', max_length=3)),
            ('vitamin_A_limit', self.gf('django.db.models.fields.DecimalField')(default=100, max_digits=8, decimal_places=2)),
            ('vitamin_A_eaten', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=8, decimal_places=2)),
            ('vitamin_A_remaining', self.gf('django.db.models.fields.DecimalField')(default=100, max_digits=8, decimal_places=2)),
            ('vitamin_C_limit', self.gf('django.db.models.fields.DecimalField')(default=100, max_digits=8, decimal_places=2)),
            ('vitamin_C_eaten', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=8, decimal_places=2)),
            ('vitamin_C_remaining', self.gf('django.db.models.fields.DecimalField')(default=100, max_digits=8, decimal_places=2)),
            ('calcium_limit', self.gf('django.db.models.fields.DecimalField')(default=100, max_digits=8, decimal_places=2)),
            ('calcium_eaten', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=8, decimal_places=2)),
            ('calcium_remaining', self.gf('django.db.models.fields.DecimalField')(default=100, max_digits=8, decimal_places=2)),
            ('iron_limit', self.gf('django.db.models.fields.DecimalField')(default=100, max_digits=8, decimal_places=2)),
            ('iron_eaten', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=8, decimal_places=2)),
            ('iron_remaining', self.gf('django.db.models.fields.DecimalField')(default=100, max_digits=8, decimal_places=2)),
        ))
        db.send_create_signal(u'Menu', ['Profile'])

        # Adding model 'FoodLog'
        db.create_table(u'Menu_foodlog', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('item', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['Menu.Item'])),
            ('profile', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['Menu.Profile'])),
            ('portion', self.gf('django.db.models.fields.IntegerField')(default=1, blank=True)),
            ('meal', self.gf('django.db.models.fields.CharField')(max_length=9)),
            ('date', self.gf('django.db.models.fields.DateField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'Menu', ['FoodLog'])


    def backwards(self, orm):
        # Deleting model 'Item'
        db.delete_table(u'Menu_item')

        # Deleting model 'Profile'
        db.delete_table(u'Menu_profile')

        # Deleting model 'FoodLog'
        db.delete_table(u'Menu_foodlog')


    models = {
        u'Menu.foodlog': {
            'Meta': {'object_name': 'FoodLog'},
            'date': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'item': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['Menu.Item']"}),
            'meal': ('django.db.models.fields.CharField', [], {'max_length': '9'}),
            'portion': ('django.db.models.fields.IntegerField', [], {'default': '1', 'blank': 'True'}),
            'profile': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['Menu.Profile']"})
        },
        u'Menu.item': {
            'Meta': {'object_name': 'Item'},
            'calcium_dv': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '8', 'decimal_places': '2'}),
            'calories': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'category': ('django.db.models.fields.CharField', [], {'default': "'n/a'", 'max_length': '35'}),
            'cholesterol': ('django.db.models.fields.DecimalField', [], {'default': '0.0', 'max_digits': '8', 'decimal_places': '2'}),
            'cholesterol_dv': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'cholesterol_units': ('django.db.models.fields.CharField', [], {'default': "'n/a'", 'max_length': '3'}),
            'day': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'dietary_fiber': ('django.db.models.fields.DecimalField', [], {'default': '0.0', 'max_digits': '8', 'decimal_places': '2'}),
            'dietary_fiber_dv': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'dietary_fiber_units': ('django.db.models.fields.CharField', [], {'default': "'n/a'", 'max_length': '3'}),
            'fat_calories': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'iron_dv': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '8', 'decimal_places': '2'}),
            'meal': ('django.db.models.fields.CharField', [], {'max_length': '35'}),
            'month': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'protein': ('django.db.models.fields.DecimalField', [], {'default': '0.0', 'max_digits': '8', 'decimal_places': '2'}),
            'protein_units': ('django.db.models.fields.CharField', [], {'default': "'n/a'", 'max_length': '3'}),
            'restaurant': ('django.db.models.fields.CharField', [], {'max_length': '35'}),
            'saturated_fat': ('django.db.models.fields.DecimalField', [], {'default': '0.0', 'max_digits': '8', 'decimal_places': '2'}),
            'saturated_fat_dv': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'saturated_fat_units': ('django.db.models.fields.CharField', [], {'default': "'n/a'", 'max_length': '3'}),
            'sodium': ('django.db.models.fields.DecimalField', [], {'default': '0.0', 'max_digits': '8', 'decimal_places': '2'}),
            'sodium_dv': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'sodium_units': ('django.db.models.fields.CharField', [], {'default': "'n/a'", 'max_length': '3'}),
            'sugars': ('django.db.models.fields.DecimalField', [], {'default': '0.0', 'max_digits': '8', 'decimal_places': '2'}),
            'sugars_units': ('django.db.models.fields.CharField', [], {'default': "'n/a'", 'max_length': '3'}),
            'total_carbs': ('django.db.models.fields.DecimalField', [], {'default': '0.0', 'max_digits': '8', 'decimal_places': '2'}),
            'total_carbs_dv': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'total_carbs_units': ('django.db.models.fields.CharField', [], {'default': "'n/a'", 'max_length': '3'}),
            'total_fat': ('django.db.models.fields.DecimalField', [], {'default': '0.0', 'max_digits': '8', 'decimal_places': '2'}),
            'total_fat_dv': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'total_fat_units': ('django.db.models.fields.CharField', [], {'default': "'n/a'", 'max_length': '3'}),
            'trans_fat': ('django.db.models.fields.DecimalField', [], {'default': '0.0', 'max_digits': '8', 'decimal_places': '2'}),
            'trans_fat_units': ('django.db.models.fields.CharField', [], {'default': "'n/a'", 'max_length': '15'}),
            'vitamin_A_dv': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '8', 'decimal_places': '2'}),
            'vitamin_C_dv': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '8', 'decimal_places': '2'}),
            'year': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        u'Menu.profile': {
            'Meta': {'object_name': 'Profile'},
            'activity_level': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'age': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'calcium_eaten': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '8', 'decimal_places': '2'}),
            'calcium_limit': ('django.db.models.fields.DecimalField', [], {'default': '100', 'max_digits': '8', 'decimal_places': '2'}),
            'calcium_remaining': ('django.db.models.fields.DecimalField', [], {'default': '100', 'max_digits': '8', 'decimal_places': '2'}),
            'calories_eaten': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'calories_limit': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'calories_remaining': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'cholesterol_eaten': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '8', 'decimal_places': '2'}),
            'cholesterol_limit': ('django.db.models.fields.DecimalField', [], {'default': '300', 'max_digits': '8', 'decimal_places': '2'}),
            'cholesterol_remaining': ('django.db.models.fields.DecimalField', [], {'default': '300', 'max_digits': '8', 'decimal_places': '2'}),
            'cholesterol_units': ('django.db.models.fields.CharField', [], {'default': "'mg'", 'max_length': '3'}),
            'dietary_fiber_eaten': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '8', 'decimal_places': '2'}),
            'dietary_fiber_limit': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '8', 'decimal_places': '2'}),
            'dietary_fiber_remaining': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '8', 'decimal_places': '2'}),
            'dietary_fiber_units': ('django.db.models.fields.CharField', [], {'default': "'g'", 'max_length': '3'}),
            'gender': ('django.db.models.fields.CharField', [], {'default': "'Male'", 'max_length': '6'}),
            'height': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'iron_eaten': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '8', 'decimal_places': '2'}),
            'iron_limit': ('django.db.models.fields.DecimalField', [], {'default': '100', 'max_digits': '8', 'decimal_places': '2'}),
            'iron_remaining': ('django.db.models.fields.DecimalField', [], {'default': '100', 'max_digits': '8', 'decimal_places': '2'}),
            'items': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['Menu.Item']", 'symmetrical': 'False', 'through': u"orm['Menu.FoodLog']", 'blank': 'True'}),
            'protein_eaten': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '8', 'decimal_places': '2'}),
            'protein_limit': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '8', 'decimal_places': '2'}),
            'protein_remaining': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '8', 'decimal_places': '2'}),
            'protein_units': ('django.db.models.fields.CharField', [], {'default': "'g'", 'max_length': '3'}),
            'sodium_eaten': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '8', 'decimal_places': '2'}),
            'sodium_limit': ('django.db.models.fields.DecimalField', [], {'default': '2300', 'max_digits': '8', 'decimal_places': '2'}),
            'sodium_remaining': ('django.db.models.fields.DecimalField', [], {'default': '2300', 'max_digits': '8', 'decimal_places': '2'}),
            'sodium_units': ('django.db.models.fields.CharField', [], {'default': "'mg'", 'max_length': '3'}),
            'total_carbs_eaten': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '8', 'decimal_places': '2'}),
            'total_carbs_limit': ('django.db.models.fields.DecimalField', [], {'default': '130', 'max_digits': '8', 'decimal_places': '2'}),
            'total_carbs_remaining': ('django.db.models.fields.DecimalField', [], {'default': '130', 'max_digits': '8', 'decimal_places': '2'}),
            'total_carbs_units': ('django.db.models.fields.CharField', [], {'default': "'g'", 'max_length': '3'}),
            'total_fat_eaten': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '8', 'decimal_places': '2'}),
            'total_fat_limit': ('django.db.models.fields.DecimalField', [], {'default': '65', 'max_digits': '8', 'decimal_places': '2'}),
            'total_fat_remaining': ('django.db.models.fields.DecimalField', [], {'default': '65', 'max_digits': '8', 'decimal_places': '2'}),
            'total_fat_units': ('django.db.models.fields.CharField', [], {'default': "'g'", 'max_length': '3'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['auth.User']", 'unique': 'True'}),
            'vitamin_A_eaten': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '8', 'decimal_places': '2'}),
            'vitamin_A_limit': ('django.db.models.fields.DecimalField', [], {'default': '100', 'max_digits': '8', 'decimal_places': '2'}),
            'vitamin_A_remaining': ('django.db.models.fields.DecimalField', [], {'default': '100', 'max_digits': '8', 'decimal_places': '2'}),
            'vitamin_C_eaten': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '8', 'decimal_places': '2'}),
            'vitamin_C_limit': ('django.db.models.fields.DecimalField', [], {'default': '100', 'max_digits': '8', 'decimal_places': '2'}),
            'vitamin_C_remaining': ('django.db.models.fields.DecimalField', [], {'default': '100', 'max_digits': '8', 'decimal_places': '2'}),
            'weight': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'weight_goal': ('django.db.models.fields.CharField', [], {'max_length': '15'})
        },
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
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
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
        }
    }

    complete_apps = ['Menu']
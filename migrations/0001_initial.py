# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AclList',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('deny_value', models.BooleanField(default=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='AclRule',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('acl_type', models.CharField(default=b'foobar', max_length=200)),
                ('acl_values', jsonfield.fields.JSONField(default=b'NULL')),
                ('acl_name', models.CharField(default=b'foobar', max_length=200)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='acllist',
            name='acl_rules',
            field=models.ManyToManyField(to='api_squid.AclRule'),
            preserve_default=True,
        ),
    ]

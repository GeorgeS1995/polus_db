# Generated by Django 2.2.3 on 2019-09-26 19:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='type_of_operation',
            name='department_id',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.DO_NOTHING, to='mainapp.Department'),
            preserve_default=False,
        ),
    ]

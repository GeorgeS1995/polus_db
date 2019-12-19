# Generated by Django 2.2.3 on 2019-09-26 18:53

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Characteristic_of_product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=255)),
                ('units', models.CharField(max_length=255)),
                ('description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Employess',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Operation_history',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateTimeField(auto_now_add=True)),
                ('end_date', models.DateTimeField(auto_now_add=True)),
                ('employess_id', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='mainapp.Employess')),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('serial_number', models.CharField(max_length=255)),
                ('Assembly', models.ManyToManyField(to='mainapp.Product')),
            ],
        ),
        migrations.CreateModel(
            name='Type_of_defect',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Type_of_operation_groups',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Type_of_product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('model', models.CharField(max_length=255)),
                ('department_id', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='mainapp.Department')),
            ],
        ),
        migrations.CreateModel(
            name='Type_of_operation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=255)),
                ('type_of_operation_groups_id', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='mainapp.Type_of_operation_groups')),
            ],
        ),
        migrations.CreateModel(
            name='Rang',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=255)),
                ('department_id', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='mainapp.Department')),
            ],
        ),
        migrations.CreateModel(
            name='Product_2_characteristic',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.CharField(max_length=255)),
                ('characteristic_of_product_id', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='mainapp.Characteristic_of_product')),
                ('operation_history_id', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='mainapp.Operation_history')),
                ('product_id', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='mainapp.Product')),
            ],
        ),
        migrations.AddField(
            model_name='product',
            name='type_of_product_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='mainapp.Type_of_product'),
        ),
        migrations.AddField(
            model_name='operation_history',
            name='type_of_defect_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='mainapp.Type_of_defect'),
        ),
        migrations.AddField(
            model_name='operation_history',
            name='type_of_operation_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='mainapp.Type_of_operation'),
        ),
        migrations.AddField(
            model_name='employess',
            name='rang_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='mainapp.Rang'),
        ),
        migrations.AddField(
            model_name='employess',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='characteristic_of_product',
            name='type_of_product_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='mainapp.Type_of_product'),
        ),
    ]

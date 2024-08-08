# Generated by Django 5.0.7 on 2024-08-06 11:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('texnomart', '0003_attribute_attributevalue_alter_product_category_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='attribute',
            old_name='attribute_name',
            new_name='key',
        ),
        migrations.RemoveField(
            model_name='attributevalue',
            name='attribute_value',
        ),
        migrations.AddField(
            model_name='attributevalue',
            name='value',
            field=models.CharField(default=21, max_length=100),
            preserve_default=False,
        ),
    ]

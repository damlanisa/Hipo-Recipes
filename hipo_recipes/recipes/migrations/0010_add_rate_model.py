# Generated by Django 3.0.4 on 2020-03-17 11:03

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0009_rename_recipe_fields'),
    ]

    operations = [
        migrations.RenameField(
            model_name='rate',
            old_name='rate',
            new_name='points',
        ),
        migrations.AddField(
            model_name='rate',
            name='date',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='recipe',
            name='rate_count',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='recipe',
            name='rate_points',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='rate',
            name='recipe',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rates', to='recipes.Recipe'),
        ),
    ]
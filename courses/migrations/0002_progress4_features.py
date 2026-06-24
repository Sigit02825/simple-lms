# Generated manually for Progress 4 advanced features

import django.db.models.constraints
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='completion_count',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='course',
            name='enrollment_count',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='coursemember',
            name='certificate_path',
            field=models.CharField(blank=True, default='', max_length=255),
        ),
        migrations.AddField(
            model_name='coursemember',
            name='completed_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddIndex(
            model_name='course',
            index=models.Index(fields=['name'], name='idx_course_name'),
        ),
        migrations.AddConstraint(
            model_name='coursemember',
            constraint=models.UniqueConstraint(
                fields=('course_id', 'user_id'),
                name='unique_course_member',
            ),
        ),
    ]

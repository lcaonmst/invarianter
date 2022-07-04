from django.contrib import admin

# Register your models here.

from django.apps import apps

app = apps.get_app_config('invarianterC')

for model_name, model in app.models.items():
    if model_name != 'section':
        admin.site.register(model)
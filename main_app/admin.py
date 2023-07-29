from django.contrib import admin
from .models import Game, Profile, File, Review

# add database models to admin portal
admin.site.register(Game)
admin.site.register(Profile)
admin.site.register(Review)
admin.site.register(File)

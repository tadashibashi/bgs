"""
    Custom forms for main_app
"""
from django.forms import ModelForm

from .models import Game


class GameForm(ModelForm):
    class Meta:
        model = Game
        fields = ["title", "description", "tags", "frame_width", "frame_height"]
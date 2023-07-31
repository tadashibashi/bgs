"""
    Custom forms for main_app
"""
from django.forms import ModelForm, FileField
from .models import Game

class GameForm(ModelForm):
    game = FileField()
    class Meta:
        model = Game
        fields = ["title", "description", "tags", "frame_width", "frame_height"]
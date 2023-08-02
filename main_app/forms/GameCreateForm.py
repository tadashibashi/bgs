from django import forms

from ..models import Game
from .TagsField import TagsField


class GameCreateForm(forms.ModelForm):
    """
        Form to create and edit games
    """
    # game = forms.FileField(widget=forms.FileInput(attrs={"accept": ".zip"}))
    tags = TagsField(required=False) #ArrayField(CharField(), size=4)


    class Meta:
        model = Game
        fields = ["title", "description", "tags", "frame_width", "frame_height", "url"]

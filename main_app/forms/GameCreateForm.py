from django import forms

from ..models import Game
from .TagsField import TagsField

class CheckboxField(forms.BooleanField):
    widget=forms.CheckboxInput(attrs={"class": "form-check-input ms-2"})
    required=False

class GameCreateForm(forms.ModelForm):
    """
        Form to create and edit games
    """
    # game = forms.FileField(widget=forms.FileInput(attrs={"accept": ".zip"}))
    tags = TagsField(required=False) #ArrayField(CharField(), size=4)
    tags.widget.attrs.update({"placholder": "no tags"})

    add_fullscreen_btn = CheckboxField(label="Add fullscreen button?")

    is_published = CheckboxField(label="Publish")

    class Meta:
        model = Game
        fields = ["title", "description", "tags", "frame_width", "frame_height",
                  "add_fullscreen_btn", "url", "is_published"]

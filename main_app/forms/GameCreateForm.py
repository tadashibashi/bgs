from django import forms
from django.forms import FileField

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
    tags = TagsField(required=False)
    tags.widget.attrs.update({"placholder": "no tags"})

    add_fullscreen_btn = CheckboxField(label="Add fullscreen button?", required=False)

    is_published = CheckboxField(label="Publish", required=False)

    screenshot = FileField(required=False)

    class Meta:
        model = Game
        fields = ["title", "description", "tags", "frame_width", "frame_height",
                  "add_fullscreen_btn", "url", "is_published"]

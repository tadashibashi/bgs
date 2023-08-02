from django import forms

from ..models import Game
from .TagsField import TagsField


class GameCreateForm(forms.ModelForm):
    """
        Form to create and edit games
    """
    # game = forms.FileField(widget=forms.FileInput(attrs={"accept": ".zip"}))
    tags = TagsField(required=False) #ArrayField(CharField(), size=4)
    tags.widget.attrs.update({"placholder": "no tags"})

    add_fullscreen_btn = forms.BooleanField(label="Add fullscreen button?", required=False,
                                            widget=forms.CheckboxInput(attrs={"class": "form-check-input ms-2"}))

    class Meta:
        model = Game
        fields = ["title", "description", "tags", "frame_width", "frame_height", "add_fullscreen_btn", "url"]

from django import forms

from django.forms import FileField, CharField, Textarea

from ..models import Game
from .fields import TagsField
from .fields import CheckboxField


class GameForm(forms.ModelForm):
    """
        Form to edit games
    """

    description = CharField(widget=Textarea(attrs={"rows": "10"}), required=False)

    tags = TagsField(required=False)
    tags.widget.attrs.update({"placholder": "no tags"})

    add_fullscreen_btn = CheckboxField(label="Add fullscreen button?", required=False)
    is_published = CheckboxField(label="Publish", required=False)

    screenshot = FileField(required=False)


    class Meta:
        model = Game
        fields = ["title", "description", "tags", "frame_width", "frame_height",
                  "add_fullscreen_btn", "is_published"]

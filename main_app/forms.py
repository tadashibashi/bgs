"""
    Custom forms for main_app
"""
from django.core.exceptions import ValidationError
from django.db.models import QuerySet
from django import forms

from .models import Game, Tag


class TagsField(forms.CharField):
    def to_python(self, value: str) -> QuerySet:
        """Normalize data to a list of  strings, create a tag if it doesn't exist"""
        if not value or not value.strip():
            return Tag.objects.none()
        tag_strs = [val.strip() for val in value.split("\xa0")]
        tag_ids = []
        for tag_str in tag_strs:
            if not tag_str: continue

            new_tag = Tag.objects.get_or_create(text=tag_str)
            tag_ids.append(new_tag[0].id)
        return Tag.objects.filter(id__in=tag_ids)

    def validate(self, value):
        """Make sure valid tag instances were received"""
        super().validate(value)
        if not isinstance(value, QuerySet):
            raise ValidationError("Invalid value: %(value)",
                                  params={"value": value})

    def clean(self, value):
        res = self.to_python(value)
        self.validate(res)
        return res



class GameForm(forms.ModelForm):
    game = forms.FileField(widget=forms.FileInput(attrs={"accept": ".zip"}))
    tags = TagsField(required=False) #ArrayField(CharField(), size=4)
    class Meta:
        model = Game
        fields = ["title", "description", "tags", "frame_width", "frame_height"]

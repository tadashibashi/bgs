"""
    Contains custom form field for game tags
"""
from django.core.exceptions import ValidationError
from django.db.models import QuerySet
from django import forms
from django.template.defaultfilters import slugify

from ..models import Tag

class TagsWidget(forms.TextInput):
    """
        Text field for tags, makes sure to include the corresponding css/js
        for custom writable div frontend behavior
    """

    input_type = "text"
    is_required = False

    class Media:
        css = {
            "all": ["/static/css/widgets/TagsWidget.css"]
        }
        js = ["/static/js/widgets/TagsWidget.js"]


class TagsField(forms.Field):
    """
        A CharField that converts space-separated tags into
        Tags for a Game.
    """

    widget = TagsWidget

    def to_python(self, value: str) -> QuerySet:
        """
            Converts input string of space separated tag strings
            to a QuerySet of Tag models.
            Create Tags in the database if any do not exist
        """

        # Return an empty QuerySet if there is no tag data
        if not value or not value.strip():
            return Tag.objects.none()

        # Parse strings into Tags
        #    the implementation on the frontend separates tags with "\xa0",
        #    which is just a non-linebreaking space.
        tag_strs = [slugify(val.strip().lower()) for val in value.split("\xa0")]
        tag_ids = []
        for tag_str in tag_strs:
            # don't parse blank tags from any trailing spaces
            if not tag_str: continue

            # create tags
            new_tag = Tag.objects.get_or_create(text=tag_str)
            tag_ids.append(new_tag[0].id)

        # return a query with all tags
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

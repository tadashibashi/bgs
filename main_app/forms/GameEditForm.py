from .GameForm import GameForm

from django.forms import forms, widgets

class GameEditForm(GameForm):
    """
        Form to edit games
    """
    zip_upload = forms.FileField(widget=widgets.FileInput(attrs={"accept": ".zip"}), required=False)

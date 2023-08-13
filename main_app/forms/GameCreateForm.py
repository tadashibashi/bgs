from django.forms import forms, widgets

from .GameForm import GameForm

class GameCreateForm(GameForm):
    """
        Form to edit games
    """
    zip_upload = forms.FileField(widget=widgets.FileInput(attrs={"accept": ".zip"}), required=True)
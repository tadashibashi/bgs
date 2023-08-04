from django import forms
from django.contrib.postgres.forms import SimpleArrayField

class ProfileForm(forms.Form):


    username = forms.CharField()
    """
        User's username, used to log-in
        Must be unique. Required.
    """


    display_name = forms.CharField()
    """
        Outward facing name that will appear on profile, reviews, etc.
        Required.
    """


    email = forms.EmailField()
    """
        User's email address for validation, notifications, etc.
        Must be unique. Required.
    """


    password = forms.PasswordInput()
    """
        User's password for log-in validation.
        Optional. Leave blank to keep old password.
    """


    confirm_password = forms.PasswordInput()
    """
        Confirm password, must match with password to validate successfully.  
    """


    avatar = forms.FileField(label="Profile picture", required=False)
    """
        Set when the user wants to override their current avatar image.
    """


    bio = forms.CharField(widget=forms.Textarea, required=False)
    """
        Text area for user bio / about me.
    """


    social_links = SimpleArrayField(forms.URLField(), required=False)
    """
        List of social links.
    """

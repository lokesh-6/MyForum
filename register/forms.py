from django import forms
from posts.models import Author

class UpdateForm(forms.ModelForm):

    class Meta:
        model=Author
        fields=("fullname","bio")
from django.forms import TextInput
from django.forms.models import ModelForm

from .models import Project


class ProjectForm(ModelForm):
    """
    From to add a Project
    """

    class Meta:
        model = Project
        fields = ('name', 'teaser', 'wikiPage', 'finished_at')
        widgets = {
            'teaser': TextInput,
        }

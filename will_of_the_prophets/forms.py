from django import forms

from will_of_the_prophets.models import Roll

class RollForm(forms.ModelForm):
    
    embargo = forms.SplitDateTimeField()

    class Meta:
        model = Roll
        fields = ['embargo']

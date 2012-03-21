import django.forms as forms


class DateTimeCombiWidget(forms.MultiWidget):
    """
    A newform widget, which provides a seperate input tag for
    date and time, the output is merged again
    """

    def __init__(self, attrs=None):
        widgets = (forms.TextInput(attrs={'class': 'vDateField'}),
                   forms.TextInput(attrs={'class': 'vTimeField'}))
        super(DateTimeCombiWidget, self).__init__(widgets, attrs)

    def decompress(self, value):
        
        if value:
            return [value.date(), value.time()]
        return ['', '']

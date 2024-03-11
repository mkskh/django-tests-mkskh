from django import forms


class SearchForm(forms.Form):
    search_term = forms.CharField(label='Search Term', max_length=200)
    section = forms.ChoiceField(label='Section', required=False, choices=[
        ('', 'All Sections'), 
        ('Web Frameworks', 'Web Frameworks'),
        ('Setting up Django', 'Setting up Django'), 
        ('URL Mapping', 'URL Mapping')
    ])


class NoteForm(forms.Form):
    section = forms.ChoiceField(label='Section', required=False, choices=[
        ('', 'Any'), 
        ('Web Frameworks', 'Web Frameworks'),
        ('Setting up Django', 'Setting up Django'), 
        ('URL Mapping', 'URL Mapping')
    ])
    text  = forms.CharField(widget=forms.Textarea)


class EditNoteForm(forms.Form):
    section = forms.ChoiceField(label='Section', required=False, choices=[
        ('', 'Any'), 
        ('Web Frameworks', 'Web Frameworks'),
        ('Setting up Django', 'Setting up Django'), 
        ('URL Mapping', 'URL Mapping')
        ], disabled=True)
    text  = forms.CharField(widget=forms.Textarea)
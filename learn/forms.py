from django import forms
import datetime

from .models import Dutch, English, Translation, TranslationGroup

class DutchForm(forms.ModelForm):
    class Meta:
        model = Dutch
        fields = ['value']#,'creation_date'] # might be better to avoid
        widgets = {
                'value' : forms.TextInput(attrs={
                    'size' : 50,
                    'title' : 'Dutch term',
                    'placeholder' : 'Dutch translation/word',
                    'required' : 'False',
                    }),
#                'creation_date' : forms.DateTimeInput(attrs={
#                    'type' : 'datetime-local',
#                    'class' : 'form-control'},
#                    format='%y-%m-%dT%H:%M'),
                }
        labels = {
                'value' : ('Dutch term'),
#                'creation_date' : ('Created at'),
                }

class EnglishForm(forms.ModelForm):
    class Meta:
        model = English
        fields = ['value']#,'creation_date'] #might be better to avoid
        widgets = {
                'value' : forms.TextInput(attrs={
                    'size' : 50,
                    'title' : 'English term',
                    'placeholder' : 'English translation/word',
                    'required' : 'False',
                    }),
                # inclusion of the creation date form
#                'creation_date' : forms.DateTimeInput(attrs={
#                    'type' : 'datetime-local',
#                    'class' : 'form-control'},
#                    format='%y-%m-%dT%H:%M'),
                }
        labels = {
                'value' : ('English term'),
#                'creation_date' : ('Created at'),
                }

class TranslationGroupForm(forms.ModelForm):
    class Meta:
        model = TranslationGroup
        fields = ['groupName']
        widgets = {
                'groupName' : forms.TextInput(attrs={
                    'size' : 50,
                    'title' : 'English term',
                    'placeholder' : 'group',
                    'required' : 'False',
                    }),
                }
        labels = {
               'groupName' : ('Category for Translation'),
               }

class TranslationListForm(forms.Form):
    translation_list = forms.ModelMultipleChoiceField(
            widget=forms.CheckboxSelectMultiple(),
            queryset=TranslationGroup.objects.all(),
            to_field_name="groupName",
            initial=0,
            required=False,
            )

class TranslationsForm(forms.Form):
    translations = forms.ModelMultipleChoiceField(
            widget=forms.CheckboxSelectMultiple(),
            queryset=Translation.objects.all(),
            to_field_name="translation_key",
            initial=0,
            required=False,
            )


# TODO Ultimately it would be nice to modify the deletion form
# scrolling through all the entries is not feasible, sorting
# a menu item would be better
#class TranslationsForm(forms.ModelForm):
#    class Meta:
#        model = Translation
#        exclude = ('english','dutch')
#    def __init__(self,grp=None,**kwargs):
#        super(TranslationsForm,self).__init__(**kwargs)
#        if isinstance(grp,TranslationGroup):
#            self.fields['translation_group'].queryset = Translation.objects.filter(translation_group=grp)
#        else:
#            self.fields['translation_group'].queryset = Translation.objects.all()


class DateForm(forms.Form):
    date = forms.DateField(
            label='Starting from ...',
            widget=forms.DateInput(attrs={ 
                'type' : 'date',
                'class' : 'form-control',
                },
                format='%d/%m/%d',
            ),
            required=False
        )

class TextForm(forms.Form):
    check = forms.CharField(
            widget=forms.TextInput(attrs={
                'size' : '50',
                'placeholder' : 'write your response here',
                'required' : 'False',
                'autocomplete' : 'off',
                }),
            required=False
            )

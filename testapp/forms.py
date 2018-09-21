from django import forms
import pandas as pd
import numpy as np
from multiselectfield import MultiSelectField
from .models import EnrollmentApplication,VizInfoModel

from django import forms

class UploadFileForm(forms.Form):
    title = forms.CharField(max_length=50)
    file = forms.FileField()


class VizInfoForm(forms.ModelForm):

    class Meta:
        model = VizInfoModel
        fields = '__all__'

    def __init__(self,choice,*args,**kwargs):
        super(VizInfoForm, self).__init__(*args,**kwargs)
        print("Choice")
        print(choice)
        self.fields['tog'].choices = choice
        #self.fields['vis'].choices = choice


class CountryForm(forms.ModelForm):
    class Meta:
        model = EnrollmentApplication
        fields = [
            'reasons_for_childcare',
        ]
    def __init__(self,choice,*args,**kwargs):
        super(CountryForm, self).__init__(*args,**kwargs)
        self.fields['reasons_for_childcare'].choices = choice

class CountryForm2(forms.Form):
    OPTIONS = (
         ("abc","abc"),
         ("abc", "abc"),
    )
    CHILDCARE_REASONS1 = (('Working', 'working'), ('Training', 'training'), ('Teen Parent', 'teen_parent'),
                         ('Working W/Child With A Disability', 'child_disability'),
                         ('Adult W/Disability', 'adult_disability'))
    CHILDCARE_REASONS = (('working', 'Working'),
                         ('training', 'Training'),
                         ('teen_parent', 'Teen Parent'),
                         ('child_disability', 'Working W/Child With A Disability'),
                         ('adult_disability', 'Adult W/Disability'))
    df = pd.DataFrame({'a': ['AUT', 'DEU', 'NLD', 'IND', 'JPN', 'CHN'],
                       'b': ['Austria', 'Germany', 'Netherland', 'India', 'Japan', 'China']})
    lstOptions = str(df.values.tolist())
    strOptions = (str(lstOptions).replace('[', '(')).replace(']', ')')
    print("options")
    print(OPTIONS)
    print("strOptions")
    print(strOptions)
    Countries = MultiSelectField(choices=CHILDCARE_REASONS)

class CountryFormold(forms.Form):
    def __init__(self, *args, **kwargs):
        super(CountryForm, self).__init__(*args, **kwargs)
        self.fields['my_choice_field'] = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple,choices=get_my_choices() )

class CountryFormold1(forms.Form):

    def __init__(self, *args, **kwargs):
        dict = get_my_choices()
        print (dict)
        super(CountryForm, self).__init__(*args, **kwargs)

    OPTIONS = (
        (dict.keys, dict.values),
        ("abc","abc"),
    )
    #print("options")
    #print(OPTIONS)
    Countries = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple,choices=OPTIONS)

class CountryFormold(forms.Form):
    def __init__(self, *args, **kwargs):
        super(CountryForm, self).__init__(*args, **kwargs)
        self.fields['my_choice_field'] = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple,choices=get_my_choices() )

#
# def get_my_choices():
#     df = pd.DataFrame({'a': ['AUT', 'DEU', 'NLD', 'IND', 'JPN', 'CHN'],
#                        'b': ['Austria', 'Germany', 'Netherland', 'India', 'Japan', 'China']})
#     lstOptions = str(df.values.tolist())
#     strOptions = (str(lstOptions).replace('[', '(')).replace(']]', '),)').replace('],', '),')
#     #print("df")
#     #print(df)
#     #return df

class CountryForm1(forms.Form):
  OPTIONS = (
            ("AUT", "Austria"),
            ("DEU", "Germany"),
            ("NLD", "Neitherlands"),
        )
  Countries = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, choices=OPTIONS)


def get_my_choices():
    choices_list=["abc"]
    return choices_list

class CountryFormold(forms.Form):
    def __init__(self, *args, **kwargs):
        super(CountryForm, self).__init__(*args, **kwargs)
        self.fields['my_choice_field'] = MultiSelectField(choices=get_my_choices())

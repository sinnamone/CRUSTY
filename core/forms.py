from django import forms
import uuid


class ContactForms(forms.Form):
    AnalysisID = forms.CharField(label="Analysis ID",
                                 initial=uuid.uuid1(),
                                 widget=forms.TextInput(attrs={'readonly':'True'}))
    AnalysisName = forms.CharField(label="Analysis Name",
                                   max_length=100,
                                   help_text="Please insert Analysis Name, max length 100 characters",
                                   initial="e.g PBMC dataset",
                                   error_messages={'required': 'Please enter Analysis Name'})
    email = forms.EmailField(label="E-Mail",
                             help_text="Please insert a valid E-mail address",
                             error_messages={'required': 'Please enter a valid E-mail address'}
                             )
    kvalue = forms.IntegerField(max_value=1000,
                                min_value=15,
                                label="K-value",
                                initial=30,
                                help_text="Please insert a K-value for nearest neighbors search",)
    clusteringtype = forms.ChoiceField(choices=(('Phenograph','Phenograph'),('Parc','Parc')),
                                       )



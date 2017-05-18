# -*- coding: utf-8 -*-
from django import forms

from bandnames.names.models import NewBand, ReportBand


class ReportBandForm(forms.ModelForm):
    reason = forms.CharField(
        label='Reason (how did they actually get their name?)  *',
        widget=forms.Textarea(attrs={
            'class': 'mdl-textfield__input',
            'rows': '7',
        })
    )
    source = forms.CharField(
        label='Source (URL)  *',
        widget=forms.TextInput(attrs={
            'class': 'mdl-textfield__input',
        })
    )
    reporter_name = forms.CharField(
        label='Your Name / Alias',
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'mdl-textfield__input',
        })
    )
    reporter_email = forms.EmailField(
        label='Your Email (in case we need to get in touch)',
        required=False,
        widget=forms.EmailInput(attrs={
            'class': 'mdl-textfield__input',
        })
    )

    class Meta:
        model = ReportBand
        exclude = ['band']


class NewBandForm(forms.ModelForm):
    name = forms.CharField(
        label='The bands name  *',
        widget=forms.TextInput(attrs={
            'class': 'mdl-textfield__input',
        })
    )
    reason = forms.CharField(
        label='Reason (how did they get their name?)  *',
        widget=forms.Textarea(attrs={
            'class': 'mdl-textfield__input',
            'rows': '7',
        })
    )
    source = forms.CharField(
        label='Source (URL)  *',
        widget=forms.TextInput(attrs={
            'class': 'mdl-textfield__input',
        })
    )
    submitter_name = forms.CharField(
        label='Your Name / Alias (so you can get credit)',
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'mdl-textfield__input',
        })
    )
    submitter_email = forms.EmailField(
        label='Your Email (so we can notify you when it\' approved)',
        required=False,
        widget=forms.EmailInput(attrs={
            'class': 'mdl-textfield__input',
        })
    )

    class Meta:
        model = NewBand

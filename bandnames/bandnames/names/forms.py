# -*- coding: utf-8 -*-
from django import forms

from bandnames.names.models import NewBand, ReportBand


class ReportBandForm(forms.ModelForm):
    reason = forms.CharField(widget=forms.Textarea)
    source = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'A link of proof will help us varify'
    }))
    reporter_name = forms.CharField(
        label='Name / Alias',
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': '(Optional) So we can give you all the credit'
        })
    )
    reporter_email = forms.CharField(
        label='Email',
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': '(Optional) In case we need to get in touch'
        })
    )

    class Meta:
        model = ReportBand
        exclude = ['band']


class NewBandForm(forms.ModelForm):
    name = forms.CharField(label='Band Name')
    reason = forms.CharField(widget=forms.Textarea)
    source = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'A link of proof will help us varify'
    }))
    submitter_name = forms.CharField(
        label='Name / Alias',
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': '(Optional) So we can give you all the credit'
        })
    )
    submitter_email = forms.CharField(
        label='Email',
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': '(Optional) In case we need to get in touch'
        })
    )

    class Meta:
        model = NewBand

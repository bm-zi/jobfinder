from typing import ValuesView
from bs4.element import Stylesheet
from django import forms
from django.db.models import fields
from django.forms.forms import Form
from django.forms.widgets import HiddenInput
from django.shortcuts import redirect
from .models import Job, JobSearchFilter
from ckeditor.widgets import CKEditorWidget



class SaveJobForm(forms.ModelForm):
    """ Creates a Form class from Django model, customization of 
        generated fields by this calss is done by class Meta. """

    title = forms.CharField(label='',
        widget=forms.TextInput(
            attrs={'placeholder': 'job title', 'style':"width:50%",
                    'class':'form-control'}),
    )

    link = forms.CharField(label='',
            widget=forms.TextInput(
                attrs={'placeholder': 'job url', 'style':"width:50%",
                        'class':'form-control'})
    )

    # description = forms.CharField(label='',
    #     widget=forms.Textarea(
    #         attrs={'placeholder': 'job description', 'rows': 5,
    #         'class':'form-control'})
    # )

    description = forms.CharField(label='', 
                        widget=CKEditorWidget('default'))

    is_applied = forms.BooleanField(required=False, label='applied',
                widget=forms.CheckboxInput
            )

    class Meta:
        model = Job
        fields = ['title', 'link', 'description', 'is_applied']

    def clean_content(self):
        description = self.clean_content.get("description")

        if len(description) > 100:
            raise forms.ValidationError('Description is too long.')
        return description


class SearchFilterForm(forms.ModelForm):

    search_filter_name = forms.CharField(label='',
        widget=forms.TextInput(
            attrs={'placeholder': 'search name', 
                    'class':'form-control', 'size':'50'})
        )

    with_all_of_these_words = forms.CharField(label='',
        required=False,
        widget=forms.TextInput(
            attrs={'placeholder': 'with all of these words', 
                    'class':'form-control'})
        )

    with_the_exact_phrase = forms.CharField(label='', required=False,
        widget=forms.TextInput(
            attrs={'placeholder': 'with the exact phrase', 
                    'class':'form-control'})
        )

    with_at_least_one_of_these_words = forms.CharField(label='', 
        required=False,
        widget=forms.TextInput(
            attrs={'placeholder': 'with at least one of these words', 
                    'class':'form-control'})
        )

    with_none_of_these_words = forms.CharField(label='', 
        required=False,
        widget=forms.TextInput(
            attrs={'placeholder': 'with none of these words', 
                    'class':'form-control'})
        )

    with_these_words_in_the_title = forms.CharField(label='', 
        required=False,
        widget=forms.TextInput( 
            attrs={'placeholder': 'with these words in the title', 
                    'class':'form-control'})
       )

    from_this_company = forms.CharField(label='', required=False,
        widget=forms.TextInput(
            attrs={'placeholder': 'from this company',
                    'class':'form-control'}),
        )

    class Meta:
        model = JobSearchFilter
        fields = [
            'search_filter_name',
            'with_all_of_these_words',
            'with_the_exact_phrase',
            'with_at_least_one_of_these_words',
            'with_none_of_these_words',
            'with_these_words_in_the_title',
            'from_this_company',
        ]

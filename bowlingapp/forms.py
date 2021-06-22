from django import forms
from django.shortcuts import render
from django.forms import widgets
from .models import CoreModel, MemberModel

class SpendingForm(forms.Form):
    member_list = forms.ModelChoiceField(
        label="Member",
        queryset=MemberModel.objects.all(),
        widget=forms.RadioSelect,
        empty_label=None,
    )
    class Meta:
        teams = (('A','A'),('B','B'),('C','C'))
        model = CoreModel
        fields = ('member_list', 'raund', 'score', 'point_alloc', 'team_choice','pin', 'handicap')
        widgets = {
            'raund': forms.IntegerField(),
            'score': forms.IntegerField(),
            'team_choice': forms.CharField(),
            'pin': forms.IntegerField(),
            'handicap' : forms.CharField(),
        }
    

    
    
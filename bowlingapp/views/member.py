from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.utils.timezone import localtime
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.db.models import Avg, Max, Min
from django.views import generic
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView
from ..models import CoreModel, MemberModel, GameModel, CoreModel, TeamCalculusModel, EachGameDataModel
from ..forms import SpendingForm

class MemberList(ListView, LoginRequiredMixin):
    template_name = 'member_list.html'
    model = MemberModel

@login_required
def memberlistview(request):
    object = MemberModel.objects.filter(user_set=request.user)
    if request.method == 'POST':    # フォームでデータが送られてきたら
        context = {}
        if 'high_point' in request.POST:
            context["object"] = MemberModel.objects.filter(user_set=request.user).order_by('-point_total')
        elif 'high_average' in request.POST:
            context["object"] = MemberModel.objects.filter(user_set=request.user).order_by('-ave')
        elif 'high_max' in request.POST:
            context["object"] = MemberModel.objects.filter(user_set=request.user).order_by('-max')
        elif 'high_min' in request.POST:
            context["object"]= MemberModel.objects.filter(user_set=request.user).order_by('-min')
        return render(request, 'member_list.html', context)
    return render(request, 'member_list.html', {'object':object})

class MemberCreate(CreateView, LoginRequiredMixin):
    template_name = 'member_add.html'
    model = MemberModel
    fields = ('membername', 'user_set')
    success_url = reverse_lazy('member_list')

class MemberDetail(DetailView, LoginRequiredMixin):
    template_name = 'member_detail.html'
    model = MemberModel

class MemberUpdate(UpdateView, LoginRequiredMixin):
    template_name = 'member_update.html'
    model = MemberModel
    fields = ('membername', 'point_total', 'ave', 'max', 'min')
    success_url = reverse_lazy('member_list')

class MemberDelete(DeleteView, LoginRequiredMixin):
    template_name = 'member_delete.html'
    model = MemberModel
    success_url = reverse_lazy('member_list')
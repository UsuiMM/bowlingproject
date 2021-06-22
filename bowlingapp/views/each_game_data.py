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


class EachGameDataList(generic.ListView, LoginRequiredMixin):
    template_name = 'game_list.html'
    model = EachGameDataModel
    paginate_by = 10
    def get_queryset(self):
        return EachGameDataModel.objects.filter(user_set=self.request.user).order_by('-datetime')

@login_required
def gamedetailview(request, pk):
    object = EachGameDataModel.objects.get(pk=pk)
    today = str(timezone.now()).split('-')
    for m in EachGameDataModel.objects.filter(user_set=request.user, datetime=object, pk=pk).annotate(mem=Max('members')):
        member_list = str('{}'.format(m.mem)).split(',')
    for m in EachGameDataModel.objects.filter(user_set=request.user, datetime=object, pk=pk).annotate(mem=Max('points')):
        member_point = str('{}'.format(m.mem)).split(',')
    for m in EachGameDataModel.objects.filter(user_set=request.user, datetime=object, pk=pk).annotate(mem=Max('aves')):
        member_ave = str('{}'.format(m.mem)).split(',')
    for m in EachGameDataModel.objects.filter(user_set=request.user, datetime=object, pk=pk).annotate(mem=Max('maxs')):
        member_max = str('{}'.format(m.mem)).split(',')
    for m in EachGameDataModel.objects.filter(user_set=request.user, datetime=object, pk=pk).annotate(mem=Max('mins')):
        member_min = str('{}'.format(m.mem)).split(',')
    context = {
            'object' : object,
            'year' : today[0],
            'month' : today[1],
            'date' : today[2],
            'member_list' : member_list,
            'member_point' : member_point,
            'member_ave' : member_ave,
            'member_max' : member_max,
            'member_min' : member_min,
        }
    return render(request, 'game_detail.html', context)

class EachGameDataDelete(DeleteView, LoginRequiredMixin):
    template_name = 'game_delete.html'
    model = EachGameDataModel
    success_url = reverse_lazy('game_list')

class EachGameDataUpdate(UpdateView, LoginRequiredMixin):
    template_name = 'game_update.html'
    model = EachGameDataModel
    fields = ('datetime', 'members', 'points', 'aves', 'maxs', 'mins')
    success_url = reverse_lazy('game_list')

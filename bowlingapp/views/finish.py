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

@login_required
def finishview(request):
    today = str(localtime(timezone.now())).split('-')
    date = today[2]
    game = GameModel.objects.filter(user_set=request.user).order_by('membername')
    eachgame = EachGameDataModel.objects.all().order_by('datetime')
    context = {
            'year' : today[0],
            'month' : today[1],
            'date' : today[2],
    }

    if request.method == 'POST':  
        count = mcount = 0
        mname = mpoint = mave = mmax = mmin = ''
        for m in GameModel.objects.filter(user_set=request.user).annotate(name=Max('membername')): 
            count += 1
        # テキストに、それぞれカンマ区切りでぶちこむ
        for m in GameModel.objects.filter(user_set=request.user).annotate(name=Max('membername')): 
            mname += '{}'.format(m.name)
            if count != mcount+1:
                mname += str(',')
            mcount += 1
        mcount = 0
        for m in GameModel.objects.filter(user_set=request.user).annotate(point=Max('point_total')): 
            mpoint += str('{}'.format(m.point)) 
            if count != mcount+1:
                mpoint += str(',')
            mcount += 1
        mcount = 0
        for m in GameModel.objects.filter(user_set=request.user).annotate(aves=Max('ave')): 
            mave += str('{}'.format(m.aves)) 
            if count != mcount+1:
                mave += str(',')
            mcount += 1
        mcount = 0
        for m in GameModel.objects.filter(user_set=request.user).annotate(maxs=Max('max')): 
            mmax += str('{}'.format(m.maxs)) 
            if count != mcount+1:
                mmax += str(',')
            mcount += 1
        mcount = 0
        for m in GameModel.objects.filter(user_set=request.user).annotate(mins=Max('min')): 
            mmin += str('{}'.format(m.mins)) 
            if count != mcount+1:
                mmin += str(',')
            mcount += 1
        EachGameDataModel.objects.create(    # データベースに今回のデータを記録
                datetime = str(today[0] + '/' + today[1] + '/' + date[:2] + ' -' + date[3:5] + 'h' + date[6:8] + 'm-'),        #today[0] + '/' + today[1] + '/' + date[:2]           
                members = str(mname),
                points = str(mpoint),
                aves = str(mave),
                maxs = str(mmax),
                mins = str(mmin),
                user_set = str(request.user),
            )   
        
        mname = mpoint = mave = mmax = mmin = 0
        for m in GameModel.objects.filter(user_set=request.user).annotate(name=Max('membername'), point=Max('point_total'), aves=Max('ave'), maxs=Max('max'), mins=Max('min')): 
            # 各メンバーの試合データ取得
            mname = str('{}'.format(m.name))
            mpoint = int('{}'.format(m.point)) 
            mave = int('{}'.format(m.aves)) 
            mmax = int('{}'.format(m.maxs)) 
            mmin = int('{}'.format(m.mins)) 
            for n in MemberModel.objects.filter(user_set=request.user, membername=mname).annotate(po=Max('point_total'), av=Max('ave'), ma=Max('max'), mi=Max('min')):
                # そのメンバーのデータ取得
                mpo = int('{}'.format(n.po)) 
                mav = int('{}'.format(n.av)) 
                mma = int('{}'.format(n.ma)) 
                mmi = int('{}'.format(n.mi)) 
            # そのメンバーのデータを試合データと計算し、新データに更新
            mpo += mpoint   # ポイント加算
            if mave > mav:  # averageの高い方を記録
                mav = mave
            if mmax > mma:  # maxの高い方を記録
                mma = mmax
            if mmin > mmi:  # minの高い方を記録
                mmi = mmin
            MemberModel.objects.filter(user_set=request.user, membername=mname).update(  # データベースに今回のデータを参照し、更新
                    point_total = int(mpo),
                    ave = int(mav),
                    max = int(mma),
                    min = int(mmi),
                )

        GameModel.objects.filter(user_set=request.user).delete()
        CoreModel.objects.filter(user_set=request.user).delete()
        TeamCalculusModel.objects.filter(user_set=request.user).delete()    

        return redirect(to='/home/')   
    return render(request, 'game_finish.html', context)      
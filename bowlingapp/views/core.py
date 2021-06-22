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

class CoreDetail(DetailView, LoginRequiredMixin):
    template_name = 'core_detail_2.html'
    model = CoreModel

class CoreDelete(DeleteView, LoginRequiredMixin):
    template_name = 'core_delete_2.html'
    model = CoreModel
    success_url = reverse_lazy('index')

@login_required
def coreview(request):
    today = str(timezone.now()).split('-')
    member_list = MemberModel.objects.filter(user_set=request.user)
    core = CoreModel.objects.filter(user_set=request.user).order_by('-raund', 'member')
    game = GameModel.objects.filter(user_set=request.user).order_by('membername')
    calucu = TeamCalculusModel.objects.filter(user_set=request.user).order_by('-raund')
    form = SpendingForm()    #フォームを読み込む
    context = {
            'year' : today[0],
            'month' : today[1],
            'member_list' : member_list,
            'core' : core,
            'game' : game,
            'calucu' : calucu,
            'form' : form,
            }

    if request.method == 'POST':    # フォームでデータが送られてきたら
        if 'ok' in request.POST:
            data = request.POST         # 以下フォームのデータの代入
            member_name = data['member_list']
            raund = data['raund']
            score = data['score']
            team_choice = data['team_choice']
            pin = data['pin']
            hand = data['handicap']
            
            if int(raund) <= 0:
                return redirect(to='/index/')

            if int(score) >= 0: # 0 or +スコアなら通常通り
                aave = int(score)
                bmax = int(score)
                cmin = int(score)
                count = 1
            elif int(score) < 0: # -スコアならpostしたスコア無視 >>> 単純な更新！！
                aave = 0
                bmax = 0
                cmin = 10000
                count = 0
            # Average計算
            for m in CoreModel.objects.filter(user_set=request.user, member=member_name).annotate(avg_score=Max('score')):
                aave += int('{}'.format(m.avg_score))
                count += 1
            if count != 0:
                aave //= count
            # Max計算
            for m in CoreModel.objects.filter(user_set=request.user, member=member_name).annotate(max_score=Max('score')):
                b = int('{}'.format(m.max_score))
                if b > bmax:
                    bmax = b
            # Min計算
            for m in CoreModel.objects.filter(user_set=request.user, member=member_name).annotate(min_score=Min('score')):
                c = int('{}'.format(m.min_score))
                if c < cmin:
                    cmin = c

            # ハンデありのスコア計算
            if hand[0] == '+':
                score_h = int(score) + int(hand[1:])
            elif hand[0] == 'x':
                score_h = int(score) * float(hand[1:])
            
            if int(score) >= 0:
                CoreModel.objects.create(    # データベースにデータを入れる
                    member = str(member_name),
                    raund = int(raund),
                    score = int(score),
                    ave = int(aave),
                    max = int(bmax),
                    min = int(cmin),
                    team_choice = str(team_choice),
                    pin = int(pin),
                    handicap = str(hand),
                    score_h = int(score_h),
                    user_set = str(request.user),
                )   
            #---------------------------------------------------
            # CoreModelのデータベースに依存させたい
            GameModel.objects.filter(user_set=request.user, membername=member_name).delete() # 同じ名前のデータを削除、最新のみにするため
            if count != 0:                                       # count=0 >>> 保存するデータ無し
                GameModel.objects.create(                        # データベースにデータを入れる
                    membername = str(member_name),
                    ave = int(aave),
                    max = int(bmax),
                    min = int(cmin),
                    user_set = str(request.user),
                )   
            
            # pointの計算------------------------------------------ CoreModelのデータベースに依存させたい
            #-----------------------------------------------------
            sc_a = sc_b = sc_c = point_a = point_b = point_c = 0
            for m in CoreModel.objects.filter(user_set=request.user, team_choice="A", raund=raund).annotate(score_cul=Max('score_h')): # 保存してあるスコア(ハンデ込み)を取り出して合計出す
                sc_a += int('{}'.format(m.score_cul)) 
            for m in CoreModel.objects.filter(user_set=request.user, team_choice="B", raund=raund).annotate(score_cul=Max('score_h')):
                sc_b += int('{}'.format(m.score_cul))
            for m in CoreModel.objects.filter(user_set=request.user, team_choice="C", raund=raund).annotate(score_cul=Max('score_h')):
                sc_c += int('{}'.format(m.score_cul))
            
            if sc_a > sc_b and sc_c == 0:              # 2チーム対戦
                point_a = sc_a - sc_b
                point_b = sc_b - sc_a
            elif sc_a < sc_b and sc_c == 0:
                point_a = sc_a - sc_b
                point_b = sc_b - sc_a
            elif sc_a == sc_b and sc_c == 0:
                point_a = point_b = point_c = 0
            elif sc_a > sc_b and sc_a > sc_c:          # 3チーム対戦
                if sc_b > sc_c:              
                    point_a = sc_a - sc_c
                    point_c = sc_c - sc_a
                elif sc_b < sc_c:
                    point_a = sc_a - sc_b
                    point_b = sc_b - sc_a
                elif sc_b == sc_c:               # 下位同点
                    point_a = sc_a - sc_b
                    point_b = point_c = -(point_a // 2)
            elif sc_b > sc_a and sc_b > sc_c:  
                if sc_a > sc_c:
                    point_b = sc_b - sc_c
                    point_c = sc_c - sc_b
                elif sc_a < sc_c:
                    point_b = sc_b - sc_a
                    point_a = sc_a - sc_b
                elif sc_a == sc_c:
                    point_b = sc_b - sc_a
                    point_a = point_c = -(point_b // 2)
            elif sc_c > sc_a and sc_c > sc_b: 
                if sc_a > sc_b:
                    point_c = sc_c - sc_b
                    point_b = sc_b - sc_c
                elif sc_a < sc_b:
                    point_c = sc_c - sc_a
                    point_a = sc_a - sc_c
                elif sc_a == sc_b:
                    point_c = sc_c - sc_a
                    point_a = point_b = -(point_c // 2)
            elif sc_a == sc_b and sc_a > sc_c:   # 上位同点
                point_a = point_b = (sc_a - sc_c) // 2
                point_c = sc_c - sc_a
            elif sc_a == sc_c and sc_a > sc_b:  
                point_a = point_c = (sc_a - sc_b) // 2
                point_b = sc_b - sc_a
            elif sc_b == sc_c and sc_b > sc_a:  
                point_b = point_c = (sc_b - sc_a) // 2
                point_a = sc_a - sc_b
            
            if int(score) >= 0:
                TeamCalculusModel.objects.filter(user_set=request.user, raund=raund).delete() # 最新だけ残すため
                TeamCalculusModel.objects.create(                      # 最新情報のみ、データベースにデータを入れる
                    team = "A",
                    raund = int(raund),
                    sum_total = sc_a,
                    point_alloc = int(point_a) * int(pin),
                    user_set = str(request.user),
                )   
                TeamCalculusModel.objects.create(   
                    team = "B",
                    raund = int(raund),
                    sum_total = sc_b,
                    point_alloc = int(point_b) * int(pin),
                    user_set = str(request.user),
                )   
                TeamCalculusModel.objects.create(   
                    team = "C",
                    raund = int(raund),
                    sum_total = sc_c,
                    point_alloc = int(point_c) * int(pin),
                    user_set = str(request.user),
                )   
            for m in TeamCalculusModel.objects.filter(user_set=request.user, raund=raund, team='A').annotate(pt=Max('point_alloc')): 
                pa = int('{}'.format(m.pt)) 
                CoreModel.objects.filter(user_set=request.user, raund=raund, team_choice='A').update(point=pa)
            for m in TeamCalculusModel.objects.filter(user_set=request.user, raund=raund, team='B').annotate(pt=Max('point_alloc')):
                pb = int('{}'.format(m.pt))
                CoreModel.objects.filter(user_set=request.user, raund=raund, team_choice='B').update(point=pb)
            for m in TeamCalculusModel.objects.filter(user_set=request.user, raund=raund, team='C').annotate(pt=Max('point_alloc')):
                pc = int('{}'.format(m.pt))
                CoreModel.objects.filter(user_set=request.user, raund=raund, team_choice='C').update(point=pc)

            gpt = 0
            for g in GameModel.objects.filter(user_set=request.user).annotate(mn=Max('membername')):
                g = '{}'.format(g.mn)
                for n in CoreModel.objects.filter(user_set=request.user, member=g).annotate(pt=Max('point')):
                    gpt += int('{}'.format(n.pt))
                GameModel.objects.filter(user_set=request.user, membername=g).update(point_total=gpt)
                gpt = 0
            #----------------------------------------------------
            '''
            if int(score) == -2:
                # 選択したラウンドのポイント取得
                for m in TeamCalculusModel.objects.filter(raund=raund, team='A').annotate(pt=Max('point_alloc')): 
                    pa = int('{}'.format(m.pt)) 
                for m in TeamCalculusModel.objects.filter(raund=raund, team='B').annotate(pt=Max('point_alloc')):
                    pb = int('{}'.format(m.pt))
                for m in TeamCalculusModel.objects.filter(raund=raund, team='C').annotate(pt=Max('point_alloc')):
                    pc = int('{}'.format(m.pt))
                # メンバー取得して、今までのポイントに加算
                for m in CoreModel.objects.filter(raund=raund, team_choice='A').annotate(mem=Max('member')): 
                    ma = '{}'.format(m.mem)
                    for n in GameModel.objects.filter(membername=ma).annotate(pt=Max('point_total')):
                        pa += int('{}'.format(n.pt))
                    GameModel.objects.filter(membername=ma).update(point_total=pa)
                for m in CoreModel.objects.filter(raund=raund, team_choice='B').annotate(mem=Max('member')):
                    mb = '{}'.format(m.mem)
                    for n in GameModel.objects.filter(membername=mb).annotate(pt=Max('point_total')):
                        pb += int('{}'.format(n.pt))
                    GameModel.objects.filter(membername=mb).update(point_total=pb)
                for m in CoreModel.objects.filter(raund=raund, team_choice='C').annotate(mem=Max('member')):
                    mc = '{}'.format(m.mem)
                    for n in GameModel.objects.filter(membername=mc).annotate(pt=Max('point_total')):
                        pc += int('{}'.format(n.pt))
                    GameModel.objects.filter(membername=mc).update(point_total=pc)

            if int(score) == -3:
                for g in GameModel.objects.annotate(pt=Max('point_total')):
                    gp = int('{}'.format(g.pt))
                    GameModel.objects.filter(point_total=gp).update(point_total=0)
                    '''
            #-----------------------------------------------------------------------------------------------------
            return redirect(to='/index/')   #再び/index/を読み込む
        '''
        elif 'button_1' in request.POST:
            # ラウンド数の最大値取得
            r = rmax = 0
            for m in CoreModel.objects.annotate(rm=Max('raund')):
                r = int('{}'.format(m.rm))
                if r > rmax:
                    rmax = r
            # スコアを取得、加算、ピン取得、トータルスコア×ピン＝ポイント取得
            stotal = pin = point = 0
            for i in range(rmax):
                for m in CoreModel.objects.filter(raund=i, team_choice='A').annotate(s=Max('score'), p=Max('pin')): 
                    stotal += int('{}'.format(m.s)) 
                    pin = int('{}'.format(m.p))
                point = stotal * pin
                TeamCalculusModel.objects.filter(raund=i, team='A').update(sum_total=stotal, point_alloc=point)
                stotal = 0
                for m in CoreModel.objects.filter(raund=i, team_choice='B').annotate(s=Max('score'), p=Max('pin')):
                    stotal += int('{}'.format(m.s))
                    pin = int('{}'.format(m.p))
                point = stotal * pin
                TeamCalculusModel.objects.filter(raund=i, team='B').update(sum_total=stotal, point_alloc=point)
                stotal = 0
                for m in CoreModel.objects.filter(raund=i, team_choice='C').annotate(s=Max('score'), p=Max('pin')):
                    stotal += int('{}'.format(m.s))
                    pin = int('{}'.format(m.p))
                point = stotal * pin
                TeamCalculusModel.objects.filter(raund=i, team='C').update(sum_total=stotal, point_alloc=point)
            
            TeamCalculusModel.objects.all().order_by('-raund', 'team')
        
            return redirect(to='/index/')   #再び/index/を読み込む
        '''

    return render(request, 'core/index.html', context)      


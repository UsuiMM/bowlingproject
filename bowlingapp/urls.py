from django.contrib import admin
from django.urls import path
from . import views
from .views import bowling_home, core, each_game_data, finish, game, member, login

urlpatterns = [
    path('admin/', admin.site.urls), 

    path('home/', bowling_home.BowlingHome.as_view(), name='home'),

    path('game_list/', each_game_data.EachGameDataList.as_view(), name='game_list'),
    path('game_detail/<int:pk>/',each_game_data. gamedetailview, name='game_detail'),
    path('game_delete/<int:pk>/', each_game_data.EachGameDataDelete.as_view(), name='game_delete'),
    path('game_update/<int:pk>/', each_game_data.EachGameDataUpdate.as_view(), name='game_update'),

    path('member_list/', member.memberlistview, name='member_list'),
    path('member_add/', member.MemberCreate.as_view(), name='member_add'),
    path('member_detail/<int:pk>/', member.MemberDetail.as_view(), name='member_detail'),
    path('member_update/<int:pk>/', member.MemberUpdate.as_view(), name='member_update'),
    path('member_delete/<int:pk>/', member.MemberDelete.as_view(), name='member_delete'),

    path('core_detale_1/<int:pk>/', game.GameDetail.as_view(), name='core_detail_1'),
    path('core_delete_1/<int:pk>/', game.GameDelete.as_view(), name='core_delete_1'),

    path('core_detale_2/<int:pk>/', core.CoreDetail.as_view(), name='core_detail_2'),
    path('core_delete_2/<int:pk>/', core.CoreDelete.as_view(), name='core_delete_2'),
    path('core_update/<int:pk>/', core.CoreDetail.as_view(), name='core_update'),
    path('index/', core.coreview, name="index"),

    path('game_finish/', finish.finishview, name="game_finish"),

    path('signup/', login.signupview, name="signup"),
    path('login/', login.loginview, name="login"),
    path('logout/', login.logoutview, name="logout"),

]

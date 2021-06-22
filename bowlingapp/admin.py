from django.contrib import admin
from .models import EachGameDataModel, GameModel, MemberModel, CoreModel, TeamCalculusModel


# ゲーム中
admin.site.register(CoreModel) # form
admin.site.register(GameModel) # ゲーム中のメンバーデータ
admin.site.register(TeamCalculusModel) # ゲーム中のチーム計算のデータ 

# 保存
admin.site.register(MemberModel) # メンバーデータ保存
admin.site.register(EachGameDataModel) # ゲームデータ保存

# Register your models here.

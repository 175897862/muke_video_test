# coding:utf-8

from enum import Enum  # python枚举包，优先于django
from django.db import models

class VideoType(Enum):
    movie = 'movie'
    cartoom = 'cartoom'
    episode = 'episode'
    variety = 'variety'
    other = 'other'

# 定义标签
VideoType.movie.label = '电影'
VideoType.cartoom.label = '卡通'
VideoType.episode.label = '电视剧'
VideoType.variety.label = '综艺'
VideoType.other.label = '其他'

class FromType(Enum):
    youku = 'youku'
    custom = 'custom'

FromType.youku.label = '优酷'
FromType.custom.label = '自制'

class NationalityType(Enum):
    china = 'china'
    japan = 'japan'
    korea = 'korea'
    american = 'american'
    other = 'other'

NationalityType.china.label = '中国'
NationalityType.japan.label = '日本'
NationalityType.korea.label = '韩国'
NationalityType.american.label = '美国'
NationalityType.other.label = '其他'

class IdentityType(Enum):
    to_star = 'to_star'
    supporting_rule = 'supporting_rule'
    director = 'director'

IdentityType.to_star.label = '主演'
IdentityType.supporting_rule.label = '配角'
IdentityType.director.label = '导演'


class Video(models.Model):
    name = models.CharField(max_length=100, null=False)
    image = models.CharField(max_length=500, default='')
    video_type = models.CharField(max_length=50, default=VideoType.other.value)
    from_to = models.CharField(max_length=20, default=FromType.custom.value)
    nationality = models.CharField(max_length=20, default=NationalityType.other.value)
    info = models.TextField()
    status = models.BooleanField(default=True, db_index=True)
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)

    class Meta:  # 联合唯一索引
        unique_together = ('name', 'video_type', 'from_to', 'nationality')

    def __str__(self):
        return self.name

class VideoStar(models.Model):  # 演员附表
    video = models.ForeignKey(Video, related_name='video_star', on_delete=models.SET_NULL, blank=True, null=True)
    name = models.CharField(max_length=100, null=False)
    identity = models.CharField(max_length=50, default='')  # 身份

    class Meta:  # 联合唯一索引
        unique_together = ('video', 'name', 'identity')

    def __str__(self):
        return self.name

class VideoSub(models.Model):  # 剧集及播放地址附表
    video = models.ForeignKey(Video, related_name='video_sub', on_delete=models.SET_NULL, blank=True, null=True)
    url = models.CharField(max_length=500, null=False)
    number = models.IntegerField(default=1)  # 视频集数据，默认为1（如电影）

    class Meta:  # 联合唯一索引
        unique_together = ('video', 'number')

    def __str__(self):
        return 'video:{},number:{}'.format(self.video.name, self.number)

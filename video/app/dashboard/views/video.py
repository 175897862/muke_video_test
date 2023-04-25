# coding:utf-8

from django.views.generic import View
from django.shortcuts import redirect, reverse
from app.libs.base_render import render_to_response
from app.utils.permission import dashboard_auth
from app.model.video import (
    VideoType, FromType, NationalityType, Video, VideoSub,
    IdentityType, VideoStar)
from app.utils.common import check_and_get_video_type

class ExternaVideo(View):  # 外链视频
    TEMPLATE = 'dashboard/video/externa_video.html'

    @dashboard_auth
    def get(self,request):
        error = request.GET.get('error', '')
        data = {'error': error}

        # 从数据库中获取排除custom自制以外的所有视频
        videos = Video.objects.exclude(from_to=FromType.custom.value)
        data['videos'] = videos

        return  render_to_response(request, self.TEMPLATE, data=data)

    def post(self, request):
        name = request.POST.get('name')
        image = request.POST.get('image')
        video_type = request.POST.get('video_type')
        from_to = request.POST.get('from_to')
        nationality = request.POST.get('nationality')
        info = request.POST.get('info')

        # if not all()里面是一个列表，而不是元素。
        if not all([name, image, video_type, from_to, nationality, info]):
            return redirect('{}?error={}'.format(reverse('video_externa'), '缺少必要字段'))

        result = check_and_get_video_type(VideoType, video_type, '非法的视频类型')
        if result.get('code') != 0:
            return redirect('{}?error={}'.format(reverse('video_externa'), result['msg']))

        result = check_and_get_video_type(FromType, from_to, '非法的视频来源')
        if result.get('code') != 0:
            return redirect('{}?error={}'.format(reverse('video_externa'), result['msg']))

        result = check_and_get_video_type(NationalityType, nationality, '非法的国籍')
        if result.get('code') != 0:
            return redirect('{}?error={}'.format(reverse('video_externa'), result['msg']))

        Video.objects.create(
            name=name,
            image=image,
            video_type=video_type,
            from_to=from_to,
            nationality=nationality,
            info=info
        )

        return redirect(reverse('video_externa'))

class VideoSubView(View):
    TEMPLATE = 'dashboard/video/video_sub.html'

    @dashboard_auth
    def get(self, request, video_id):
        data = {}
        video = Video.objects.get(pk=video_id)

        data['video'] = video
        error = request.GET.get('error', '')
        data['error'] = error
        return render_to_response(request, self.TEMPLATE, data=data)

    def post(self, request, video_id):
        url = request.POST.get('url')

        video = Video.objects.get(pk=video_id)
        # 获取视频集数的方法有多种，这里采用直接拿video_sub长度的方法
        # video_subs = VideoSub.objects.filter(video=video)
        length = video.video_sub.count()
        VideoSub.objects.create(video=video, url=url, number=length + 1)

        return redirect(reverse('video_sub', kwargs={'video_id':video_id}))

class VideoStarView(View):

    def post(self, request):
        name = request.POST.get('name')
        identity = request.POST.get('identity')
        video_id = request.POST.get('video_id')

        # print(name, identity, video_id)  # 验证数据是否到达时用
        path_format = '{}'.format(reverse('video_sub', kwargs={'video_id':video_id}))
        if not all([name, identity, video_id]):
            return redirect('{}?error={}'.format(path_format, '缺少必要字段'))

        result = check_and_get_video_type(IdentityType, identity, '非法的身份')
        if result.get('code') != 0:
            return redirect('{}?error={}'.format(path_format, result['msg']))

        video = Video.objects.get(pk=video_id)  # 这里用get默认视频已存在，如果不存在这样用会报错
        try:
            VideoStar.objects.create(
                video=video,
                name=name,
                identity=identity
            )
        except:
            return redirect('{}?error={}'.format(path_format, '添加失败'))

        return redirect(reverse('video_sub', kwargs={'video_id':video_id}))

class StarDelete(View):
    def get(self, request, star_id, video_id):
        VideoStar.objects.filter(id=star_id).delete()
        return redirect(reverse('video_sub', kwargs={'video_id':video_id}))

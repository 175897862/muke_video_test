var videoEreaStatic = false;  //视频编辑区域初始状态为false
var videoEditArea = $('#video-edit-area');  //定义视频编辑区域

$('#open-add-video-btn').click(function(){  //定义创建视频按钮区域点击事件
    if (!videoEreaStatic) {        //如果视频编辑区域状态非false为真
        videoEditArea.show();      //则让视频编辑区域可见
        videoEreaStatic = true;    //同时将视频编辑区域状态改为true
    } else {
        videoEditArea.hide();      //否则隐藏视频编辑区域
        videoEreaStatic = false;   //同时将视频编辑区域状态改为false
    }
});

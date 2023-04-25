# coding:utf-8

# 获取和验证视频类型的公共函数，传入的参数为（类型枚举函数，类型值，返回信息）
def check_and_get_video_type(type_obj, type_value, message):
    try:  # 从枚举函数中取值
        type_obj(type_value)
    except:  # 如果失败则返回状态码-1和message
        return {'code':-1, 'msg':message}
    # 如果成功则返回状态码0和success
    return {'code':0, 'msg':'success'}

import hashlib
import hmac
import json
import random
import string
import time

# 随机生成字符串重新组装成新的字符串
import requests


def make(rule, n):
    """
    :param rule: 随机数的组成规则
    :param n: 生成随机数的长度
    :return: 返回生成的随机数
    """
    # rule = string.ascii_letters + string.digits 字母加数字的格式
    ran_str = ''.join(random.sample(rule, n))
    print(ran_str)
    return ran_str


# def MakeRN():
#     """
#     :生成0-9范围内的随机数
#     :return: 生成的随机数
#     """
#     RN = random.randint(0, 9)
#     return RN
#
#
# def MakeRNumber(x, y):
#     """
#     :生成在一定范围内的随机数字
#     :param x: 开始的数字，包括
#     :param y: 结束的范围，不包括
#     :return: 生成的随机数
#     """
#     RN = random.randint(x, y)
#     return RN
#
#
# def MakeRS():
#     """
#     :从a-z里面随机产生一个字母
#     :return:
#     """
#     Str = string.ascii_lowercase
#     RS = random.choice(Str)
#     return RS
#
#
# def MakeStr():
#     """
#     # 生成规律的随机字符串
#     :return:
#     """
#     nonceStr = str(MakeRN()) + str(MakeRS()) + str(MakeRN()) + str(MakeRS()) + str(MakeRN()) + str(MakeRS()) + str(
#         MakeRN()) + str(MakeRN()) + '-' + str(
#         MakeRN()) + str(
#         MakeRN()) + str(MakeRS()) + str(MakeRN()) + '-' + str(MakeRN()) + str(MakeRN()) + str(MakeRN()) + str(
#         MakeRN()) + '-' + str(MakeRS()) + str(MakeRN()) + str(MakeRS()) + str(
#         MakeRN()) + '-' + str(MakeRN()) + str(MakeRN()) + str(MakeRS()) + str(MakeRN()) + str(MakeRN()) + str(
#         MakeRN()) + str(MakeRN()) + str(MakeRS()) + str(MakeRS()) + str(
#         MakeRN()) + str(MakeRS()) + str(MakeRS())
#     print(nonceStr)
#     return nonceStr
def maketoken():
    with open("D://Locust/TOKEN1.json") as f:
        B = json.load(f)
        # print(B)
        token = B.get("tokens")
        print(token)
        print([X for X in token])


class InterfaceSign:

    def getStringA(self, content):
        """
        按照参数名ASCII码从小到大排序
        :param content:
        :return:
        """
        data = []
        StringA = ''
        # for key1 in content: 对性能有较大的消耗
        # 获取字典里面的值
        for key1, value in content.items():
            # 将字典转化为key=value形式
            Str = str(key1) + '=' + str(value)
            # 将字符串写入list中
            data.append(Str)
        # 将list按照key从小到大进行排序,sort默认升序
        data.sort()
        nums = 0
        # print(data)
        for i in data:
            max_nums = len(data)
            nums = nums + 1
            # 如果是最后一位就不要带上&
            # 拼接字符串
            if nums == max_nums:
                StringA += str(i)
            else:
                StringA += str(i) + '&'
        # print(StringA)
        return StringA

    # 处理生成签名和组装post请求参数
    def GetStringSignTemp(self, interfaceKey, content):
        """
        :param interfaceKey: 接口的密匙
        :param content: 接口的参数
        :return: 返回加密的参数
        """
        StringA = self.getStringA(content)
        StringSignTemp = StringA + "&" + "key=" + interfaceKey
        # print(StringSignTemp)
        interfaceKey = interfaceKey.encode('utf-8')
        StringSignTemp = StringSignTemp.encode('utf-8')
        # .hexdigest 加密后为字符串类型
        interfaceSign = hmac.new(interfaceKey, StringSignTemp, digestmod=hashlib.sha256).hexdigest().upper()
        content['sign'] = interfaceSign
        # content['timestamp'] = int(time.time())
        # 将数据转化为json格式
        data = json.dumps(content, ensure_ascii=False)
        return data

    # 组装GET\PUT请求参数
    def GetURL(self, interfaceKey, content):
        data = self.GetStringSignTemp(interfaceKey, content)
        params = self.getStringA(json.loads(data))
        return params


sign = InterfaceSign()

if __name__ == '__main__':
    key = "84b4aea73e331b15cf7c6d1dd0f7ee9c"

    # 保存用户名片信息
    url = "https://api-beta.cdhourong.top/game/userHave/userDetailGame"
    data = {

        "gameId": "1437345809191411714",
        "userId": "1407881211981041666",
        "timestamp": int(time.time()),
        "nonceStr": "8c5e2a16-93c7-4937-b2f7-93a9124ac3bc"
    }

    headers = {
        'Content-Type': "application/json",
        'Authorization': 'Bearer eyJhbGciOiJSUzI1NiJ9.eyJ1c2VyIjoie1widW5pb25JZFwiOjk5OTk5OS'
                         'xcImltVG9rZW5cIjpcIjA5OTlmNTE2NWQyZmRkNGFjY2EzZTY2MWFkMTZiZTAzXCIsX'
                         'CJwZXJmZWN0SW5mb1wiOjEsXCJhY2NJZFwiOlwiMGMwMTUyZjA1NTk3NDIyMGFkNzYxM'
                         'Dc3YjJiZTdmN2RcIixcImlkXCI6MTMzODgxMDQzMDI5MDgyMTEyMn0iLCJqdGkiOiJOb'
                         'UU0WmpnellUQXRaVFV5WVMwME1EVmlMV0psTWprdFpHTmpaRFZqWkRFMllqQmkiLCJleH'
                         'AiOjc5NDY2NjU4NzF9.vilSblWBcjwgoerGYEQfBNiPScvV6RMiz2Qg_B7vLFhd9X9ANL'
                         '9z8SmZP9OvaqiIobqYAaxnc-cwRUGb6ubMLc9FJgquMORIvE2l1Pd1eBKT5LKO437HnM4'
                         'UYSkMRzdC1t7yUoIMtL6h19Oy17YhGnDG6cgQhxKqu97GWyU3cAzoEl6e_oungfstBW3F9'
                         '8qOqnVAzEIAJUNJOxp9nIZfRN7e7MsZkYH554GEHoQWOX1vf1VocBFLC_vKQvL1oN42dJ20'
                         'HnY_F8uuuZ0NO6Y-ePsELYHQHTjSz1SKpzgDvJh7a1ZF8WMun5wQ5z9AlGx7CPUhPjmcMxRAm6JrzQq4Jg '
    }

    # POST请求
    # params1 = sign.GetStringSignTemp(key, data)
    params1 = sign.GetURL(key, data)
    response = requests.request("get", url, headers=headers, params=params1)
    # get请求
    print(response.text)
    # maketoken()

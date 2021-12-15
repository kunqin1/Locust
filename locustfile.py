import json

# import gevent
# from gevent import monkey

# gevent.monkey.patch_all()
import queue

from locust import task, between, TaskSet, HttpUser
import os
import time
from sign import sign


class UserGame(TaskSet):

    @task(1)
    # task后面的数字表示多个接口同时运行时的概率task(1):task(2):task(1);这里表示按照1：2：1比例执行
    def Gamedetail(self):

        try:
            # 从队列头部获取值
            self.token = self.user.queue_token_list.get()
            # print(self.token)
        except queue.Empty:
            print('队列中没有数据了')
            # 队列中的数据取完后，结束线程
            exit(0)
        key = "84b4aea73e331b15cf7c6d1dd0f7ee9c"
        data = {

            "gameId": "1437345809191411714",
            "userId": "1407881211981041666",
            "timestamp": int(time.time()),
            "nonceStr": "8c5e2a16-93c7-4937-b2f7-93a9124ac3bc"
        }
        headers = {
            # 'Content-Type': "application/json",
            'Authorization': self.token
        }
        # print()
        params1 = sign.GetURL(key, data)
        self.url = "/game/userHave/userDetailGame"
        with self.client.get(self.url, headers=headers, params=params1, catch_response=True) as response:
            req = response.text
            # print(req)
            # if req.code == 0:
            #     response.success()
            # else:
            #     response.failure(req)


class GameLocust(HttpUser):
    weight = 1
    tasks = [UserGame]
    # 定义一个队列
    queue_token_list = queue.Queue()
    host = 'https://api-beta.cdhourong.top'
    wait_time = between(500, 1000)
    with open("D://Locust/token.json") as f:
        B = json.load(f)
        token = B.get("tokens")
        # print(token)
        for x in token:
            # strip()出去空格回车等字符串
            queue_token_list.put(x.strip())
            # print(queue_token_list)


if __name__ == '__main__':
    os.system("locust -f locustfile.py --host= https://api-beta.cdhourong.top")
    # maketoken()

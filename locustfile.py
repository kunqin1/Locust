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
    def Gamedetail(self):
        try:
            self.token = self.user.queue_token_list.get()
            # print(self.token)
        except queue.Empty:
            print('no data exist')
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
        req = self.client.get("/game/userHave/userDetailGame", headers=headers, params=params1).text

        # print(req)
        # if req.code == 0:
        #     print("ture")
        # else:
        #     print("fails")


class GameLocust(HttpUser):
    weight = 1
    tasks = [UserGame]
    queue_token_list = queue.Queue()
    host = 'https://api-beta.cdhourong.top'
    wait_time = between(500, 1000)
    with open("D://Locust/token.json") as f:
        B = json.load(f)
        token = B.get("tokens")
        # print(token)
        for x in token:
            queue_token_list.put(x)
            # print(queue_token_list)


if __name__ == '__main__':
    os.system("locust -f locustfile.py --host= https://api-beta.cdhourong.top")
    # maketoken()

from . import models
import json
from django.http import request, HttpResponse
import requests
from . import models
import logging


# def send_smd_whatsapp(request):
#     # idInstance = 1101792647
#     url = "https://api.green-api.com/waInstance1101792647/sendMessage/0e2ae4131ecf4790a7547155232ac940acd8091632444e17b3"
#     payload = {"chatId": "917976129787@c.us","message": "hello bro"}
#     dumped_payload = json.dumps(payload)
#     headers = {
#         'Content-Type': 'application/json'
#     }
#     response = requests.request("POST", url, headers=headers, data=dumped_payload)
#     print(response.text.encode('utf8'))

#     return HttpResponse("hey")

def send_smd_whatsapp(to, msg):
    # to=7976192787
    # msg='lovde'
    url="https://api.green-api.com/waInstance1101792647/sendMessage/0e2ae4131ecf4790a7547155232ac940acd8091632444e17b3"
    payload = {"chatId": f"91{to}@c.us","message": f"{msg}"}
    dumped_payload = json.dumps(payload)
    print(dumped_payload,"Payload")
    headers = {
    'Content-Type': 'application/json'
    }
    
    response = requests.request("POST", url, headers=headers, data=dumped_payload)

    print(response.text.encode('utf8'))
    return HttpResponse("hey")


# def send_task_reminder():

def send_reminder():
    tasks = models.TodoList.objects.all()
    for i in tasks.values('id', 'task', 'completed'):
        task = i['task']
        status = i['completed']
        if status == False:
            to = 7976192787
            msg = f'hey Priyank your {i["task"]} task is still not complete yet'
            send_smd_whatsapp(to, msg)

    print("Cronjob work successfull")   
  
from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Bank(models.Model):
    name = models.CharField(max_length = 200)
    blood_group = models.CharField(max_length =15)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    email = models.CharField(max_length = 50)
    phone_no = models.CharField(max_length = 10)
    decease = models.CharField(max_length =300)
    address =models.CharField(max_length = 300)
    time = models.DateTimeField(blank = True,null=True,auto_now_add=True)
    req_time =models.DateTimeField(blank = True,null=True)
    status = models.CharField(max_length=10,default="Active")
    def __str__(self):
        return str(self.name) + " , Blood Group : " + str(self.blood_group)


#chat system
class ChatRoom(models.Model):
    #user_requested = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_reqed')
    #user_requesting = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_reqing')
    owner = models.CharField(max_length=900)
    chatter1 = models.CharField(max_length=200)
    def __str__(self):
        return str(self.owner)


class Chat(models.Model):
    room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE)
    text = models.TextField()
    time  = models.DateTimeField(auto_now_add=True)
    chatter = models.CharField(max_length=900)
    def __str__(self):
        return str(self.text)
from email import message
from plistlib import UID
from django.db import models
from django.forms import CharField

# Create your models here.
class user_table(models.Model):
    userID=models.CharField(max_length=20)
    tokenID=models.CharField(max_length=200)
    imageUrl=models.CharField(max_length=200)
    nickname=models.CharField(max_length=10)
    kakaochat=models.CharField(max_length=50)
    joindate=models.DateField()
    kakaoID=models.CharField(max_length=15)
    address=models.CharField(max_length=50)
    messageonoff=models.CharField(max_length=2)

    def __str__(self) -> str:
        return self.nickname

class gossip_table(models.Model):
    gpsX=models.FloatField()
    gpsY=models.FloatField()    
    address=models.CharField(max_length=50)
    writeDate=models.DateTimeField()
    kakaochat=models.CharField(max_length=50)
    tokenID=models.CharField(max_length=200)
    userID=models.CharField(max_length=20)
    imageURL=models.CharField(max_length=200)
    memo=models.TextField()
    userFID=models.ForeignKey(user_table,on_delete=models.CASCADE)

    def __str__(self):
        return self.memo
    
class question(models.Model):
    gossip=models.ForeignKey(gossip_table,on_delete=models.CASCADE)
    questiondata=models.CharField(max_length=200)
    tokenID=models.CharField(max_length=200)
    userID=models.CharField(max_length=20)
    imageURL=models.CharField(max_length=200)
    writeTime=models.DateTimeField()

    def __str__(self):
        return self.questiondata

class answer(models.Model):
    questionFID=models.ForeignKey(question,on_delete=models.CASCADE)
    answerdata=models.CharField(max_length=200)    
    writeTime=models.DateTimeField()

    def __str__(self):
        return self.answerdata


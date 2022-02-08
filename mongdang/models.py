from django.db import models


class User(models.Model):
    username = models.CharField(max_length=10, unique=True)
    delYn = models.BooleanField(default=False)

    def __str__(self):
        return self.username + ':' + str(self.delYn)


class Note(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    contents = models.CharField(max_length=100, help_text="쪽지 내용")
    latitude = models.FloatField(default=0, help_text="위도")
    longitude = models.FloatField(default=0, help_text="경도")
    registtime = models.CharField(max_length=100, help_text="등록시간")
    endtime = models.CharField(max_length=100, help_text="종료시간")

    def __str__(self):
        return str(self.id) + ':' + str(self.user) + ':' + self.contents + ':' + str(self.latitude) + ':' + str(self.longitude) \
               + ':' + str(self.registtime) + ':' + str(self.endtime)


class Comment(models.Model):
    note = models.ForeignKey(Note, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.CharField(max_length=50, help_text="댓글 내용")

    def __str__(self):
        return str(self.id) + ':' + str(self.note) + ':' + str(self.user) + ':' + self.comment

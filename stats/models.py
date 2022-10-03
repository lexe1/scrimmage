from django.db import models


class Upload(models.Model):
    title = models.CharField(max_length=50, unique=True)
    file = models.FileField(upload_to='uploads')
    uploaded_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-uploaded_on']


class PlayerGameStats(models.Model):
    date = models.DateTimeField()
    player = models.CharField(max_length=255)
    min = models.FloatField()
    made_2 = models.IntegerField()
    attempts_2 = models.IntegerField()
    made_3 = models.IntegerField()
    attempts_3 = models.IntegerField()
    made_ft = models.IntegerField()
    attempts_ft = models.IntegerField()
    reb_o = models.IntegerField()
    reb_d = models.IntegerField()
    assist = models.IntegerField()
    poa = models.IntegerField()
    pf = models.IntegerField()
    fd = models.IntegerField()
    steals = models.IntegerField()
    turnovers = models.IntegerField()
    blocks = models.IntegerField()
    # pts = models.FloatField()

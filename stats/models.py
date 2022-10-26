from django.db import models
from django.urls import reverse


class Upload(models.Model):
    file = models.FileField(upload_to='uploads')
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.id)

    class Meta:
        ordering = ['-date']

    def get_absolute_url(self):
        return reverse('home')


class Match(models.Model):
    date = models.DateTimeField()

    def __str__(self):
        return str(self.id)

    class Meta:
        ordering = ['-date']

    def get_absolute_url(self):
        return reverse('home')


class StatLine(models.Model):
    match = models.ForeignKey(Match, on_delete=models.CASCADE)
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

    class Meta:
        ordering = ['date']

    def __str__(self):
        return self.player

    @property
    def percentage_2(self):
        if self.attempts_2 == 0:
            return 0.0
        x = float(self.made_2/self.attempts_2)
        return (round(x, 2))

    @property
    def percentage_3(self):
        if self.attempts_3 == 0:
            return 0.0
        x = float(self.made_3/self.attempts_3)
        return (round(x, 2))

    @property
    def percentage_ft(self):
        if self.attempts_ft == 0:
            return 0.0
        x = float(self.made_ft/self.attempts_ft)
        return (round(x, 2))

    @property
    def reb_t(self):
        x = int(self.reb_o) + int(self.reb_d)
        return x

    # @property
    #   def pts(self):

from django.db import models
from django.contrib.auth.models import User


class RPS(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    content = models.TextField(blank=True, null=True)

    def __str__(self):
        return f'From {self.sender}'


class Lobby(models.Model):
    # name = models.CharField(max_length=100, blank=True, null=True) - Можно будет использовать для уникальности
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    members = models.ManyToManyField(User, through=r'LobbyMember', symmetrical=False,
                                     related_name='members_group')

    def __str__(self):
        return str(self.id)


class LobbyMember(models.Model):
    lobby = models.ForeignKey(Lobby, on_delete=models.CASCADE)
    member = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('lobby', 'member')

    def __str__(self):
        return f"{self.member} in {self.lobby}"

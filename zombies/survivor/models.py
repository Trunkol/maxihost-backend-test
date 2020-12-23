from django.db import models
from django.contrib.gis.db import models as postgis_models
from users.models import User

class Survivor(models.Model):
    name = models.TextField("Name")
    gender = models.TextField("Gender")
    localization = postgis_models.PointField()
    infected = models.BooleanField('Infected', default=False)
    created = models.DateTimeField(auto_now_add=True)
    latitude = models.DecimalField(decimal_places=6,max_digits=10)
    longitude =  models.DecimalField(decimal_places=6,max_digits=10)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def evaluate_infection(self):
        infected_times = InfectedSurvivor.objects.filter(survivor_infected=self).count()
        if infected_times > 2:
            self.infected = True
            self.save()
        
class InfectedSurvivor(models.Model):
    reported_by = models.ForeignKey(Survivor, on_delete=models.CASCADE, related_name='reported_by')
    survivor_infected = models.ForeignKey(Survivor, on_delete=models.CASCADE, related_name='survivor_infected')

    class Meta:
        unique_together = ('reported_by', 'survivor_infected')
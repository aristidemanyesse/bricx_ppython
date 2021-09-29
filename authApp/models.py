from django.db import models
from coreApp.models import BaseModel
from organisationApp.models import Employe, Agence
from django.contrib.auth.models import User, Permission


class ForgotPassword(BaseModel):
    email       = models.EmailField(null = False, blank = False)
    finished_at = models.DateTimeField(default = "")
    is_validate = models.BooleanField(default = False)
    employe     = models.ForeignKey(Employe, on_delete = models.CASCADE, blank = True, null = True, related_name="employe_forgotpassword")

    def __str__(self):
        return self.email



class AccesAgence(BaseModel):
    agence = models.ForeignKey(Agence, on_delete = models.CASCADE, related_name="agence_acces")
    employe = models.ForeignKey(Employe, on_delete = models.CASCADE, related_name="employe_acces")

    def __str__(self):
        return self.employe.first_name + " " + self.employe.last_name + " dans " + self.agence.name


######################################################################################################
##### SIGNAUX



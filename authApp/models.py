from django.db import models
from django.contrib.auth.models import User, Permission

import productionApp.models as production_models
import organisationApp.models as organisation_models
import clientApp.models as client_models
import coreApp.models as core_models
import comptabilityApp.models as comptability_models

class ForgotPassword(core_models.BaseModel):
    email       = models.EmailField(null = False, blank = False)
    finished_at = models.DateTimeField(default = "")
    is_validate = models.BooleanField(default = False)
    employe     = models.ForeignKey(organisation_models.Employe, on_delete = models.CASCADE, blank = True, null = True, related_name="employe_forgotpassword")

    def __str__(self):
        return self.email



class AccesAgence(core_models.BaseModel):
    agence = models.ForeignKey(organisation_models.Agence, on_delete = models.CASCADE, related_name="agence_acces")
    employe = models.ForeignKey(organisation_models.Employe, on_delete = models.CASCADE, related_name="employe_acces")

    def __str__(self):
        return self.employe.first_name + " " + self.employe.last_name + " dans " + self.agence.name


######################################################################################################
##### SIGNAUX



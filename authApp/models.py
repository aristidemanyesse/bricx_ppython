from django.db import models
from coreApp.models import BaseModel
from organisationApp.models import Employe

class ForgotPassword(BaseModel):
    email       = models.EmailField(null = False, blank = False)
    finished_at = models.DateTimeField(default = "")
    is_validate = models.BooleanField(default = False)
    employe     = models.ForeignKey(Employe, on_delete = models.CASCADE, blank = True, null = True, related_name="employe_forgotpassword")

    def __str__(self):
        return self.email



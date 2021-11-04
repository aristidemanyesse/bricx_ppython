from django.contrib.admin.models import LogEntry, ADDITION, CHANGE, DELETION 
from django.db import models
import uuid,inspect,  os
from django.db.models.signals import pre_save, post_save
from django.dispatch.dispatcher import receiver
from django.contrib.contenttypes.models import ContentType

# Create your models here.


class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    deleted = models.BooleanField(default=False)
    protected = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-created_at']
        abstract = True


class Etat(models.Model):
    EN_COURS = 1
    TERMINE = 2
    ANNULE = 3

    name = models.CharField(max_length=255)
    etiquette = models.CharField(max_length=255)
    classe = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.name


class History(LogEntry):
    created_at = models.DateTimeField(auto_now_add=True)

class MyCodeException:
    ERROR = 401
    ERROR_MIDDLEWARE = 402
    USER_NOT_CONNECTED = 403
    PAGE_NOT_FOUND = 404
    SAME_PASSWORDS = 405
    BAD_PASSWORD = 406
    USERNAME_ALREADY_EXISTS = 407

    ACCESS_DENIED = 500
    BAD_CREDENTIALS = 501
    USER_PASSWORD_NOT_CHANGED = 502
    NOT_OR_BAD_TOKEN = 503
    CHANGING_PASSWORD_EXPIRED = 504

    SENDING_ERROR_MAIL = 600

    LOW_AVAILABLE_VOLUME = 800
    SCISSION_WITH_NULL_VOLUME = 801
    SAME_VOLUME = 802
    OPERATION_VOLUME_SIZE_NULL = 803

    class Meta:
        abstract = True


################################################################################################


@receiver(post_save)
def post_save(sender, instance, created, **kwargs):
    if issubclass(sender, BaseModel):
        user = None
        for entry in reversed(inspect.stack()):
            if "request" in entry[0].f_locals:
                if hasattr(entry[0].f_locals['request'], "user") :
                    user = entry[0].f_locals['request'].user
                    break

    # if created:
    #     if user is not None:
    #         History.objects.log_action(
    #             user_id=user,
    #             content_type_id=ContentType.objects.get_for_model(instance).pk,
    #             object_repr=instance, #or any field you wish to represent here
    #             object_id=instance.id,
    #             message="Nouvel enregistrement", # a new user has been added
    #             action_flag=ADDITION) # assuming it's a new object
    # else:
    #     if not instance.deleted:
    #         History.objects.log_action(
    #             user_id=user,
    #             content_type_id=ContentType.objects.get_for_model(instance).pk,
    #             object_repr=instance, #or any field you wish to represent here
    #             object_id=instance.id,
    #             message="Mise à jour de l'enregistrement", # a new user has been added
    #             action_flag=CHANGE) # assuming it's a new object
    #     else:
    #         History.objects.log_action(
    #             user_id=user,
    #             content_type_id=ContentType.objects.get_for_model(instance).pk,
    #             object_repr=instance, #or any field you wish to represent here
    #             object_id=instance.id,
    #             message="Suppression de l'élément", # a new user has been added
    #             action_flag=DELETION) # assuming it's a new object



 
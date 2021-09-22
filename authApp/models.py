from organisationApp.models import Agence
from django.db import models
from coreApp.models import BaseModel, MyCodeException
from django.contrib.auth.models import User
import uuid, datetime
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver









# @receiver(post_save, sender = Employe)
# def post_save_employe(sender, created, instance, **kwargs):
#     if created :
#         try:
#             instance.groups.clear()
#             group = get_admin_group(UserGroup, instance.enterprise)
#             employes = Employe.objects.filter(enterprise = instance.enterprise)
#             if len(employes) == 1:
#                 group = get_admin_group(UserGroup, instance.enterprise)
#             else:
#                 group = get_default_group(UserGroup, instance.enterprise)
#                 SendMail.send_mail(Employe, instance.email, SendMail.NEW_USER_MAIL, password = "")

#             instance.groups.add(group)
            
#             if instance.enterprise.is_private_entreprise and len(employes) == 1:
#                 SendMail.send_mail(Employe, instance.email, SendMail.NEW_USER_MAIL, password = "")

#         except Exception as e:
#             print("-----------------------------------", e)
#             raise Exception(MyCodeException.ERROR)



# @receiver(pre_save, sender = Enterprise)
# def pre_save_enterprise(sender, instance, **kwargs):
#     instance.image_url = b64_to_image(instance.img_to_base64)




# @receiver(post_save, sender = Enterprise)
# def post_save_enterprise(sender, created, instance, **kwargs):
#     if created: 
#         create_defaults_groups(UserGroup, instance)
#         if not(instance.is_private_entreprise):
#             create_default_user(Employe, instance)




# @receiver(pre_save, sender = UserGroup)
# def pre_save_group(sender, instance, **kwargs):
#     rand = uuid.uuid4()
#     if instance.id  == None :
#         instance.name = uuid.uuid4()



@receiver(pre_save, sender = ForgotPassword)
def pre_save_forgotpassword(sender, instance, **kwargs):
    if instance._state.adding:
        try:
            #supprime les anciennes demandes non validées de l'utiliateur
            ForgotPassword.objects.filter(email = instance.email, is_validate = False, deleted=False).update(deleted=True)

            #Enregistrement de la nouvelle demande
            user = Employe.objects.get(email = instance.email)
            instance.employe = user
            instance.finished_at = datetime.datetime.now() + datetime.timedelta(hours=4)
        except Exception as e:
            print("-----------------------------------", e)
            raise Exception(MyCodeException.BAD_CREDENTIALS)
    


@receiver(post_save, sender = ForgotPassword)
def post_save_forgotpassword(sender, created, instance, **kwargs):
    if created :
        pass
        #SendMail.send_mail(Employe, instance.email, SendMail.CHANGING_PASSWORD_MAIL, demande_id = instance.id)




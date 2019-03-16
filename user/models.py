from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from bootstrap_datepicker_plus import DatePickerInput
# Create your models here.
def upload_to(instance,filename):
    return '%s/%s/%s'%('profile_photo',instance.user.userprofile,filename)


class UserProfile(models.Model):

    MAN='E'
    FEMALE='K'
    OTHER='O'

    SEX={(MAN,'Erkek'),(FEMALE,'Kadın'),(OTHER,'Diğer')}

    user=models.OneToOneField(User,on_delete=models.CASCADE,blank=True,null=True)
    phone=models.CharField(max_length=11,verbose_name='Telefon Numarası',blank=True)
    sex=models.CharField(max_length=1,default=3,choices=SEX,verbose_name='Cinsiyet',blank=True)
    biography=models.TextField(max_length=500,verbose_name='Hakkımda',blank=True)
    birth_date=models.DateField(verbose_name='Doğum Tarihi',blank=True,null=True)
    profile_photo=models.ImageField(verbose_name='Profil Fotoğrafı',upload_to=upload_to,blank=True)



    def get_image_or_default(self):
        if self.profile_photo and hasattr(self.profile_photo, 'url'):  # HTML dosyasının içinde if kullandım daha güzel oldu
            return self.profile_photo.url
        return '/static/img/default-user-profile.png'

    def get_fullname_or_username(self):
        if self.user.get_full_name():
            return self.user.get_full_name()
        return self.user.username

    def __str__(self):
            return "%s Profili"%(self.get_fullname_or_username())


    class Meta:
        verbose_name_plural='Kullanıcı Bilgileri'

def create_user_profile(instance,created,**kwargs):
    if created:
        UserProfile.objects.create(user=instance)

    post_save.connect(receiver=create_user_profile,sender=User)
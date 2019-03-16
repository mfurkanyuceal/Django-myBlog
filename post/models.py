from django.db import models
from django.utils.text import slugify
from ckeditor.fields import RichTextField
from django.contrib.auth.models import User

# Create your models here.

def upload_to(instance,filename):
    return '%s/%s/%s'%('posts',instance.slug,filename)



class Category(models.Model):
    category_name = models.CharField(max_length=120)

    def __str__(self):
        return "%s" % (self.category_name)

    class Meta:
        verbose_name_plural = 'Kategoriler'
        verbose_name = 'Kategori'

#Choice alanını if ler falan değil de daha düzgün yönetmek için
class PostManager(models.Manager):
    def activate(self,*args,**kwargs):
        return super(PostManager, self).filter(draft=False)
    def draft(self,*args,**kwargs):
        return super(PostManager,self).filter(draft=True)


class Post(models.Model):

    user=models.ForeignKey(User,default=1,null=True,related_name='posts',verbose_name='Kullanıcı',on_delete=models.CASCADE)
    category = models.ManyToManyField(Category, related_name='post', verbose_name='Kategoriler')
    title = models.CharField(max_length=120, blank=False, verbose_name='Başlık')
    #content = models.TextField(verbose_name='İçerik', help_text='İçerik giriniz')
    content = RichTextField(verbose_name='İçerik')
    img = models.ImageField(blank=True, verbose_name='Fotoğraf',upload_to=upload_to)
    draft = models.BooleanField(default=False, verbose_name='Taslak Oluştursun mu?')
    created_date = models.DateTimeField(auto_now_add=True)  # Sadece ilk oluşturduğumuzda
    updated_date = models.DateTimeField(auto_now=True)  # Her kayıt işleminde
    slug = models.SlugField(max_length=122, unique=True,default='', null=False, verbose_name='Slug Alanı', editable=False)
    #object=PostManager()//Burada choice işlemini daha düzgün bir yapıyla kullanmak için ekledik

    def __str__(self):
        return "%s" % (self.title)

    def get_image_or_default(self):
        if self.img and hasattr(self.img, 'url'):  # HTML dosyasının içinde if kullandım daha güzsel oldu
            return self.img.url
        return '/static/img/default.png'

    def unique_slug(self, newSlug,originalSlug, index):
        if Post.objects.filter(slug=newSlug):
            index += 1
            newSlug = '%s-%s' % (originalSlug, index)
            return self.unique_slug(newSlug=newSlug,originalSlug=originalSlug, index=index)

        return newSlug


    def save(self, *args, **kwargs):
        if self.slug == '':
            index = 1
            text='%s-%s'%(self.title,index)
            newSlug = slugify(text)
            self.slug = self.unique_slug(newSlug=newSlug,originalSlug=newSlug, index=index)
        super(Post, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "Gönderi"
        verbose_name_plural = "Gönderiler"
        ordering = ['-created_date']  # id nin önüne - falan koyabiliriz, created_date de kullanılabilir


class Comment(models.Model):
    post=models.ForeignKey(Post,verbose_name='post',related_name='comment',on_delete=models.CASCADE)
    user=models.ForeignKey(User,verbose_name='User',related_name='usercomment',default=1,on_delete=models.CASCADE)
    content=models.TextField(verbose_name='Yorum',max_length=1000)
    time = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Yorum'
        verbose_name_plural='Yorumlar'
        ordering=['-time']


    def __str__(self):
        return "%s - %s"%(self.post,self.user)


class CommentChild(models.Model):
    comment=models.ForeignKey(Comment,related_name='comment_child',on_delete=models.CASCADE)
    user=models.ForeignKey(User,related_name='comment_user',on_delete=models.CASCADE)
    content=models.TextField(max_length=1000,verbose_name='content')
    date=models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural='Cocuk Yorumlar'
        ordering=['-date']


    def __str__(self):
        return "%s"%(self.comment)
from django import forms
from .models import Post
from .models import Comment

class PostForm(forms.ModelForm):
    # title=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    # content=forms.CharField(widget=forms.Textarea(attrs={'class':'form-control'}))

    class Meta:
        model = Post
        fields=['title','category','img','content','draft']



    def __init__(self,*args,**kwargs):
        super(PostForm,self).__init__(*args,**kwargs)

        for field in self.fields:
            self.fields[field].widget.attrs={'class':'form-control'}
        self.fields['draft'].widget.attrs['class']=''
        self.fields['content'].widget.attrs['rows']=10
        self.fields['content'].widget.attrs['cols']=50
        self.fields['img'].widget.attrs['class']=''

    def clean_title(self):
        title = self.cleaned_data['title']

        if title.isdigit():
            raise forms.ValidationError('Lütfen sadece sayı girişi yapmayınız')


        if '@' in title:
            raise forms.ValidationError('Lütfen @ işareti girmeyiniz')


        return title


class PostFilterForm(forms.Form):
    OPTIONS = (('H','Hepsi'),('T','Taslak'),('TD','Taslak Değil'))

    choice=forms.CharField(label='Filtre',widget=forms.Select(choices=OPTIONS,attrs={'class':'form-control'}))


class CommentForm(forms.ModelForm):

    def __init__(self,*args,**kwargs):
        super(CommentForm,self).__init__(*args,**kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs={'class':'form-control'}

        self.fields['content'].widget.attrs['rows'] = 10
        self.fields['content'].widget.attrs['cols'] = 50
        self.fields['content'].widget.attrs['placeholder'] = 'Yorumunuzu yazınız...'

    class Meta:
        model=Comment
        fields=['content']


    def clean_name_lastname(self):
        name_lastname = self.cleaned_data['name_lastname']

        if not name_lastname.isalpha:
            raise forms.ValidationError('Lütfen sadece karakter giriniz')
        return name_lastname
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import get_user_model
from django import forms
from django.core.validators import RegexValidator

User = get_user_model()
class LoginForm(forms.ModelForm):
        email=forms.EmailField(
            max_length=255
           )
        password = forms.CharField(widget=forms.PasswordInput)
        email.widget.attrs.update({'placeholder':'Enter Email','class':'input'})
        password.widget.attrs.update({'placeholder':'Password','class':'input'})
        class Meta:
            model=User
            fields = ['email','password']

        def clean_email(self):
            '''
            Verify email is available.
            '''
            email = self.cleaned_data.get('email')
            qs = User.objects.filter(email=email)
            if qs.exists():
                raise forms.ValidationError("email is taken")
            return email

class RegisterForm(UserCreationForm):
        fullname = forms.CharField(max_length=50)
        email=forms.EmailField(
            max_length=255
           )
        phone = forms.CharField(validators=[RegexValidator('^[+250]*[0-9]{9}$',message='phone must be rwandan and start with +250')])
        password1 = forms.CharField(widget=forms.PasswordInput)
        password2 = forms.CharField(widget=forms.PasswordInput)
        fullname.widget.attrs.update({'placeholder':'Enter name','class':'input'})
        email.widget.attrs.update({'placeholder':'Enter Email','class':'input'})
        phone.widget.attrs.update({'placeholder':'+250 - - - - - - - - -','class':'input','value':'+250 - - - - - - - - -'})
        password1.widget.attrs.update({'placeholder':'Password','class':'input'})
        password2.widget.attrs.update({'hidden':'true'})
        class Meta:
            model=User
            fields = ['fullname','email','phone','password1','password2']

        def clean_email(self):
            '''
            Verify email is available.
            '''
            email = self.cleaned_data.get('email')
            qs = User.objects.filter(email=email)
            if qs.exists():
                raise forms.ValidationError("email is taken")
            return email

    
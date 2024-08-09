from django.contrib.auth.forms import UserCreationForm, PasswordResetForm
from django.core.exceptions import ValidationError

from .models import *
from django import forms


class ForgotPasswordForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('email',)

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email:
            if not User.objects.filter(email=email).exists():
                raise forms.ValidationError(u'Email address does not exist.')
        else:
            raise forms.ValidationError(u'This field is required.')
        return email


class EmailValidationOnForgotPassword(PasswordResetForm):
    def clean_email(self):
        print("here")
        email = self.cleaned_data['email']
        if not User.objects.filter(email__iexact=email).exists():
            raise ValidationError("Email address does not exist!")
            print("here")
        return email


class UserLoginForm(forms.ModelForm):
    remember_me = forms.BooleanField(required=False)

    class Meta:
        model = User
        fields = ('email', 'password', 'remember_me', )

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not email:
            raise forms.ValidationError(u'This field is required.')
        if not User.objects.filter(email=email.lower()).exists():
            raise forms.ValidationError(u'Email address does not exist.')
        return email.lower()


class UserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'password1', 'password2', )

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email and User.objects.filter(email=email).exists():
            raise forms.ValidationError(u'Email address already exists.')
        if not email:
            raise forms.ValidationError(u'This field is required.')
        return email

    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')
        if not first_name:
            raise forms.ValidationError(u'This field is required.')
        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name')
        if not last_name:
            raise forms.ValidationError(u'This field is required.')
        return last_name


class ProfileForm(forms.ModelForm):
    is_validated = forms.CharField()
    class Meta:
        model = UserProfile
        fields = ('cell_phone', 'is_validated')

    def clean(self):
        cell_phone = self.cleaned_data.get('cell_phone')
        print(cell_phone)
        if not cell_phone:
            raise forms.ValidationError(u'This field is required.')
        if self.cleaned_data.get('is_validated') != 'valid':
            raise forms.ValidationError(self.cleaned_data.get('is_validated'))
        return self.cleaned_data


class UpdateProfileForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', )

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not email:
            raise forms.ValidationError(u'This field is required')
        return email

    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')
        if not first_name:
            raise forms.ValidationError(u'This field is required')
        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name')
        if not last_name:
            raise forms.ValidationError(u'This field is required')
        return last_name


class UpdateProfileForm2(forms.ModelForm):
    landline_phone = forms.CharField(required=False)
    profile_image = forms.ImageField(required=False)
    # is_validated = forms.CharField()
    is_validated2 = forms.CharField()

    class Meta:
        model = UserProfile
        fields = ('address', 'profile_image', 'city', 'state', 'zip', 'landline_phone', 'cell_phone', 'is_validated2', )

    def clean_address(self):
        address = self.cleaned_data.get('address')
        if not address:
            raise forms.ValidationError(u'This field is required')
        return address

    def clean_city(self):
        city = self.cleaned_data.get('city')
        if not city:
            raise forms.ValidationError(u'This field is required')
        return city

    def clean_state(self):
        state = self.cleaned_data.get('state')
        if not state:
            raise forms.ValidationError(u'This field is required')
        return state

    def clean_zip(self):
        zip = self.cleaned_data.get('zip')
        if not zip:
            raise forms.ValidationError(u'This field is required')
        if len(zip) < 5:
            raise forms.ValidationError(u'Too Short')
        return zip

    def clean(self):
        cell_phone = self.cleaned_data.get('cell_phone')
        landline_phone = self.cleaned_data.get('landline_phone')
        print(cell_phone)
        print(len(landline_phone))
        if not cell_phone:
            if landline_phone and len(landline_phone) < 12:
                raise ValidationError({
                    'landline_phone': forms.ValidationError('Too Short.'),
                    'cell_phone': forms.ValidationError('This field is required.'),
                })
            else:
                raise ValidationError({
                    'cell_phone': forms.ValidationError('This field is required.')
                })
        elif self.cleaned_data.get('is_validated2') != 'valid':
            if landline_phone and len(landline_phone) < 12:
                raise ValidationError({
                    'cell_phone': forms.ValidationError(self.cleaned_data.get('is_validated2')),
                    'landline_phone': forms.ValidationError('Too Short.'),
                })
            else:
                raise ValidationError({
                    'cell_phone': forms.ValidationError(self.cleaned_data.get('is_validated2'))
                })
        else:
            if landline_phone and len(landline_phone) < 12:
                raise ValidationError({'landline_phone': forms.ValidationError('Too Short.')})
        return self.cleaned_data


class ChangePasswordForm(forms.Form):
    old_password = forms.CharField(max_length=30)
    new_password = forms.CharField(max_length=30)
    confirm_new_password = forms.CharField(max_length=30)

    # def clean(self):
    #     new_password = self.cleaned_data.get('new_password')
    #     confirm_new_password = self.cleaned_data.get('confirm_new_password')
    #     current_password = self.cleaned_data.get('old_password')
    #
    #     if new_password and confirm_new_password and current_password:
    #         if new_password == current_password:
    #             raise forms.ValidationError(u'Current and New Password are same!')
    #         elif new_password != confirm_new_password:
    #             raise forms.ValidationError(u"Password and Confirm Password didn't match")
    #         elif new_password.isnumeric():
    #             raise forms.ValidationError(u'Your password cannot be entirely numeric.')
    #         elif len(new_password) < 8:
    #             raise forms.ValidationError(u'Your password must contain at least 8 characters.')
    #     return self.cleaned_data


class AddUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'password1', 'password2',)

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email and User.objects.filter(email=email).exists():
            raise forms.ValidationError(u'Email address already exists.')
        if not email:
            raise forms.ValidationError(u'This field is required.')
        return email

    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')
        if not first_name:
            raise forms.ValidationError(u'This field is required.')
        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name')
        if not last_name:
            raise forms.ValidationError(u'This field is required.')
        return last_name


class UpdateUserForm(forms.ModelForm):
    password1 = forms.CharField(required=False, widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput, required=False)
    key = forms.IntegerField()

    class Meta:
        model = User
        fields = ('key', 'first_name', 'last_name', 'email', 'password1', 'password2')

    def clean(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        key = self.cleaned_data.get('key')
        email = self.cleaned_data.get('email')
        if password1:
            if password2:
                if password1 != password2:
                    raise ValidationError({
                        'password2': forms.ValidationError("Password mismatch")
                    })
            else:
                raise ValidationError({
                    'password2': forms.ValidationError("Please enter confirm password")
                })
        elif password2:
            raise ValidationError({
                'password': forms.ValidationError("Please enter password")
            })
        user = User.objects.get(id=key)
        # user = profile.user
        print(key)
        print(user)
        if user.email != email and User.objects.filter(email=email).exists():
            raise ValidationError({
                'email': forms.ValidationError("Email address already exists.")
            })
        return self.cleaned_data


    def clean_email(self):
        print("in clean method")
        email = self.cleaned_data.get('email')
        print("printing email")
        # all_users = User.objects.filter()
        print(email)
        # if email and User.objects.filter(email=email).exists():
        #     raise forms.ValidationError(u'Email address already exists.')
        if not email:
            raise forms.ValidationError(u'This field is required.')
        return email

    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')
        if not first_name:
            raise forms.ValidationError(u'This field is required.')
        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name')
        if not last_name:
            raise forms.ValidationError(u'This field is required.')
        return last_name


class AddProfileForm(forms.ModelForm):
    is_validated = forms.CharField()

    class Meta:
        model = UserProfile
        fields = ('cell_phone', 'status', 'is_validated')

    def clean(self):
        cell_phone = self.cleaned_data.get('cell_phone')
        if not cell_phone:
            raise ValidationError({
                'cell_phone': forms.ValidationError('This field is required.'),
            })
        elif self.cleaned_data.get('is_validated') != 'valid':
            raise ValidationError({
                'cell_phone': forms.ValidationError(self.cleaned_data.get('is_validated'))
            })
        return self.cleaned_data


class PermissionForm(forms.ModelForm):
    class Meta:
        model = Permissions
        fields = '__all__'


class AddBlockForm(forms.ModelForm):
    class Meta:
        model = Dashboard
        fields = '__all__'


class EmailTemplateForm(forms.ModelForm):
    class Meta:
        model = WelcomeEmail
        fields = '__all__'


class SendEmailTemplateForm(forms.ModelForm):
    email_to = forms.CharField(max_length=250)

    class Meta:
        model = WelcomeEmail
        fields = ('email_from', 'email_content', 'email_to')

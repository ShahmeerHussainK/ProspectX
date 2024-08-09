
from django.db import migrations


def user_data_migrations(apps, schema_editor):
    # We can't import the Person model directly as it may be a newer
    # version than this migration expects. We use the historical version.
    User = apps.get_model('auth', 'User')
    Profile = apps.get_model('user', 'UserProfile')
    Role = apps.get_model('user', 'Role')
    Permissions = apps.get_model('user', 'Permissions')
    WelcomeEmail = apps.get_model('user', 'WelcomeEmail')
    EmailContent = apps.get_model('user', 'EmailContent')

    role = Role.objects.create(role_name="Super User")
    Role.objects.create(role_name="Admin User")
    Role.objects.create(role_name="Sub User")

    permission = Permissions.objects.create()

    for user in User.objects.all():
        if not Profile.objects.filter(user=user).exists():
            Profile.objects.create(user=user, email_confirmed=True,
                                   role=role,
                                   permissions=permission,
                                   status="active",
                                   email_verified=True)

    WelcomeEmail.objects.create(email_from="muhammad.tahir@argonteq.com",
                                email_content="Dear %first_name%&nbsp;%last_name%;<br><br>Welcome. To access your account, please log into our secure portal:<br><a data-cke-saved-href=\"https://app.stackmylist.com/site/login\" href=\"http://18.223.227.40/\" target=\"_blank\">Login now</a><br>Your Email id : %email%<br>Your Password :&nbsp;%password%<br>Your phone number : %phone%<br>From there, you can access your account and&nbsp;manage property&nbsp;addresses.<br><br>Sincerely,<br>ProspectX")

    EmailContent.objects.create(email_content="This mail is from prospectx team")


class Migration(migrations.Migration):
    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(user_data_migrations),
    ]

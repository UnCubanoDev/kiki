from django.db import migrations, models
import django.contrib.auth.models
import django.contrib.auth.validators
import django.core.validators
import django.utils.timezone

class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()])),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now)),
                ('phone', models.CharField(max_length=18, unique=True, validators=[django.core.validators.RegexValidator('^\\+[1-9]\\d{1,14}$', 'phone number in the format')])),
                ('groups', models.ManyToManyField(blank=True, to='auth.group')),
                ('user_permissions', models.ManyToManyField(blank=True, to='auth.permission')),
            ],
            options={
                'app_label': 'directorio',
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=240, verbose_name='name')),
                ('details', models.CharField(max_length=240, verbose_name='details')),
                ('long', models.CharField(max_length=50, verbose_name='longitude')),
                ('lat', models.CharField(max_length=50, verbose_name='latitude')),
                ('receiver_name', models.CharField(blank=True, max_length=80, null=True, verbose_name='reciever name')),
                ('phone', models.CharField(blank=True, max_length=18, null=True, verbose_name='phone number')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='directorio.user')),
            ],
            options={
                'verbose_name': 'address',
                'verbose_name_plural': 'addresses',
            },
        ),
    ]
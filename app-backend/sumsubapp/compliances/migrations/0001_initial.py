# Generated by Django 5.0.4 on 2024-08-23 21:54

import django.db.models.deletion
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('street', models.CharField(default='', max_length=100)),
                ('substreet', models.CharField(default='', max_length=100)),
                ('town', models.CharField(default='', max_length=100)),
                ('state', models.CharField(default='', max_length=100)),
                ('post_code', models.CharField(default='', max_length=100)),
                ('country', models.CharField(default='', max_length=3)),
            ],
        ),
        migrations.CreateModel(
            name='FixedInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(default='', max_length=100)),
                ('middle_name', models.CharField(default='', max_length=100)),
                ('last_name', models.CharField(default='', max_length=100)),
                ('legal_name', models.CharField(default='', max_length=100)),
                ('gender', models.CharField(choices=[('M', 'M'), ('F', 'F')], max_length=2)),
                ('dob', models.DateField()),
                ('place_of_birth', models.CharField(default='', max_length=100)),
                ('country_of_birth', models.CharField(default='', max_length=3)),
                ('state_of_birth', models.CharField(default='', max_length=100)),
                ('country', models.CharField(default='', max_length=3)),
                ('nationality', models.CharField(default='', max_length=3)),
                ('tin', models.CharField(default='', max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Metadata',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_doc_type', models.CharField(choices=[('ID_CARD', 'ID_CARD'), ('PASSPORT', 'PASSPORT'), ('DRIVERS', 'DRIVERS'), ('RESIDENCE_PERMIT', 'RESIDENCE_PERMIT'), ('UTILITY_BILL', 'UTILITY_BILL'), ('SELFIE', 'SELFIE'), ('VIDEO_SELFIE', 'VIDEO_SELFIE'), ('PROFILE_IMAGE', 'PROFILE_IMAGE'), ('ID_DOC_PHOTO', 'ID_DOC_PHOTO'), ('AGREEMENT', 'AGREEMENT'), ('CONTRACT', 'CONTRACT'), ('DRIVERS_TRANSLATION', 'DRIVERS_TRANSLATION'), ('INVESTOR_DOC', 'INVESTOR_DOC'), ('VEHICLE_REGISTRATION_CERTIFICATE', 'VEHICLE_REGISTRATION_CERTIFICATE'), ('INCOME_SOURCE', 'INCOME_SOURCE'), ('PAYMENT_METHOD', 'PAYMENT_METHOD'), ('BANK_CARD', 'BANK_CARD'), ('COVID_VACCINATION_FORM', 'COVID_VACCINATION_FORM'), ('OTHER', 'OTHER')], max_length=50)),
                ('id_doc_sub_type', models.CharField(choices=[('FRONT_SIDE', 'FRONT_SIDE'), ('BACK_SIDE', 'BACK_SIDE'), ('null', 'null')], max_length=20)),
                ('country', models.CharField(max_length=3)),
                ('first_name', models.CharField(default='', max_length=100)),
                ('middle_name', models.CharField(default='', max_length=100)),
                ('last_name', models.CharField(default='', max_length=100)),
                ('issued_date', models.DateField()),
                ('valid_until', models.DateField()),
                ('number', models.CharField(default='', max_length=100)),
                ('dob', models.DateField()),
                ('place_of_birth', models.CharField(default='', max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='CompanyInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company_name', models.CharField(max_length=100)),
                ('registration_number', models.CharField(default='', max_length=100)),
                ('country', models.CharField(max_length=3)),
                ('legal_address', models.CharField(default='', max_length=100)),
                ('incorporated_on', models.DateField()),
                ('type', models.CharField(choices=[('Private Company Limited by Shares', 'Private Company Limited by Shares'), ('Public Limited Company', 'Public Limited Company'), ('Limited Partnership', 'Limited Partnership')], max_length=100)),
                ('email', models.EmailField(default='', max_length=254)),
                ('phone', models.CharField(default='', max_length=100)),
                ('control_scheme', models.CharField(default='', max_length=100)),
                ('tax_id', models.CharField(default='', max_length=100)),
                ('registration_location', models.CharField(default='', max_length=100)),
                ('website', models.CharField(default='', max_length=100)),
                ('postal_address', models.CharField(default='', max_length=100)),
                ('no_ubos', models.BooleanField(default=True)),
                ('no_shareholders', models.BooleanField(default=True)),
                ('address', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='compliances.address')),
            ],
        ),
        migrations.CreateModel(
            name='Beneficiary',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('applicant_id', models.CharField(max_length=100)),
                ('type', models.CharField(choices=[('shareholder', 'shareholder'), ('ubo', 'ubo'), ('representative', 'representative'), ('director', 'director')], max_length=15)),
                ('share_size', models.BigIntegerField(default=0)),
                ('in_registry', models.BooleanField(default=True)),
                ('company_info', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='company_info_beneficiaries', to='compliances.companyinfo')),
            ],
        ),
        migrations.CreateModel(
            name='Applicant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('external_id', models.UUIDField(default=uuid.uuid4, editable=False)),
                ('source_key', models.CharField(default='', max_length=100)),
                ('email', models.EmailField(default='', max_length=254)),
                ('phone', models.CharField(default='', max_length=100)),
                ('lang', models.CharField(choices=[('en', 'English'), ('fr', 'French')], default='en', max_length=2)),
                ('type', models.CharField(choices=[('company', 'company'), ('individual', 'individual')], max_length=100)),
                ('applicant_id', models.CharField(default='', max_length=50)),
                ('account', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('company_info', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='compliances.companyinfo')),
                ('fixed_info', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='compliances.fixedinfo')),
            ],
        ),
        migrations.CreateModel(
            name='FixedInfoAddress',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('country', models.CharField(default='', max_length=3)),
                ('post_code', models.CharField(default='', max_length=100)),
                ('town', models.CharField(default='', max_length=100)),
                ('street', models.CharField(max_length=100)),
                ('substreet', models.CharField(default='', max_length=100)),
                ('state', models.CharField(default='', max_length=100)),
                ('building_name', models.CharField(default='', max_length=100)),
                ('flat_number', models.CharField(default='', max_length=100)),
                ('building_number', models.CharField(default='', max_length=100)),
                ('fixed_info', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='fixed_info_addresses', to='compliances.fixedinfo')),
            ],
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image_id', models.CharField(default='', max_length=100)),
                ('beneficiary', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='beneficiary_images', to='compliances.beneficiary')),
            ],
        ),
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.FileField(upload_to='')),
                ('applicant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='applicant_documents', to='compliances.applicant')),
                ('metadata', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='compliances.metadata')),
            ],
        ),
        migrations.CreateModel(
            name='Position',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('position', models.CharField(choices=[('director', 'director'), ('shareholder', 'shareholder'), ('other', 'other')], max_length=100)),
                ('beneficiary', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='beneficiary_positions', to='compliances.beneficiary')),
            ],
        ),
    ]

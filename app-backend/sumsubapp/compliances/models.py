from django.db import models


# Create your models here.


class Address(models.Model):
    street = models.CharField(max_length=100, default='')
    substreet = models.CharField(max_length=100, default='')
    town = models.CharField(max_length=100, default='')
    state = models.CharField(max_length=100, default='')
    post_code = models.CharField(max_length=100, default='')
    country = models.CharField(max_length=3, default='')  # Alpha-3 country code


class CompanyInfo(models.Model):
    TYPE_CHOICES = [
        ('Private Company Limited by Shares', 'Private Company Limited by Shares'),
        ('Public Limited Company', 'Public Limited Company'),
        ('Limited Partnership', 'Limited Partnership'),
    ]
    company_name = models.CharField(max_length=100)
    registration_number = models.CharField(max_length=100, default='')
    country = models.CharField(max_length=3)  # Alpha-3 country code
    legal_address = models.CharField(max_length=100, default='')
    address = models.OneToOneField(Address, on_delete=models.CASCADE)
    incorporated_on = models.DateField()
    type = models.CharField(max_length=100, choices=TYPE_CHOICES)
    email = models.EmailField(default='')
    phone = models.CharField(max_length=100, default='')
    control_scheme = models.CharField(max_length=100, default='')
    tax_id = models.CharField(max_length=100, default='')
    registration_location = models.CharField(max_length=100, default='')
    website = models.CharField(max_length=100, default='')
    postal_address = models.CharField(max_length=100, default='')
    no_ubos = models.BooleanField(default=True)
    no_shareholders = models.BooleanField(default=True)


class Beneficiary(models.Model):
    TYPE_CHOICES = [
        ('shareholder', 'shareholder'),
        ('ubo', 'ubo'),
        ('representative', 'representative'),
        ('director', 'director'),
    ]
    applicant_id = models.CharField(max_length=100)
    type = models.CharField(max_length=15, choices=TYPE_CHOICES)
    share_size = models.BigIntegerField(default=0)
    in_registry = models.BooleanField(default=True)
    company_info = models.ForeignKey(CompanyInfo, on_delete=models.CASCADE, related_name='company_info_beneficiaries')


class Position(models.Model):
    POSITION_CHOICES = [
        ('director', 'director'),
        ('shareholder', 'shareholder'),
        ('other', 'other'),
    ]
    position = models.CharField(max_length=100, choices=POSITION_CHOICES)
    beneficiary = models.ForeignKey(Beneficiary, on_delete=models.CASCADE, related_name='beneficiary_positions')


class Image(models.Model):
    image_id = models.CharField(max_length=100, default='')
    beneficiary = models.ForeignKey(Beneficiary, on_delete=models.CASCADE, related_name='beneficiary_images')


class FixedInfo(models.Model):
    GENDER_CHOICES = [
        ('M', 'M'),
        ('F', 'F'),
    ]
    first_name = models.CharField(max_length=100, default='')
    middle_name = models.CharField(max_length=100, default='')
    last_name = models.CharField(max_length=100, default='')
    legal_name = models.CharField(max_length=100, default='')
    gender = models.CharField(max_length=2, choices=GENDER_CHOICES)
    dob = models.DateField()  # datetime.date(YEAR, MONTH, DAY)
    place_of_birth = models.CharField(max_length=100, default='')
    country_of_birth = models.CharField(max_length=3, default='')  # Alpha-3 country code
    state_of_birth = models.CharField(max_length=100, default='')
    country = models.CharField(max_length=3, default='')  # Alpha-3 country code
    nationality = models.CharField(max_length=3, default='')  # Alpha-3 country code
    tin = models.CharField(max_length=100, default='')  # Taxpayer Identification Number


class FixedInfoAddress(models.Model):
    country = models.CharField(max_length=3, default='')  # Alpha-3 country code
    post_code = models.CharField(max_length=100, default='')
    town = models.CharField(max_length=100, default='')
    street = models.CharField(max_length=100)
    substreet = models.CharField(max_length=100, default='')
    state = models.CharField(max_length=100, default='')
    building_name = models.CharField(max_length=100, default='')
    flat_number = models.CharField(max_length=100, default='')
    building_number = models.CharField(max_length=100, default='')
    fixed_info = models.ForeignKey(FixedInfo, on_delete=models.CASCADE, related_name='fixed_info_addresses')


class Applicant(models.Model):
    LANG_CHOICES = [
        ('en', 'English'),
        ('fr', 'French'),
    ]
    TYPE_CHOICES = [
        ('company', 'company'),
        ('individual', 'individual'),
    ]
    external_id = models.UUIDField()
    company_info = models.OneToOneField(CompanyInfo, on_delete=models.CASCADE)
    source_key = models.CharField(max_length=100, default='')
    email = models.EmailField(default='')  # not mandatory
    phone = models.CharField(max_length=100, default='')  # not mandatory
    lang = models.CharField(max_length=2, choices=LANG_CHOICES, default='en')
    fixed_info = models.OneToOneField(FixedInfo, on_delete=models.CASCADE)
    type = models.CharField(max_length=100, choices=TYPE_CHOICES)


class Metadata(models.Model):
    DOC_TYPE_CHOICES = [
        ('ID_CARD', 'ID_CARD'),
        ('PASSPORT', 'PASSPORT'),
        ('DRIVERS', 'DRIVERS'),
        ('RESIDENCE_PERMIT', 'RESIDENCE_PERMIT'),
        ('UTILITY_BILL', 'UTILITY_BILL'),
        ('SELFIE', 'SELFIE'),
        ('VIDEO_SELFIE', 'VIDEO_SELFIE'),
        ('PROFILE_IMAGE', 'PROFILE_IMAGE'),
        ('ID_DOC_PHOTO', 'ID_DOC_PHOTO'),
        ('AGREEMENT', 'AGREEMENT'),
        ('CONTRACT', 'CONTRACT'),
        ('DRIVERS_TRANSLATION', 'DRIVERS_TRANSLATION'),
        ('INVESTOR_DOC', 'INVESTOR_DOC'),
        ('VEHICLE_REGISTRATION_CERTIFICATE', 'VEHICLE_REGISTRATION_CERTIFICATE'),
        ('INCOME_SOURCE', 'INCOME_SOURCE'),
        ('PAYMENT_METHOD', 'PAYMENT_METHOD'),
        ('BANK_CARD', 'BANK_CARD'),
        ('COVID_VACCINATION_FORM', 'COVID_VACCINATION_FORM'),
        ('OTHER', 'OTHER'),
    ]

    SUB_TYPE_CHOICES = [
        ('FRONT_SIDE', 'FRONT_SIDE'),
        ('BACK_SIDE', 'BACK_SIDE'),
        ('null', 'null'),
    ]
    id_doc_type = models.CharField(max_length=50, choices=DOC_TYPE_CHOICES)  # Check Document Type
    id_doc_sub_type = models.CharField(max_length=20, choices=SUB_TYPE_CHOICES)
    country = models.CharField(max_length=3)  # Alpha-3 country code
    first_name = models.CharField(max_length=100, default='')
    middle_name = models.CharField(max_length=100, default='')
    last_name = models.CharField(max_length=100, default='')
    issued_date = models.DateField()
    valid_until = models.DateField()
    number = models.CharField(max_length=100, default='')
    dob = models.DateField()
    place_of_birth = models.CharField(max_length=100, default='')


class Document(models.Model):
    applicant_id = models.CharField(max_length=100)
    metadata = models.OneToOneField(Metadata, on_delete=models.CASCADE)
    content = models.FileField()
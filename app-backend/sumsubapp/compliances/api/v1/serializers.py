from rest_framework import serializers

from decouple import config

from sumsubapp.compliances.models import Document, Metadata, Applicant, CompanyInfo, Address, Beneficiary, Position, \
    Image, FixedInfo, FixedInfoAddress
from sumsubapp.sumsubapi.sumsub_api import SumSubAPI

api = SumSubAPI(app_token=config('SUMSUB_APP_TOKEN'), secret_key=config('SUMSUB_SECRET_KEY'))


class PositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Position
        fields = ('position',)


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ('image_id',)


class BeneficiarySerializer(serializers.ModelSerializer):
    beneficiary_positions = PositionSerializer(many=True)
    beneficiary_images = ImageSerializer(many=True)

    class Meta:
        model = Beneficiary
        fields = ('applicant_id', 'type', 'share_size', 'in_registry', 'beneficiary_positions', 'beneficiary_images')


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ('street', 'substreet', 'town', 'state', 'post_code', 'country')


class CompanyInfoSerializer(serializers.ModelSerializer):
    address = AddressSerializer(write_only=True)
    company_info_beneficiaries = BeneficiarySerializer(many=True, write_only=True)

    class Meta:
        model = CompanyInfo
        fields = ('company_name', 'registration_number', 'country', 'legal_address', 'address', 'incorporated_on',
                  'type', 'email', 'phone', 'control_scheme', 'tax_id', 'registration_location', 'website',
                  'postal_address', 'no_ubos', 'no_shareholders', 'company_info_beneficiaries')


class FixedInfoAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = FixedInfoAddress
        fields = ('country', 'post_code', 'town', 'street', 'substreet', 'state', 'building_name', 'flat_number',
                  'building_number', 'substreet')


class FixedInfoSerializer(serializers.ModelSerializer):
    fixed_info_addresses = FixedInfoAddressSerializer(many=True, write_only=True)

    class Meta:
        model = FixedInfo
        fields = ('first_name', 'middle_name', 'last_name', 'legal_name', 'gender', 'dob', 'place_of_birth',
                  'country_of_birth', 'state_of_birth', 'country', 'nationality', 'tin', 'fixed_info_addresses')


class ApplicantSerializer(serializers.ModelSerializer):
    company_info = CompanyInfoSerializer(write_only=True)
    fixed_info = FixedInfoSerializer(write_only=True)

    class Meta:
        model = Applicant
        fields = ('external_id', 'company_info', 'source_key', 'email', 'phone', 'lang', 'fixed_info', 'type')

    def create(self, validated_data):
        applicant = Applicant.objects.create(**validated_data)
        response = api.create_applicant(
            level_name='external_id', external_user_id=applicant.external_id,
            company_name=applicant.company_info.company_name,
            registration_number=applicant.company_info.registration_number,
            company_country=applicant.company_info.country, legal_address=applicant.company_info.legal_address,
            company_address=applicant.company_info.address, incorporated_on=applicant.company_info.incorporated_on,
            company_type=applicant.company_info.type, company_email=applicant.company_info.email,
            company_phone=applicant.company_info.phone, control_scheme=applicant.company_info.control_scheme,
            tax_id=applicant.company_info.tax_id, registration_location=applicant.company_info.registration_location,
            website=applicant.company_info.website, postal_address=applicant.company_info.postal_address,
            beneficiaries=applicant.company_info.company_info_beneficiaries, no_ubos=applicant.company_info.no_ubos,
            no_shareholders=applicant.company_info.no_shareholders, source_key=applicant.source_key,
            applicant_email=applicant.email, applicant_phone=applicant.phone, lang=applicant.lang,
            first_name=applicant.fixed_info.first_name, middle_name=applicant.fixed_info.middle_name,
            last_name=applicant.fixed_info.last_name, legal_name=applicant.fixed_info.legal_name,
            gender=applicant.fixed_info.gender, dob=applicant.fixed_info.dob,
            place_of_birth=applicant.fixed_info.place_of_birth, country_of_birth=applicant.fixed_info.country_of_birth,
            state_of_birth=applicant.fixed_info.state_of_birth, country=applicant.fixed_info.country,
            nationality=applicant.fixed_info.nationality, addresses=applicant.fixed_info.fixed_info_addresses,
            tin=applicant.fixed_info.tin, applicant_type=applicant.type
        )
        applicant.applicant_id = response.id
        applicant.save()
        return applicant


class FixedInfoReadSerializer(serializers.Serializer):
    firstName = serializers.CharField()
    lastName = serializers.CharField()


class IdDocSerializer(serializers.Serializer):
    idDocType = serializers.CharField()
    country = serializers.CharField()
    firstName = serializers.CharField()
    firstNameEn = serializers.CharField()
    lastName = serializers.CharField()
    lastNameEn = serializers.CharField()
    validUntil = serializers.DateField()
    number = serializers.CharField()
    dob = serializers.DateField()
    mrzLine1 = serializers.CharField()
    mrzLine2 = serializers.CharField()
    mrzLine3 = serializers.CharField()


class InfoSerializer(serializers.Serializer):
    firstName = serializers.CharField()
    firstNameEn = serializers.CharField()
    lastName = serializers.CharField()
    lastNameEn = serializers.CharField()
    dob = serializers.DateField()
    country = serializers.CharField()
    idDocs = IdDocSerializer(many=True)


class AgreementSerializer(serializers.Serializer):
    createdAt = serializers.DateTimeField()
    source = serializers.CharField()
    targets = serializers.ListField(child=serializers.CharField())


class DocSetSerializer(serializers.Serializer):
    idDocSetType = serializers.CharField()
    types = serializers.ListField(child=serializers.CharField())


class RequiredIdDocsSerializer(serializers.Serializer):
    docSets = DocSetSerializer(many=True)


class ReviewResultSerializer(serializers.Serializer):
    reviewAnswer = serializers.CharField()


class ReviewSerializer(serializers.Serializer):
    elapsedSincePendingMs = serializers.IntegerField()
    elapsedSinceQueuedMs = serializers.IntegerField()
    reprocessing = serializers.BooleanField()
    levelName = serializers.CharField()
    createDate = serializers.DateTimeField()
    reviewDate = serializers.DateTimeField()
    reviewResult = ReviewResultSerializer()
    reviewStatus = serializers.CharField()


class ApplicantReadSerializer(serializers.Serializer):
    id = serializers.CharField()
    createdAt = serializers.DateTimeField()
    clientId = serializers.CharField()
    inspectionId = serializers.CharField()
    externalUserId = serializers.CharField()
    fixedInfo = FixedInfoSerializer()
    info = InfoSerializer()
    agreement = AgreementSerializer()
    email = serializers.EmailField()
    applicantPlatform = serializers.CharField()
    requiredIdDocs = RequiredIdDocsSerializer()
    review = ReviewSerializer()
    lang = serializers.CharField()
    type = serializers.CharField()


class MetadataSerializer(serializers.ModelSerializer):
    class Meta:
        model = Metadata
        fields = ('id_doc_type', 'id_doc_sub_type', 'country', 'first_name', 'middle_name', 'last_name', 'issued_date',
                  'valid_until', 'number', 'dob', 'place_of_birth')


class DocumentSerializer(serializers.ModelSerializer):
    applicant = serializers.PrimaryKeyRelatedField(queryset=Applicant.objects.all())
    metadata = MetadataSerializer(write_only=True)

    class Meta:
        model = Document
        fields = ('applicant', 'metadata', 'content')

    def create(self, validated_data):
        document = Document.objects.create(**validated_data)
        api.add_id_document(
            applicant_id=document.applicant.applicant_id, id_doc_type=document.metadata.id_doc_type,
            id_doc_sub_type=document.metadata.id_doc_sub_type, country=document.metadata.country,
            first_name=document.metadata.first_name, middle_name=document.metadata.middle_name,
            last_name=document.metadata.last_name, issued_date=document.metadata.issued_date,
            valid_until=document.metadata.valid_until, number=document.metadata.number, dob=document.metadata.dob,
            place_of_birth=document.metadata.place_of_birth, content=document.content.file
        )
        return document


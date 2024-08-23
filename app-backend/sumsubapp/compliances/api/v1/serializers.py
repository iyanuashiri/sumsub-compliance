from rest_framework import serializers

from sumsubapp.compliances.models import Document, Metadata, Applicant, CompanyInfo, Address, Beneficiary, Position, \
    Image, FixedInfo, FixedInfoAddress


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
    company_info_beneficiaries = BeneficiarySerializer(many=True)

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
    fixed_info_addresses = FixedInfoAddressSerializer(many=True)
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


class MetadataSerializer(serializers.ModelSerializer):
    class Meta:
        model = Metadata
        fields = ('id_doc_type', 'id_doc_sub_type', 'country', 'first_name', 'middle_name', 'last_name', 'issued_date',
                  'valid_until', 'number', 'dob', 'place_of_birth')


class DocumentSerializer(serializers.ModelSerializer):
    metadata = MetadataSerializer(write_only=True)

    class Meta:
        model = Document
        fields = ('applicant_id', 'metadata', 'content')

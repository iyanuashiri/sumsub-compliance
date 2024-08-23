from rest_framework import serializers

from sumsubapp.compliances.models import Document, Metadata


class MetadataSerializer(serializers.ModelSerializer):
    class Meta:
        model = Metadata
        fields = ('id_doc_type', 'id_doc_sub_type', 'country', 'first_name', 'middle_name', 'last_name', 'issued_date',
                  'valid_until', 'number', 'dob', 'place_of_birth')


class DocumentSerializer(serializers.ModelSerializer):
    metadata = MetadataSerializer()

    class Meta:
        model = Document
        fields = ('applicant_id', 'metadata', 'content')

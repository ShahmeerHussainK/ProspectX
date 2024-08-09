from django_elasticsearch_dsl_drf import serializers
from django_elasticsearch_dsl_drf.serializers import DocumentSerializer

from filter_prospects.documents import ProspectDocument


class ProspectDocumentSerializer(DocumentSerializer):
    class Meta:
        document = ProspectDocument
        fields = (
            'id',
            'fullname',
            'firstname',
            'lastname',
            'propertyaddress',
            'propertyaddress2',
            'propertycity',
            'propertystate',
            'propertyzip',
            'mailingaddress',
            'mailingaddress2',
            'mailingcity',
            'mailingstate',
            'mailingzip',
            'email',
            'email2',
            'phoneother',
            'phonecell',
            'phonelandline',
            'phone1',
            'phone2',
            'phone3',
            'phone4',
            'phone5',
            'phone6',
            'phone7',
            'phone8',
            'phone9',
            'phone10'
            'list',
            'tag',
            'absentee',
            'vacant',
            'skipped',
            'is_validate_complete',
            'opt_out',
            'skip_traced',
            'custome1',
            'custome2',
            'custome3',
            'custome4',
            'custome5',
            'custome6',
            'custome7',
            'custome8',
            'custome9',
            'custome10',
            'notes'

        )

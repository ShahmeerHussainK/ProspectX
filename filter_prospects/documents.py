from django_elasticsearch_dsl import (
    DocType,
    fields,
    Index,
)
from filter_prospects.models import (
    Prospect_Properties, List, Tag
)

pro_index = Index('prospect_properties')

pro_index.settings(
    number_of_shards=1,
    number_of_replicas=0
)


@pro_index.doc_type
class ProspectDocument(DocType):
    id = fields.IntegerField(
        attr='id'

    )
    fullname = fields.TextField(
        attr='fullname',
        fields={
            'suggest': fields.Completion(),
        }
    )
    firstname = fields.TextField(
        attr='firstname',
        fields={
            'suggest': fields.Completion(),
        }
    )
    lastname = fields.TextField(
        attr='lastname',
        fields={
            'suggest': fields.Completion(),
        }
    )
    propertyaddress = fields.TextField(
        attr='propertyaddress',
        fields={
            'suggest': fields.Completion(),
        }
    )
    propertyaddress2 = fields.TextField(
        attr='propertyaddress2',
        fields={
            'suggest': fields.Completion(),
        }
    )
    propertycity = fields.TextField(
        attr='propertycity',
        fields={
            'suggest': fields.Completion(),
        }
    )
    propertystate = fields.TextField(
        attr='propertystate',
        fields={
            'suggest': fields.Completion(),
        }
    )
    propertyzip = fields.TextField(
        attr='propertyzip',
        fields={
            'suggest': fields.Completion(),
        }
    )
    mailingaddress = fields.TextField(
        attr='mailingaddress',
        fields={
            'suggest': fields.Completion(),
        }
    )
    mailingaddress2 = fields.TextField(
        attr='mailingaddress2',
        fields={
            'suggest': fields.Completion(),
        }
    )
    mailingcity = fields.TextField(
        attr='mailingcity',
        fields={
            'suggest': fields.Completion(),
        }
    )
    mailingstate = fields.TextField(
        attr='mailingstate',
        fields={
            'suggest': fields.Completion(),
        }
    )
    mailingzip = fields.TextField(
        attr='mailingzip',
        fields={
            'suggest': fields.Completion(),
        }
    )
    email = fields.TextField(
        attr='email',
        fields={
            'suggest': fields.Completion(),
        }
    )
    email2 = fields.TextField(
        attr='email2',
        fields={
            'suggest': fields.Completion(),
        }
    )
    phoneother = fields.TextField(
        attr='phoneother',
        fields={
            'suggest': fields.Completion(),
        }
    )
    phonecell = fields.TextField(
        attr='phonecell',
        fields={
            'suggest': fields.Completion(),
        }
    )
    phonelandline = fields.TextField(
        attr='phonelandline',
        fields={
            'suggest': fields.Completion(),
        }
    )
    phone1 = fields.TextField(
        attr='phone1',
        fields={
            'suggest': fields.Completion(),
        }
    )
    phone2 = fields.TextField(
        attr='phone2',
        fields={
            'suggest': fields.Completion(),
        }
    )
    phone3 = fields.TextField(
        attr='phone3',
        fields={
            'suggest': fields.Completion(),
        }
    )
    phone4 = fields.TextField(
        attr='phone4',
        fields={
            'suggest': fields.Completion(),
        }
    )
    phone5 = fields.TextField(
        attr='phone5',
        fields={
            'suggest': fields.Completion(),
        }
    )
    phone6 = fields.TextField(
        attr='phone6',
        fields={
            'suggest': fields.Completion(),
        }
    )
    phone7 = fields.TextField(
        attr='phone7',
        fields={
            'suggest': fields.Completion(),
        }
    )
    phone8 = fields.TextField(
        attr='phone8',
        fields={
            'suggest': fields.Completion(),
        }
    )
    phone9 = fields.TextField(
        attr='phone9',
        fields={
            'suggest': fields.Completion(),
        }
    )
    phone10 = fields.TextField(
        attr='phone10',
        fields={
            'suggest': fields.Completion(),
        }
    )
    absentee = fields.TextField(
        attr='absentee',
        fields={
            'suggest': fields.Completion(),
        }
    )
    vacant = fields.TextField(
        attr='vacant',
        fields={
            'suggest': fields.Completion(),
        }
    )
    skipped = fields.TextField(
        attr='skipped',
        fields={
            'suggest': fields.Completion(),
        }
    )
    is_validate_complete = fields.TextField(
        attr='is_validate_complete',
        fields={
            'suggest': fields.Completion(),
        }
    )
    opt_out = fields.TextField(
        attr='opt_out',
        fields={
            'suggest': fields.Completion(),
        }
    )
    skip_traced = fields.TextField(
        attr='skip_traced',
        fields={
            'suggest': fields.Completion(),
        }
    )

    custome1 = fields.TextField(
        attr='custome1',
        fields={
            'suggest': fields.Completion(),
        }
    )
    custome2 = fields.TextField(
        attr='custome2',
        fields={
            'suggest': fields.Completion(),
        }
    )
    custome3 = fields.TextField(
        attr='custome3',
        fields={
            'suggest': fields.Completion(),
        }
    )
    custome4 = fields.TextField(
        attr='custome4',
        fields={
            'suggest': fields.Completion(),
        }
    )
    custome5 = fields.TextField(
        attr='custome5',
        fields={
            'suggest': fields.Completion(),
        }
    )
    custome6 = fields.TextField(
        attr='custome6',
        fields={
            'suggest': fields.Completion(),
        }
    )
    custome7 = fields.TextField(
        attr='custome7',
        fields={
            'suggest': fields.Completion(),
        }
    )
    custome8 = fields.TextField(
        attr='custome8',
        fields={
            'suggest': fields.Completion(),
        }
    )
    custome9 = fields.TextField(
        attr='custome9',
        fields={
            'suggest': fields.Completion(),
        }
    )
    custome10 = fields.TextField(
        attr='custome10',
        fields={
            'suggest': fields.Completion(),
        }
    )
    notes = fields.TextField(
        attr='notes',
        fields={
            'suggest': fields.Completion(),
        }
    )
    list = fields.ObjectField(
        properties={
            'list_name': fields.TextField(),
            'id': fields.IntegerField(),
            'user': fields.ObjectField(
                properties={
                    'id': fields.IntegerField(),
                    'email': fields.TextField()
                }
            )
        }
    )

    tag = fields.ObjectField(
        properties={
            'tag_name': fields.TextField(),
            'id': fields.IntegerField(),
            'user': fields.ObjectField(
                properties={
                    'id': fields.IntegerField(),
                    'email': fields.TextField()
                }
            )
        }
    )

    class Meta:
        model = Prospect_Properties
        fields = [
            'list_count', 'tag_count'
        ]

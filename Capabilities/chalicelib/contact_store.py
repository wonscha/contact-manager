import boto3


class ContactStore:
    def __init__(self, store_location, config):
        self.table = boto3.resource(
            'dynamodb',
            aws_access_key_id=config['ACCESS_KEY'],
            aws_secret_access_key=config['SECRET_KEY'],
            region_name=config['boto3_config'].region_name
        ).Table(store_location)

    def save_contact(self, contact_info):
        self.table.put_item(
            Item=contact_info
        )
        # should return values from dynamodb however,
        # dynamodb does not support ReturnValues = ALL_NEW
        return contact_info

    def get_contacts(self, search_name):
        response = self.table.scan()

        contact_info_list = []
        for item in response['Items']:
            if (str(search_name).lower() in str(item['name']).lower()):
                contact_info_list.append(item)

        return contact_info_list

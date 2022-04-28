import boto3
from collections import defaultdict
import re


class ExtractionService:
    def __init__(self, config):
        self.comprehend = boto3.client(
            'comprehend',
            aws_access_key_id=config['ACCESS_KEY'],
            aws_secret_access_key=config['SECRET_KEY'],
            config=config['boto3_config']
        )
        self.comprehend_med = boto3.client(
            'comprehendmedical',
            aws_access_key_id=config['ACCESS_KEY'],
            aws_secret_access_key=config['SECRET_KEY'],
            config=config['boto3_config']
        )

    def extract_contact_info(self, contact_string):
        contact_info = defaultdict(list)

        # extract info with comprehend
        response = self.comprehend.detect_entities(
            Text=contact_string,
            LanguageCode='en'
        )

        website_candidates = []
        for entity in response['Entities']:
            if entity['Type'] == 'PERSON':
                contact_info['name'].append(entity['Text'])
            elif entity['Type'] == 'ORGANIZATION':
                contact_info['organization'].append(entity['Text'])
            else:
                website_candidates.append(entity['Text'])

        # extract info with comprehend medical
        response = self.comprehend_med.detect_phi(
            Text=contact_string
        )

        for entity in response['Entities']:
            if entity['Type'] == 'EMAIL':
                contact_info['email'].append(entity['Text'])
            elif entity['Type'] == 'PHONE_OR_FAX':
                contact_info['phone'].append(entity['Text'])
            elif entity['Type'] == 'ADDRESS':
                contact_info['address'].append(entity['Text'])
            else:
                website_candidates.append(entity['Text'])

        for text in website_candidates:
            m = re.match(
                r"((http|https|ftp|ftps)://)?([a-zA-Z0-9\-]*\.)+[a-zA-Z0-9]{2,4}(/[a-zA-Z0-9=.?&-]*)?", text)
            if m:
                contact_info['website'] = [m.group(0)]
                break

        return dict(contact_info)

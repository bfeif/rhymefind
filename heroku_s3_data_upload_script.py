###
# DOWNLOAD PICKLE FROM S3
from boto3.session import Session
import boto3
import os

# aws_access_key_id='AKIAJLXHOPCM4IHACVDA'
# aws_secret_access_key='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'
aws_access_key_id = os.environ.get('AWS_ACCESS_KEY_ID')
aws_secret_access_key = os.environ.get('AWS_SECRET_ACCESS_KEY')
bucket_name = 'rhymefind-data-01'
object_name = 'word_glove_dictionary_protocol4.pkl'

s3 = boto3.client('s3')

# with open('s3_download_test_file', 'wb') as f:
with open('./word_glove_dictionary.pkl', 'wb') as f:
	s3.download_fileobj(bucket_name, object_name, f)


###
# LOAD PICKLE TO MEMORY AND LOAD DB
import os, sys

proj_path = "."
# This is so Django knows where to find stuff.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "rhymefindersite.settings")
sys.path.append(proj_path)

# This is so my local_settings.py gets loaded.
os.chdir(proj_path)

# This is so models get loaded.
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

# load the model
from rhymefind.models import Glove, RhymeCouplet
import pandas as pd
from tqdm import tqdm

# fill the rhymefind_glove table with data
df = pd.read_pickle('./word_glove_dictionary.pkl')
for row_number, row in tqdm(df.iterrows()):
	print(row_number)
	new_Glove = Glove(**row.to_dict())
	new_Glove.save()


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

# load the models
from rhymefind.models import Word, RhymeCouplet
import pandas as pd
from tqdm import tqdm
from data_helpers import *
import numpy as np

# AWS imports
from boto3.session import Session
import boto3
import os, sys

# AWS stuff
aws_access_key_id = os.environ.get('AWS_ACCESS_KEY_ID')
aws_secret_access_key = os.environ.get('AWS_SECRET_ACCESS_KEY')
bucket_name = 'rhymefind-data-02'
s3 = boto3.client('s3')

# config variables
GLOVE_LOCATION = 'data/glove.6B/glove.6B.{}d.txt'
CMU_LOCATION = 'data/cmudict.txt'

############
# LOAD THE WORD TABLE
# load the cmu dictionary to a dataframe
with open('temp_daddy.csv', 'wb') as f:
    s3.download_fileobj(bucket_name, CMU_LOCATION, f)
rhyme_df = load_cmu_dict('temp_daddy.csv', exclude_non_nltk_words=True, include_repeats=False)

# load glove data to dataframe
glove_names = ['glove_'+str(i) for i in range(32)]

# the 100 glove:
with open('temp_daddy.csv', 'wb') as f:
    s3.download_fileobj(bucket_name, GLOVE_LOCATION.format(str(100)), f)
glove_df = load_glove_dict('temp_daddy.csv')

# and the 32 glove
with open('temp_daddy.csv', 'wb') as f:
    s3.download_fileobj(bucket_name, GLOVE_LOCATION.format(str(50)), f)
glove_df32 = load_glove_dict('temp_daddy.csv', dimensions_to_reduce_to=32)
glove_df32[glove_names] = pd.DataFrame(glove_df32.glove.to_list())

# make the complete glove_df
glove_df = pd.concat([glove_df, glove_df32[glove_names]], axis=1)

# inner join the rhyme_df and the glove_df
word_df = glove_df.merge(rhyme_df, how='left', left_on='word', right_on='word')

# replace NaNs with None
word_df = word_df.where(word_df.notnull(), None)

# load the table
for row_number, row in tqdm(list(word_df.iterrows())):
    row_dict = row.to_dict()
    if type(row_dict['glove'])==np.ndarray:
        row_dict['glove'] = row_dict['glove'].tolist()
    new_Word = Word(**row_dict)
    new_Word.save()


############
# LOAD THE RHYMECOUPLET TABLE
# get rid of words that don't have a phoneme seq
word_df_4_rc = word_df.dropna()

# inner join on phoneme seq
rhyme_couplet_df = word_df_4_rc.merge(word_df_4_rc, how='inner', on='rhyme_seq', suffixes=('_1','_2'))

# eliminate self rhymes
rhyme_couplet_df = rhyme_couplet_df[rhyme_couplet_df.word_1 != rhyme_couplet_df.word_2]

# get rid of duplicates, e.g. ['and', 'band'] vs ['band', 'and']
rhyme_couplet_df['word_tuple'] = rhyme_couplet_df.apply(
    lambda x: tuple(sorted([x['word_1'], x['word_2']])), axis=1)
rhyme_couplet_df.drop_duplicates(subset=['word_tuple'], inplace=True)

# get glove_mean
rhyme_couplet_df['glove_mean'] = np.split((np.vstack(rhyme_couplet_df['glove_1']) + np.vstack(
    rhyme_couplet_df['glove_2'])) / 2, indices_or_sections=len(rhyme_couplet_df), axis=0)
rhyme_couplet_df.glove_mean = rhyme_couplet_df.glove_mean.apply(lambda x: x.flatten().tolist())

# drop superfluous columns
rhyme_couplet_df.drop(columns=['glove_1', 'glove_2', 'word_tuple', 'phoneme_seq_1', 'phoneme_seq_2', 'rhyme_seq'], inplace=True)

# get the glove_mean for the glove_ind columns
for i in range(32):
    rhyme_couplet_df['glove_mean_'+str(i)] = rhyme_couplet_df[['glove_{}_1'.format(i), 'glove_{}_2'.format(i)]].mean(axis=1)
    rhyme_couplet_df.drop(columns=['glove_{}_1'.format(i), 'glove_{}_2'.format(i)], inplace=True)

# rename the word columns
rhyme_couplet_df.rename(columns={'word_1': 'word1', 'word_2': 'word2'}, inplace=True)

# load the table
for row_number, row in tqdm(list(rhyme_couplet_df.iterrows())):
    row_dict = row.to_dict()
    for attr in ['1', '2']:
        row_dict['word'+attr] = Word.objects.get(word=row_dict['word'+attr])#, phoneme_seq=row_dict['phoneme_seq'+attr])
    new_RhymeCouplet = RhymeCouplet(**row_dict)
    new_RhymeCouplet.save()
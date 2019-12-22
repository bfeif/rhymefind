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
df = pd.read_pickle('/Users/benfeifke/code/RhymeFinder/data_for_site_postgres/word_glove_dictionary.pkl')
for row_number, row in tqdm(df.iterrows()):
	new_Glove = Glove(**row.to_dict())
	new_Glove.save()

# fill the rhymefind_rhymecouplet table with data
df = pd.read_pickle('/Users/benfeifke/code/RhymeFinder/data_for_site_postgres/rhymecouplet_glove_dictionary.pkl')
for row_number, row in tqdm(df.iterrows()):
	new_RhymeCouplet = RhymeCouplet(**row.to_dict())
	new_RhymeCouplet.save()
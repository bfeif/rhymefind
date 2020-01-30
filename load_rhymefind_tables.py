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
from rhymefind.models import Glove32dIND, RhymeCouplet32dIND
import pandas as pd
from tqdm import tqdm
data_location = './data/{name}_{dimensions}d.pkl'

# fill the rhymefind_Glove32dIND table with data
df = pd.read_pickle('./data/glove_df_32d.pkl')
for row_number, row in tqdm(df.iterrows()):
	new_Glove32dIND = Glove32dIND(**row.to_dict())
	new_Glove32dIND.save()

# fill the rhymefind_RhymeCouplet32dIND table with data
df = pd.read_pickle('./data/rhyme_couplet_glove_df_32d.pkl')
for row_number, row in tqdm(df.iterrows()):
	new_RhymeCouplet32dIND = RhymeCouplet32dIND(**row.to_dict())
	new_RhymeCouplet32dIND.save()
from data_helpers import *

'''
1) create the pandas pickle files necessary for loading the database tables with
'''

# config variables
GLOVE_LOCATION = './data/glove.6B/{}'
GLOVE_DIMENSIONS = 50
CMU_PRONUNCIATION_DICTIONARY_LOCATION = './'
NUM_PARTS_TO_SAVE_AS = 1

# load the cmu dictionary to a dataframe
rhyme_table = load_cmu_dict()

# load glove data to dataframe
glove_table = load_glove_dict(glove_dimensions=GLOVE_DIMENSIONS)

# create the rhyme_couplet_glove_df
rhyme_couplet_glove_df = create_rhyme_couplet_glove_df(glove_table, rhyme_table)

# split the glove column for each table
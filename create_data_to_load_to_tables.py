from data_helpers import *

'''
1) create the pandas pickle files necessary for loading the database tables with
'''

# config variables
GLOVE_LOCATION = './data/glove.6B/{}'
LOAD_GLOVE_DIMENSIONS = 50
SAVE_GLOVE_DIMENSIONS = 32
CMU_PRONUNCIATION_DICTIONARY_LOCATION = './'
NUM_PARTS_TO_SAVE_AS = 1
PATH_TO_SAVE = './data/{name}_{dimensions}d.pkl'

# load the cmu dictionary to a dataframe
rhyme_df = load_cmu_dict()

# load glove data to dataframe
glove_df = load_glove_dict(glove_dimensions=LOAD_GLOVE_DIMENSIONS,
                           dimensions_to_reduce_to=SAVE_GLOVE_DIMENSIONS)

# create the rhyme_couplet_glove_df
rhyme_couplet_glove_df = create_rhyme_couplet_glove_df(glove_df, rhyme_df)

# split the glove column for each table
rhyme_couplet_glove_df = split_df_list_column(
    rhyme_couplet_glove_df, 'glove_mean')
glove_df = split_df_list_column(glove_df, 'glove')

# save out the files
rhyme_couplet_glove_df.to_pickle(PATH_TO_SAVE.format(
    name='rhyme_couplet_glove_df', dimensions=str(SAVE_GLOVE_DIMENSIONS)), protocol=4)
glove_df.to_pickle(PATH_TO_SAVE.format(
    name='glove_df', dimensions=str(SAVE_GLOVE_DIMENSIONS)), protocol=4)

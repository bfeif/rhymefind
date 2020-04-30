import os
import math
import pandas as pd
import numpy as np
import re
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
glove_data_path = './data/glove.6B/glove.6B.{}d.txt'


def process_glove_line(x):
    '''
    GLOVE loading helper fucntion
    '''
    splitted = x.split()
    return (splitted[0].lower(), np.array(splitted[1:], dtype=np.float64))


def process_cmu_line(x):
    '''
    CMU loading helper function
    '''
    splitted = x.split()
    return (re.sub(r"\(.*?\)","",splitted[0].lower()), splitted[1:])


def convert_phoneme_seq_to_rhyme_seq(phoneme_seq):
    '''
    Convert a phoneme sequence to a rhyme sequence
    '''
    b = ['1' in i for i in phoneme_seq]
    try:
        return tuple(phoneme_seq[b.index(True):])
    except:
        return tuple(phoneme_seq)


def load_cmu_dict(exclude_non_nltk_words=True):
    '''
    Loads cmu dictionary to a dataframe of columns [word<str>, phoneme_seq<List[str]>, rhyme_seq<List[str]>]
    '''
    cmu_records = map(process_cmu_line, open('./data/cmudict.txt').readlines())
    rhyme_dict = pd.DataFrame(cmu_records, columns=['word', 'phoneme_seq'])
    if exclude_non_nltk_words:
        from nltk.corpus import words
        nltk_words = set(words.words())
        nltk_words_mask = rhyme_dict.word.isin(nltk_words)
        rhyme_dict = rhyme_dict.loc[nltk_words_mask, :]
    rhyme_dict['rhyme_seq'] = rhyme_dict.phoneme_seq.apply(
        lambda x: convert_phoneme_seq_to_rhyme_seq(x))
    return rhyme_dict


def load_glove_dict(glove_dimensions=50, dimensions_to_reduce_to=-1):
    '''
    Loads glove dictionary to a dataframe of columns [word<str>, glove<np.array[float]>]
    '''

    # create the dataframe
    df = pd.DataFrame(map(process_glove_line, open(glove_data_path.format(
        glove_dimensions)).readlines()), columns=['word', 'glove'])

    # if dimensionality doesn't need to be reduced, then just return
    if dimensions_to_reduce_to == -1:
        
        # return
        return df

    # else it does, then do the reduction and return the reduced frame
    else:
        
        # reduce the dataframe
        mat = np.vstack(df['glove'])
        reduced_mat = reduce_glove_dimensionality(mat, dimensions_to_reduce_to)
        reduced_df = pd.DataFrame()
        reduced_df['glove'] = reduced_mat.tolist()
        new_df = pd.concat([df['word'], reduced_df], axis=1)
    
        # return
        return new_df


def reduce_glove_dimensionality(array, dimensions_to_reduce_to, plot=False):
    '''
    Reduce the dimensionaliity of a word embeddings matrix, using the strategy desribed in
    Simple and Effective Dimensionality Reduction for Word Embeddings https://arxiv.org/pdf/1708.03629.pdf
    '''

    # subtract mean word embedding
    array_mean = np.mean(array, axis=0)
    array = array - array_mean

    # perform pca and keep only the dimensions to reduce to
    pca = PCA(n_components=dimensions_to_reduce_to)
    array_PCAd = pca.fit_transform(array)
    if plot:
        plt.plot(pca.explained_variance_ratio_)
        plt.show()

    # return
    return array_PCAd

def create_rhyme_couplet_df(word_df):
    
    # do the merge
    couplet_df = word_df.merge(word_df, how='inner', left_on='rhyme_seq', right_on='rhyme_seq', suffixes=('_1', '_2'))

    # get rid of couplets of the same word, e.g. ['and', 'and']
    couplet_df = couplet_df[couplet_df.word_1 != couplet_df.word_2]

    # get rid of duplicates, e.g. ['and', 'band'] vs ['band', 'and']
    couplet_df['word_tuple'] = couplet_df.apply(
        lambda x: tuple(sorted([x['word_1'], x['word_2']])), axis=1)
    couplet_df.drop_duplicates(subset=['word_tuple'], inplace=True)

    # get glove mean
    couplet_df['glove_mean'] = np.split((np.vstack(couplet_df['glove_1']) + np.vstack(
        couplet_df['glove_2'])) / 2, indices_or_sections=len(couplet_df), axis=0)

    # drop superfluous columns
    couplet_df.drop(columns=['glove_1', 'glove_2', 'word_tuple', 'phoneme_seq_1', 'phoneme_seq_2', 'rhyme_seq'], inplace=True)

    # return
    return couplet_df

def create_rhyme_couplet_glove_df(glove_table, rhyme_table):
    '''
    Creates the rhyme couplet glove table
    '''

    # add glove data to the rhyme table
    rhyme_glove_table = rhyme_table.merge(
        glove_table, how='inner', left_on='word', right_on='word')

    # make a copy
    rhyme_glove_table_copy = rhyme_glove_table.copy()

    # merge copies to make the dictionary
    couplet_dictionary = rhyme_glove_table.merge(
        rhyme_glove_table_copy, how='inner', left_on='rhyme_seq', right_on='rhyme_seq', suffixes=('_1', '_2'))

    # get rid of couplets of the same word, e.g. ['and', 'and']
    couplet_dictionary = couplet_dictionary[couplet_dictionary.word_1 !=
                                            couplet_dictionary.word_2]

    # get rid of duplicates, e.g. ['and', 'band'] vs ['band', 'and']
    couplet_dictionary['word_tuple'] = couplet_dictionary.apply(
        lambda x: tuple(sorted([x['word_1'], x['word_2']])), axis=1)
    couplet_dictionary.drop_duplicates(subset=['word_tuple'], inplace=True)

    # get glove_mean
    couplet_dictionary['glove_mean'] = np.split((np.vstack(couplet_dictionary['glove_1']) + np.vstack(
        couplet_dictionary['glove_2'])) / 2, indices_or_sections=len(couplet_dictionary), axis=0)

    # drop superfluous columns
    couplet_dictionary.drop(
        columns=['glove_1', 'glove_2', 'word_tuple'], inplace=True)

    # return
    return couplet_dictionary


def split_df_list_column(df, list_column_name):
    '''
    Takes a dataframe that has a column of type List[obj] and returns the same dataframe with new columns obj_1, obj_2, ..., obj_n
    '''

    # remove the list column name
    columns = df.columns.to_list()
    columns.remove(list_column_name)

    # separate the df into parts
    df_wo_list_column = df[columns]

    # do the unlisting
    unlisted_mat = np.vstack(df[list_column_name])
    df_w_list_column_unlisted = pd.DataFrame(unlisted_mat, columns=[
                                             list_column_name + '_{}'.format(i) for i in range(unlisted_mat.shape[1])])

    # concatenate the results and return
    new_df = pd.concat([df_wo_list_column.reset_index(
        drop=True), df_w_list_column_unlisted.reset_index(drop=True)], axis=1)
    return new_df


def save_table(df, path, name, num_parts=1):
    '''
    Saves out the generated data
    '''

    # If you want to save it out as only one file
    if num_parts==1:
        df.to_pickle(path + name + '.pkl', protocol=4)
    
    # If you want to save it out in parts
    else:
        os.mkdir(path + name)
        part_length = math.ceil(len(df)/num_parts)
        for i in range(num_parts):
            start = i * part_length
            end = (i + 1) * part_length
            df_part = df.iloc[start:end, :]
            df_part.to_pickle(path + name + '/' + name + '_part' + str(i) + '.pkl', protocol=4)

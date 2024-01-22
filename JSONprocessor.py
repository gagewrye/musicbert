import os
import sys
import random
import zipfile
from multiprocessing import Pool, Manager
import preprocess
import json
from sklearn.model_selection import StratifiedKFold


# Path to store datap
subset = input('Labeled subset: ') # This is the classification database location, we will binarize this after
raw_data_dir = subset + '_data_raw' # Processed data stored here
if os.path.exists(raw_data_dir):
    print('Output path {} already exists!'.format(raw_data_dir))
    sys.exit(0)

# Dataset Zip path
data_path = input('Main dataset zip path: ') # Includes all of the data in the labeled subset
n_folds = 5
n_times = 4  
max_length = int(input('sequence length: ')) # Set to 1000 in example

# preprocessing and tools setup
preprocess.sample_len_max = max_length
preprocess.deduplicate = False
preprocess.data_zip = zipfile.ZipFile(data_path)
fold_map = dict()
manager = Manager()
all_data = manager.list()
pool_num = 24


# Create a mapping of midi files to their composer
labels = dict()
with open('midi_composer_map.json') as f:
    for title, composer in json.load(f).items():
        labels[title] = composer


def get_id(file_name):
    return file_name.split('/')[-1].split('.')[0]


def get_fold(file_name):
    return fold_map[get_id(file_name)]


def get_sample(output_str_list):
    max_len = max(len(s.split()) for s in output_str_list)
    return random.choice([s for s in output_str_list if len(s.split()) == max_len])


# Process and store data
def new_writer(file_name, output_str_list):
    if len(output_str_list) > 0:
        all_data.append((file_name, tuple(get_sample(output_str_list)
                                          for _ in range(n_times))))


preprocess.writer = new_writer


os.system('mkdir -p {}'.format(raw_data_dir))
file_list = [file_name for file_name in preprocess.data_zip.namelist(
) if file_name[-4:].lower() == '.mid' or file_name[-5:].lower() == '.midi']
file_list = [file_name for file_name in file_list if get_id(
    file_name) in labels]
random.shuffle(file_list)

# Generate labels for split dataset
label_list = [labels[get_id(file_name)] for file_name in file_list]

# Split data into folds
fold_index = 0
for train_index, test_index in StratifiedKFold(n_folds).split(file_list, label_list):
    for i in test_index:
        fold_map[get_id(file_list[i])] = fold_index
    fold_index += 1
with Pool(pool_num) as p:
    list(p.imap_unordered(preprocess.G, file_list))
random.shuffle(all_data)
print('{}/{} ({:.2f}%)'.format(len(all_data),
                               len(file_list), len(all_data) / len(file_list) * 100))

# Organize data into test and train sets for every fold
for fold in range(n_folds):
    os.system('mkdir -p {}/{}'.format(raw_data_dir, fold))
    preprocess.gen_dictionary('{}/{}/dict.txt'.format(raw_data_dir, fold))
    for cur_split in ['train', 'test']:
        output_path_prefix = '{}/{}/{}'.format(raw_data_dir, fold, cur_split)
        with open(output_path_prefix + '.txt', 'w') as f_txt, \
             open(output_path_prefix + '.label', 'w') as f_label, \
             open(output_path_prefix + '.id', 'w') as f_id:
                    count = 0
                    for file_name, output_str_list in all_data:
                        if (cur_split == 'train' and fold != get_fold(file_name)) or (cur_split == 'test' and fold == get_fold(file_name)):
                            for i in range(n_times if cur_split == 'train' else 1):
                                f_txt.write(output_str_list[i] + '\n')
                                f_label.write(labels[get_id(file_name)] + '\n')
                                f_id.write(get_id(file_name) + '\n')
                                count += 1
                    print(fold, cur_split, count)
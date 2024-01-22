# Musicbert steps
1. Setup an Ubuntu environment with python 3.9
2. Install requirements from requirements.txt $ pip install -r requirements.txt \\
   $ pip install miditoolkit \\
   $ pip install scikit-learn \\
   $ git clone https://github.com/pytorch/fairseq
    $ cd fairseq
   $ git checkout 336942734c85791a90baa373c212d27e7c722662
    $ pip install --editable ./
   $ cd fairseq/data/
   $ nano indexed_dataset.py 
     Go to line 101, 306 and change np.float to np.float64. np.float is deprecated
4. Download Giant Midi dataset
5. preprocess the Giant dataset into Octuple format using preprocess.py
   $ python3 -u preprocess.py
   Input: Dataset zip path: ~/GiantMidi.zip
   OctupleMIDI output path: GiantMidiOct
    This will create GiantMidiOct_data_raw
7. Binarize Giant dataset using binarize_pretrain.sh
   $ bash binarize_pretrain.sh GiantMidiOct      This will create GiantMidiOct_data_bin
9. Train MusicBert base model checkpoint on the Giant to refine the model to piano solo midi
    $ bash train_mask.sh GiantMidiOct base
11. Prepare our classification data. Make Octuple midi files for each composer in the classification task. In our case it is Bach, Beetoven, Chopin, and Liszt. Save these into a base directory called composers. Place each composer’s music into separate files with the names of the composer they contain.
12. Now we can finetune the model to our classification task. Create a JSON of the composer labels using the JSON generator and JSON processor. These functions will parse all of the files in composer.zip files and create labels based on the names of the composers. Run JSONgenerator.py and ensure file path to the composers folder in the code is correct
    $ python JSONprocessor.py
    'Labeled subset: ' composers (Classification database location)
         - This will split the data into raw and binarized folders
    'Main dataset zip path: ' composers.zip (All data in labeled subset)
    'sequence length: ' 500
    $ bash train_composer.sh composers 13 0 /xxx/checkpoint_last_musicbert_base
14. Evaluate the classifier
    $ python -u eval_genre.py checkpoints/checkpoint_last_genre_topmagd_x_checkpoint_last_musicbert_small.pttopmagd_data_bin/x

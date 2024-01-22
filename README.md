# Musicbert steps
1. Setup an Ubuntu environment with python 3.9
2. Install requirements from requirements.txt $ pip install -r requirements.txt <br>
   $ pip install miditoolkit <br>
   $ pip install scikit-learn  <br>
   $ git clone https://github.com/pytorch/fairseq <br>
    $ cd fairseq<br>
   $ git checkout 336942734c85791a90baa373c212d27e7c722662<br>
    $ pip install --editable ./<br>
   $ cd fairseq/data/<br>
   $ nano indexed_dataset.py <br>
     Go to line 101, 306 and change np.float to np.float64. np.float is deprecated<br>
4. Download Giant Midi dataset
5. preprocess the Giant dataset into Octuple format using preprocess.py<br>
   $ python3 -u preprocess.py<br>
   Input: Dataset zip path: ~/GiantMidi.zip<br>
   OctupleMIDI output path: GiantMidiOct<br>
    This will create GiantMidiOct_data_raw<br><br>
7. Binarize Giant dataset using binarize_pretrain.sh<br>
   $ bash binarize_pretrain.sh GiantMidiOct      This will create GiantMidiOct_data_bin<br>
9. Train MusicBert base model checkpoint on the Giant to refine the model to piano solo midi<br>
    $ bash train_mask.sh GiantMidiOct base<br>
11. Prepare our classification data. Make Octuple midi files for each composer in the classification task. In our case it is Bach, Beetoven, Chopin, and Liszt. Save these into a base directory called composers. Place each composer’s music into separate files with the names of the composer they contain.<br>
12. Now we can finetune the model to our classification task. Create a JSON of the composer labels using the JSON generator and JSON processor. These functions will parse all of the files in composer.zip files and create labels based on the names of the composers. Run JSONgenerator.py and ensure file path to the composers folder in the code is correct<br>
    $ python JSONprocessor.py<br>
    'Labeled subset: ' composers (Classification database location)<br>
         - This will split the data into raw and binarized folders<br>
    'Main dataset zip path: ' composers.zip (All data in labeled subset)<br>
    'sequence length: ' 500<br>
    $ bash train_composer.sh composers 13 0 /xxx/checkpoint_last_musicbert_base<br><br>
14. Evaluate the classifier<br>
    $ python -u eval_genre.py checkpoints/checkpoint_last_genre_topmagd_x_checkpoint_last_musicbert_small.pttopmagd_data_bin/x

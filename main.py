# Download Giant Midi piano dataset to train MusicBert

# Run: python -u preprocess.py

# Input: Dataset zip path: /xxx/xxx/MusicBERT/lmd_full.zip
#        OctupleMIDI output path: lmd_full_data_raw

# bash binarize_pretrain.sh lmd_full

# bash train_mask.sh lmd_full small OR bash train_mask.sh lmd_full base

#



# now we can train the general model and finetune it on our classification task

# JSONgenerator.py
# JSONprocessor.py
# bash binarize_classifier.sh (Your path from JSONprocessor)

# bash train_composer.sh (JSONprocessor path) 13 0 checkpoints/checkpoint_last_musicbert_base.pt
# python -u eval_composer.py checkpoints/checkpoint_last_genre_topmagd_x_checkpoint_last_musicbert_small.pt topmagd_data_bin/x




#!/usr/bin/env bash
###########################################################
# Change the following values to preprocess a new dataset.
# TRAIN_DIR, VAL_DIR and TEST_DIR should be paths to      
#   directories containing sub-directories with .java files
# DATASET_NAME is just a name for the currently extracted 
#   dataset.                                              
# MAX_DATA_CONTEXTS is the number of contexts to keep in the dataset for each 
#   method (by default 1000). At training time, these contexts
#   will be downsampled dynamically to MAX_CONTEXTS.
# MAX_CONTEXTS - the number of actual contexts (by default 200) 
# that are taken into consideration (out of MAX_DATA_CONTEXTS)
# every training iteration. To avoid randomness at test time, 
# for the test and validation sets only MAX_CONTEXTS contexts are kept 
# (while for training, MAX_DATA_CONTEXTS are kept and MAX_CONTEXTS are
# selected dynamically during training).
# SUBTOKEN_VOCAB_SIZE, TARGET_VOCAB_SIZE -   
#   - the number of subtokens and target words to keep 
#   in the vocabulary (the top occurring words and paths will be kept). 
# NUM_THREADS - the number of parallel threads to use. It is 
#   recommended to use a multi-core machine for the preprocessing 
#   step and set this value to the number of cores.
# PYTHON - python3 interpreter alias.

# Split java_file into dir and file
JAVAFILE_DIR="$(dirname "$2")"
FILENAME="$(basename "$2")"

TEST_DIR="$1/$JAVAFILE_DIR"
DATASET_NAME=$3
MAX_DATA_CONTEXTS=1000
MAX_CONTEXTS=200
SUBTOKEN_VOCAB_SIZE=186277
TARGET_VOCAB_SIZE=26347
NUM_THREADS=64
PYTHON=python3

# print params
echo "TEST_DIR: $TEST_DIR"
echo "DATASET_NAME: $DATASET_NAME"
# print positonal params
echo "1: $1"
echo "2: $2"
echo "3: $3"
###########################################################

TEST_DATA_FILE=${DATASET_NAME}.test.raw.txt
EXTRACTOR_JAR=JavaExtractor/JPredict/target/JavaExtractor-0.0.1-SNAPSHOT.jar

mkdir -p data
mkdir -p data/${DATASET_NAME}

echo "Extracting paths from test set..."
${PYTHON} JavaExtractor/extract.py --dir ${TEST_DIR} --max_path_length 8 --max_path_width 2 --num_threads ${NUM_THREADS} --jar ${EXTRACTOR_JAR} > ${TEST_DATA_FILE} 2>> error_log.txt
echo "Finished extracting paths from test set"

${PYTHON} preprocess_test.py --test_data ${TEST_DATA_FILE} \
  --max_contexts ${MAX_CONTEXTS} --max_data_contexts ${MAX_DATA_CONTEXTS} --subtoken_vocab_size ${SUBTOKEN_VOCAB_SIZE} \
  --target_vocab_size ${TARGET_VOCAB_SIZE} --output_name data/${DATASET_NAME}/${DATASET_NAME}
    
# If all went well, the raw data files can be deleted, because preprocess.py creates new files 
# with truncated and padded number of paths for each example.
rm ${TEST_DATA_FILE}


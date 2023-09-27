#!/usr/bin/env bash

model="/Users/lap13494/workspace/ppl-extra-final/models/java-large-model/model_iter52.release"

g_root_path="/Users/lap13494/workspace/ppl-extra-final/SIVAND/models/dd-code2seq/code2seq"
cd ${g_root_path}

rm -rf data/sm/ data/tmp/ dd_data/
mkdir -p data/sm/ data/tmp/ dd_data/

echo "" > data/sm/sm.test.c2s
echo "" > data/tmp/sm_test.java

python3 -- dd_code2seq.py --load ${model} --test data/sm/sm.test.c2s

rm -rf data/sm/ data/tmp/
rm -rf tmp/ __pycache__/

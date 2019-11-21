#!/bin/bash


cur_dir=$(cd $( dirname ${BASH_SOURCE[0]} ) && pwd )
root_dir=~/Documents/BirdWatcher/caffe

cd $root_dir

redo=1
dataset_name="bird_dataset" #Edit this to your dataset name. Don't change anything else
data_root_dir=~/Documents/BirdWatcher/MyDataset/bird_dataset
mapfile="$data_root_dir/labelmap.prototxt"
anno_type="detection"
db="lmdb"
min_dim=0
max_dim=0
width=300
height=300

extra_cmd="--encode-type=jpg --encoded"
if [ $redo ]
then
  extra_cmd="$extra_cmd --redo"
fi
for subset in test trainval
do
  python3 $root_dir/scripts/create_annoset.py --anno-type=$anno_type --label-map-file=$mapfile --min-dim=$min_dim --max-dim=$max_dim --resize-width=$width --resize-height=$height --check-label $extra_cmd $data_root_dir $data_root_dir/Structure/$subset.txt $data_root_dir/$dataset_name/$db/$dataset_name"_"$subset"_"$db examples/$dataset_name
done

#!/bin/bash

root_dir=$HOME/data/VOCdevkit/
sub_dir=ImageSets/Main
bash_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

dst_file1=$bash_dir/trainval.txt
if [ -f $dst_file1 ]
then
  rm -f $dst_file1
fi

dst_file2=$bash_dir/test.txt
if [ -f $dst_file2 ]
then
  rm -f $dst_file2
fi

for dataset in trainval test
do
  for name in VOC2007 VOC2012
  do
    if [[ $dataset == "test" && $name == "VOC2012" ]]
    then
      echo "Create list for $name $dataset..."
      dataset_file=$root_dir/$name/$sub_dir/$dataset.txt

      img_file=$bash_dir/$dataset"_img.txt"
      cp $dataset_file $img_file
      sed -i "s/^/$name\/JPEGImages\//g" $img_file
      sed -i "s/$/.jpg/g" $img_file

      label_file=$bash_dir/$dataset"_label.txt"
      cp $dataset_file $label_file
      sed -i "s/^/$name\/Annotations\//g" $label_file
      sed -i "s/$/.xml/g" $label_file

      paste -d' ' $img_file $label_file >> $dst_file2

      rm -f $label_file
      rm -f $img_file
      continue
    else
      echo "Create list for $name $dataset..."
      dataset_file=$root_dir/$name/$sub_dir/$dataset.txt

      img_file=$bash_dir/$dataset"_img.txt"
      cp $dataset_file $img_file
      sed -i "s/^/$name\/JPEGImages\//g" $img_file
      sed -i "s/$/.jpg/g" $img_file

      label_file=$bash_dir/$dataset"_label.txt"
      cp $dataset_file $label_file
      sed -i "s/^/$name\/Annotations\//g" $label_file
      sed -i "s/$/.xml/g" $label_file

      paste -d' ' $img_file $label_file >> $dst_file1

      rm -f $label_file
      rm -f $img_file
    fi
  done

  # Generate image name and size infomation.
  if [[ $dataset == "test" && $name == "VOC2012" ]]
  then
    $bash_dir/../../build/tools/get_image_size $root_dir $dst_file2 $bash_dir/$dataset"_name_size.txt"
  fi

  # Shuffle trainval file.
  if [ $dataset == "trainval" ]
  then
    rand_file=$dst_file1.random
    cat $dst_file1 | perl -MList::Util=shuffle -e 'print shuffle(<STDIN>);' > $rand_file
    mv $rand_file $dst_file1
  fi
done

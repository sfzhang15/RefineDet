1. Download and extract VOC2007 and VOC2012 dataset. By default, we assume the data is stored in `$HOME/data/`
  ```Shell
  cd $HOME/data
  wget http://host.robots.ox.ac.uk/pascal/VOC/voc2012/VOCtrainval_11-May-2012.tar
  wget http://host.robots.ox.ac.uk/pascal/VOC/voc2007/VOCtrainval_06-Nov-2007.tar
  wget http://host.robots.ox.ac.uk/pascal/VOC/voc2007/VOCtest_06-Nov-2007.tar
  tar -xvf VOCtrainval_11-May-2012.tar
  tar -xvf VOCtrainval_06-Nov-2007.tar
  tar -xvf VOCtest_06-Nov-2007.tar
  # You should download the test set of VOC2012 as follow:
  Download VOC2012test.tar via http://host.robots.ox.ac.uk:8080/eval/downloads/VOC2012test.tar and upzip it.
  ```  

2. Create the trainval.txt, test.txt, and test_name_size.txt in `data/VOC0712Plus/`
  ```Shell
  cd $RefineDet_ROOT
  ./data/VOC0712Plus/create_list.sh
  ```

3. Create the LMDB file.
  ```Shell
  # You can modify the parameters in create_data.sh if needed.
  # It will create lmdb files for trainval with encoded original image:
  #   - $HOME/data/VOCdevkit/VOC0712Plus/lmdb/VOC0712Plus_trainval_lmdb
  # and make soft links at examples/VOC0712Plus/
  cd $RefineDet_ROOT
  ./data/VOC0712Plus/create_data.sh
  ```

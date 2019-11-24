#!/bin/bash

sudo apt-get update -y
sudo apt-get upgrade -y
sudo apt-get install -y git python3.6 python3-pip vim tree
sudo apt-get install -y portaudio19-dev python-pyaudio python3-pyaudio

cd ~/Documents/
mkdir BirdWatcher

cd BirdWatcher
git clone https://github.com/soja-soja/AIBirdWatching.git
cd AIBirdWatching
pip3 install -r requirements.txt

cd ~/Documents/BirdWatcher/
git clone https://github.com/chuanqi305/MobileNet-SSD.git
cd ~/Documents/BirdWatcher/AIBirdWatching/gists/


cd ~/Documents/BirdWatcher/
git clone https://github.com/chuanqi305/MobileNet-SSD.git
cd ~/Documents/BirdWatcher/AIBirdWatching/gists/



cd ~/Documents/BirdWatcher/ 
git clone https://github.com/hardikvasa/google-images-download.git
cd google-images-download && sudo python3 setup.py install

cd ~/Downloads
wget https://chromedriver.storage.googleapis.com/78.0.3904.105/chromedriver_linux64.zip
unzip -o chromedriver_linux64.zip
googleimagesdownload --keywords "hummingbird" --limit 100 --chromedriver ~/Downloads/chromedriver --format jpg -o ~/Documents/BirdWatcher/DownloadedImages/
googleimagesdownload --keywords "blue jay" --limit 100 --chromedriver ~/Downloads/chromedriver --format jpg -o ~/Documents/BirdWatcher/DownloadedImages/

# Repeating the last two commands twice just to make sure it will get the images, 
# as it sometimes will quit due to rate limit, connection issue, etc
googleimagesdownload --keywords "hummingbird" --limit 100 --chromedriver ~/Downloads/chromedriver --format jpg -o ~/Documents/BirdWatcher/DownloadedImages/
googleimagesdownload --keywords "blue jay" --limit 100 --chromedriver ~/Downloads/chromedriver --format jpg -o ~/Documents/BirdWatcher/DownloadedImages/


sudo apt-get install -y pyqt5-dev-tools
cd ~/Documents/BirdWatcher
git clone https://github.com/tzutalin/labelImg.git
cd labelImg
sudo pip3 install -r requirements/requirements-linux-python3.txt
make qt5py3

python3 labelImg.py ../DownloadedImages/hummingbird/ ../AIBirdWatching/BirdWatcher/pre_defined_labels.txt 

# and then:
python3 labelImg.py "../DownloadedImages/blue jay/" ../AIBirdWatching/BirdWatcher/pre_defined_labels.txt 

cd ~/Documents/BirdWatcher
mkdir MyDataset
mkdir MyDataset/bird_dataset
mkdir MyDataset/bird_dataset/Images
mkdir MyDataset/bird_dataset/Labels
mkdir MyDataset/bird_dataset/Videos
mkdir MyDataset/bird_dataset/Structure


cd ~/Documents/BirdWatcher/DownloadedImages/
# where the images you have downloaded and labeled are...
cp */*.jpg ~/Documents/BirdWatcher/MyDataset/bird_dataset/Images/
cp */*.xml ~/Documents/BirdWatcher/MyDataset/bird_dataset/Labels/


cd ~/Documents/BirdWatcher/AIBirdWatching/gists/
python3 trainval_creator.py
cp ~/Documents/BirdWatcher/AIBirdWatching/BirdWatcher/MyDataset/bird_dataset/labelmap.prototxt ~/Documents/BirdWatcher/MyDataset/bird_dataset/


cd ~/Documents/BirdWatcher/

git clone --branch ssd --depth 1 https://github.com/weiliu89/caffe.git

## or get INTEL OPTIMIZED CAFFE
# git clone https://github.com/intel/caffe.git
## in that case do the following:
# sudo apt-get install python3-venv
# python3 -m venv env
# source env/bin/activate 
# caffe/scripts/prepare_env.sh


cd caffe 
export CAFFE_ROOT=$(pwd)
# add this in your ~/.bashrc so you dont have to do this after each restart or system shutdown:
echo  export CAFFE_ROOT=$(pwd) >> ~/.bashrc


# for CPU:
sudo apt install -y caffe-cpu
# for GPU:
#sudo apt install caffe-cuda
sudo apt-get install -y build-essential cmake git pkg-config libprotobuf-dev libleveldb-dev libsnappy-dev libhdf5-serial-dev protobuf-compiler libatlas-base-dev libgflags-dev libgoogle-glog-dev liblmdb-dev  python3-dev python-numpy python-scipy libopencv-dev liblapack-dev liblapack3 libopenblas-base libopenblas-dev
# libjasper-dev
sudo apt-get install -y --no-install-recommends libboost-all-dev

cd /usr/lib/x86_64-linux-gnu
sudo ln -s libhdf5_serial.so.100.0.1 libhdf5.so
sudo ln -s libhdf5_serial_hl.so.100.0.0 libhdf5_hl.so

export PATH_HDF5="/usr/include/hdf5/serial/"
export CPATH="/usr/include/hdf5/serial/"

echo export CPATH="/usr/include/hdf5/serial/" >> ~/.bashrc
echo export PATH_HDF5=/usr/include/hdf5/serial/ >> ~/.bashrc



cd ~/Documents/BirdWatcher/caffe/python
export PYTHONPATH="/usr/lib/python3.6:$(pwd)"
echo export PYTHONPATH=/usr/lib/python3.6:$(pwd) >> ~/.bashrc

source ~/.bashrc

cp ~/Documents/BirdWatcher/AIBirdWatching/BirdWatcher/caffe/Makefile.config  ~/Documents/BirdWatcher/caffe/Makefile.config

# if using INTEL optimized Caffe:
#cp ~/Documents/BirdWatcher/AIBirdWatching/BirdWatcher/caffe/Makefile_intel.config  ~/Documents/BirdWatcher/caffe/Makefile.config


cd ~/Documents/BirdWatcher/caffe/
make all
make py





mkdir ~/Documents/BirdWatcher/caffe/data/CustomDataset
cp ~/Documents/BirdWatcher/AIBirdWatching/BirdWatcher/caffe/data/CustomDataset/create_data.sh ~/Documents/BirdWatcher/caffe/data/CustomDataset


cd ~/Documents/BirdWatcher/caffe/data/CustomDataset
chmod +x create_data.sh
./create_data.sh



cd ~/Documents/BirdWatcher/caffe/examples
git clone --depth 1 https://github.com/chuanqi305/MobileNet-SSD

cd MobileNet-SSD
ln -s ~/Documents/BirdWatcher/MyDataset/bird_dataset/bird_dataset/lmdb/bird_dataset_trainval_lmdb/ trainval_lmdb
ln -s ~/Documents/BirdWatcher/MyDataset/bird_dataset/bird_dataset/lmdb/bird_dataset_test_lmdb/ test_lmdb
ln -s ~/Documents/BirdWatcher/MyDataset/bird_dataset/labelmap.prototxt labelmap.prototxt
cp ~/Documents/BirdWatcher/AIBirdWatching/BirdWatcher/caffe/examples/MobileNet-SSD/solver_test.prototxt ~/Documents/BirdWatcher/caffe/examples/MobileNet-SSD/
cp ~/Documents/BirdWatcher/AIBirdWatching/BirdWatcher/caffe/examples/MobileNet-SSD/solver_train.prototxt ~/Documents/BirdWatcher/caffe/examples/MobileNet-SSD/
cp ~/Documents/BirdWatcher/AIBirdWatching/BirdWatcher/caffe/examples/MobileNet-SSD/train.sh ~/Documents/BirdWatcher/caffe/examples/MobileNet-SSD/
cp ~/Documents/BirdWatcher/AIBirdWatching/BirdWatcher/caffe/examples/MobileNet-SSD/merge_bn.py ~/Documents/BirdWatcher/caffe/examples/MobileNet-SSD/
cp ~/Documents/BirdWatcher/AIBirdWatching/BirdWatcher/caffe/src/caffe/util/math_functions.cpp ~/Documents/BirdWatcher/caffe/src/caffe/util/

cd ~/Documents/BirdWatcher/caffe/examples/MobileNet-SSD
./gen_model.sh 3


./train.sh



cd ~/Documents/BirdWatcher/caffe/examples/MobileNet-SSD
python3 merge_bn.py snapshot/$(ls snapshot|grep caffemodel |tail -n 1)



cd ~/Documents/BirdWatcher/AIBirdWatching/gists/
python3 Run.py -mc "~/Documents/BirdWatcher/caffe/examples/MobileNet-SSD/MobileNetSSD_birds_soja.caffemodel" -p "~/Documents/BirdWatcher/caffe/examples/MobileNet-SSD/example/MobileNetSSD_deploy.prototxt"

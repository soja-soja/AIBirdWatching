#!/usr/bin/bash

sudo apt-get update
sudo apt-get upgrade
sudo apt-get install git python3.6 python3-pip

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
unzip chromedriver_linux64.zip
googleimagesdownload --keywords "hummingbird" --limit 100 --chromedriver ~/Downloads/chromedriver --format jpg -o ~/Documents/BirdWatcher/DownloadedImages/
googleimagesdownload --keywords "blue jay" --limit 100 --chromedriver ~/Downloads/chromedriver --format jpg-o ~/Documents/BirdWatcher/DownloadedImages/


sudo apt-get install pyqt5-dev-tools
cd ~/Documents/BirdWatcher
git clone https://github.com/tzutalin/labelImg.git
cd labelImg
sudo pip3 install -r requirements/requirements-linux-python3.txt
make qt5py3


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


cd ~/Documents/BirdWatcher/
git clone --depth 1 https://github.com/weiliu89/caffe.git
cd caffe 
export CAFFE_ROOT=$CAFFE_ROOT:$(pwd)
# add this in your ~/.bashrc so you dont have to do this after each restart or system shutdown:
echo  export CAFFE_ROOT=$CAFFE_ROOT:$(pwd) >> ~/.bashrc


# for CPU:
sudo apt install caffe-cpu
# for GPU:
#sudo apt install caffe-cuda
sudo apt-get install -y build-essential cmake git pkg-config libprotobuf-dev libleveldb-dev libsnappy-dev libhdf5-serial-dev protobuf-compiler libatlas-base-dev libgflags-dev libgoogle-glog-dev liblmdb-dev  python3-dev python-numpy python-scipy libopencv-dev
# libjasper-dev
sudo apt-get install -y --no-install-recommends libboost-all-dev

cd ~/Documents/BirdWatcher/caffe/
cp ~/Documents/BirdWatcher/AIBirdWatching/BirdWatcher/caffe/Makefile.config  ~/Documents/BirdWatcher/caffe/


cd ~/Documents/BirdWatcher/caffe/
make all
make py
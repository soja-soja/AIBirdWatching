# AIBirdWatching

I walk you through required steps for testing and re-training a pre-trained object detection model using python language. I have put together a script that does most of the steps automatically, except labeling the images :D However, I highly recommend that you follow the detailed instructions from my Medium article to know why and how we do each of the steps, it might look time consuming, but it is rewarding, I promise ;)

Read the tutorial from here: [Link](https://medium.com/@itsoja/smart-bird-watcher-customizing-pre-trained-ai-models-to-detect-birds-of-interest-dca1202bfbdf)
<p align="center">
 <img src="https://miro.medium.com/max/600/1*mJzFUfkb1vo4x8e_Xz7UOQ.png" align="center" alt="AI bird watcher Intel ">
</p>

## If you're in rush to give it a try, then the short version is as follows:

To start, create a virtualbox/vmware Ubuntu machine, update the OS and install required packages as follows:
```
sudo apt-get update
sudo apt-get upgrade
sudo apt-get install -y git python3.6 python3-pip vim tree portaudio19-dev python-pyaudio python3-pyaudio
```

and then clone this repository:

```
cd ~/Documents/
mkdir BirdWatcher

cd BirdWatcher
git clone https://github.com/soja-soja/AIBirdWatching.git
cd AIBirdWatching
pip3 install -r requirements.txt
```

and finally run the script:

```
cd ~/Documents/BirdWatcher/AIBirdWatching/
chmod +x setup.sh
./setup.sh
```


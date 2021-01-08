#set up ubuntu machine 

#basic setup
sudo apt install net-tools
sudo apt install openssh-server0
#create new dir
sudo apt install git
mkdir app
cd app

#pull my files from github
git init
git pull https://github.com/bliss81/dockerwebapp.git

#update linux 
sudo apt update

#download repository
sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu bionic stable"
sudo apt update
install docker
apt-cache policy docker-ce
sudo apt install docker-ce

# enable docker without sudo to current user
sudo usermod -aG docker ${USER}
#install python3
sudo apt-get install python3 python3-pip -y

#install flask
sudo pip3 install flask
sudo pip3 install flask-wtf

#load my app
export FLASK_APP=main.py
run flask --host=0.0.0.0

#browse to the machine ip with port 5000.
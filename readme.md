#create new dir
mkdir app
cd app
#git pull my files
git pull https://github.com/bliss81/dockerwebapp.git

#update linux 
sudo apt update
#download repository
sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu bionic stable"
#update linux 
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

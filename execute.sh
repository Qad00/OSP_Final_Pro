# Google signing key Download
# wget https://dl.google.com.linux.linux_signing_key.pub
# sudo apt-get install gnupg
# suge apt-key add linux_signing_key.pub

sudo apt-get -y update
sudo apt-get install -y wget
sudo apt-get install -y unzip
sudo apt-get install -y curl

wget -O /tmp/chromedriver.zip http://chromedriver.storage.googleapis.com/`curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE`/chromedriver_linux64.zip
sudo unzip /tmp/chromedriver.zip chromedriver -d /usr/local/bin/  

pip install selenium  
 
sudo sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list'
sudo apt-get install -y google-chrome-stable
 
pip install webdriver-manager

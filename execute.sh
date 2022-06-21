# Google signing key Download
# wget https://dl.google.com.linux.linux_signing_key.pub
# sudo apt-get install gnupg
# suge apt-key add linux_signing_key.pub

sudo apt-get -y update
sudo apt-get install -y wget
sudo apt-get install -y unzip
sudo apt-get install -y curl

# Driver Setting
wget -O /tmp/chromedriver.zip http://chromedriver.storage.googleapis.com/`curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE`/chromedriver_linux64.zip
sudo unzip /tmp/chromedriver.zip chromedriver -d /usr/local/bin/  

wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
sudo dpkg -i google-chrome-stable_current_amd64.deb 
 
sudo sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list'
sudo apt-get install -y google-chrome-stable

# Install Python Modules
sudo pip install --upgrade pip 
pip install selenium 
pip install webdriver-manager
pip install wordcloud
sudo pip install tensorflow
pip install keras
pip install konlpy

# Running Parts
python3 app.py --listen-port 5000

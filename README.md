# Fish Tracking
## Make new virtualenv using python3 
```
cd
git clone https://github.com/minamaged113/fish-tracking.git
cd fish-tracking
virtualenv -p python3 venv/
source venv/bin/activate
```
## Install requirements
remember to change the path according to your version of python
```
pip install -r requirements.txt
sudo apt-get install python3-tk
sudo apt-get install python3-pyqt5
CWD="$(pwd)" 
cp -r /usr/lib/python3/dist-packages/PyQt5 "${CWD}/venv/lib/python3.6/site-packages/PyQt5"
cp /usr/lib/python3/dist-packages/sip.cpython-*.so "${CWD}/venv/lib/python3.6/site-packages/"
```
## Running

mghobria@cse-cn0001.oulu.fi

/home/mghobria

/research/imag/development/

adm@ee.oulu.fi
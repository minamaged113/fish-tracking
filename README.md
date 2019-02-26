# Fish Tracking

## Make new virtualenv using python3

```bash
cd
git clone https://github.com/minamaged113/fish-tracking.git
cd fish-tracking
virtualenv -p python3 venv/
source venv/bin/activate
```

## Install requirements

remember to change the path according to your version of python

```bash
pip install -r requirements.txt
sudo apt-get install python3-tk
sudo apt-get install python3-pyqt5
CWD="$(pwd)"
cp -r /usr/lib/python3/dist-packages/PyQt5 "${CWD}/venv/lib/python3.6/site-packages/PyQt5"
cp /usr/lib/python3/dist-packages/sip.cpython-*.so "${CWD}/venv/lib/python3.6/site-packages/"
```

### Windows

- Install Anaconda/Miniconda
- Create new conda environmnet

```BATCH
conda create -n venv python=3.5
```

- Use `conda` package manager to install `numpy`, `pyqt`

```BATCH
conda install -n venv numpy=1.14.5 pyqt=5
```

- Activate `conda` environment

```BATCH
conda activate venv
```

- Run pip and python as usual

```BATCH
python -m pip install --upgrade pip
pip install -r requirements.txt
python main.py
```



## Read more
To find multiple research documents and articles about the topic, please
visit the following [link](https://drive.google.com/open?id=1KgClGqckIhT0QGq54mdBsHee9TkbQyAR)

## Sample Files
To find couple of sample files and their respective output, please refer
to the following [link](https://drive.google.com/open?id=1m71RbKyDRE8FwU-6GzVxIwKSSiS62A8S)

## Download Executables
To download the executable, click [here](https://drive.google.com/open?id=1OvX94rnJiemxXv8hHyNMWmjA6Ipl_06N)

## Build from Source

TODO

## State

- README [in Progress]
- Code comments [in Progress]
- Installation instructions [in Progress]
- Documentation [in Progress]
- User Manual [in Progress]
- MVP Architecture [in Progress]

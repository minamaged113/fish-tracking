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

## Running

mghobria@cse-cn0001.oulu.fi

/home/mghobria

/research/imag/development/

adm@ee.oulu.fi

## [Style Guide](https://www.python.org/dev/peps/pep-0008/)

The style guide is mainly following PEP-8 unless stated otherwise.

- [Indentation](https://www.python.org/dev/peps/pep-0008/#indentation): 4 spaces per indentation level.

- [Continuation lines](https://www.python.org/dev/peps/pep-0008/#indentation): aligned with opening delimiter.
- [if-Conditions](https://www.python.org/dev/peps/pep-0008/#indentation): Putting comment directly after.
- [Line length](https://www.python.org/dev/peps/pep-0008/#id19): Code: 79 Characters, Blocks: 72 Characters.
- [Line Break for Binary Operators](https://www.python.org/dev/peps/pep-0008/#id20): Before
- 2 blank lines surrounding top-level function and class definitions.
- Method definitions inside a class are surrounded by a single blank line.
- [Importing Order](https://www.python.org/dev/peps/pep-0008/#id23): Standard library - Third party - Local application/library specific.
- Avoid "from ´module´ import *".
- [Whitespaces](https://www.python.org/dev/peps/pep-0008/#id26).
- Don't use spaces around the = sign when used to indicate a keyword argument, or when used to indicate a default value for an unannotated function parameter.
- Comments are complete descriptive sentences.
- All variables are mixedCase.
- All acronyms are capitalized in variable names.
- _single_leading_underscore: internal use.
- single_trailing_underscore_: used by convention to avoid conflicts with Python keyword.
- __double_leading_underscore: when naming a class attribute, invokes name mangling.
- [Package and Module Names](https://www.python.org/dev/peps/pep-0008/#id40).
- [Class names](https://www.python.org/dev/peps/pep-0008/#id41) should normally use the CapWords convention.
- [Exceptions](https://www.python.org/dev/peps/pep-0008/#id43).
- Function names should be mixedCase.
- [Constants](https://www.python.org/dev/peps/pep-0008/#id48) are written in all capital letters with underscores separating words.
- Public attributes should have no leading underscores.
- Comparisons to singletons like None should always be done with is or is not, never the equality operators.

## Read more
To find multiple research documents and articles about the topic, please
visit the following [link](https://drive.google.com/open?id=1KgClGqckIhT0QGq54mdBsHee9TkbQyAR)

## Sample Files
To find couple of sample files and their respective output, please refer
to the following [link](https://drive.google.com/open?id=1m71RbKyDRE8FwU-6GzVxIwKSSiS62A8S)

## Download Executables
To download the executable, click [here](https://drive.google.com/open?id=1OvX94rnJiemxXv8hHyNMWmjA6Ipl_06N)

## State

- README [in Progress]
- Code comments [in Progress]
- Installation instructions [in Progress]
- Documentation [in Progress]
- User Manual [in Progress]
- MVP Architecture [in Progress]

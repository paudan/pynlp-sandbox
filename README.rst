A simple Python framework for NLP tasks based on NLTK, OpenNLP and TreeTagger tools.

Copyright (C) 2017 Paulius Danenas

Dependencies
------------

-  Python 2.7 or Python 3
-  `NLTK <http://nltk.org/>`__

Additional dependencies are listed in ``requirements.txt`` file.

This sandbox installs/integrates the following NLP tools:

-  `Apache OpenNLP <https://opennlp.apache.org/>`__
-  `TreeTagger <http://www.cis.uni-muenchen.de/~schmid/tools/TreeTagger/>`__
-  `Open Dutch Wordnet <https://github.com/cltl/OpenDutchWordnet>`__
-  `Pattern <https://github.com/clips/pattern>`__

Tested with OpenNLP 1.8 (using models built with 1.5), Python 2.7/3.5/3.6 and NLTK 3.2.4


Installation
------------

`PyBuilder <http://pybuilder.github.io/>`__ is required to build and run this framework. After performing ``git clone``, run
``pyb -P install_dir=.`` or (``pyb -P install_dir=<installation directory>``, if you need to specify installation directory). ``PyBuilder`` will download and
install all the required dependencies. After installation make sure that the required packages are installed by running
``pip install -r requirements.txt``.

Additionally, you can create virtual environment using Python ``virtualenv`` tool (make sure that it is installed before framework installation).
This can be automated by running ``install_venv.sh`` script.


Testing
-------

To ensure that installation was successful, several tests are provided. The most easiest way to run them is to run ``tox`` command
(`tox <https://tox.readthedocs.io/en/latest/>`__ must be installed). Alternatively, one may run them using ``nose``.


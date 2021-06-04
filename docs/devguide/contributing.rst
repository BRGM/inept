Contributing
============

Discussions
-----------

If you have any questions or suggestions about inept, please do so here: https://github.com/BRGM/inept/discussions.


Repository
----------

The public repository is https://github.com/brgm/inept.

You can clone and start working on the code with:

.. code-block:: bash

  $ git clone https://github.com/BRGM/inept.git
  $ cd inept/


For now, the developments are done on a restricted repository: https://gitlab.inria.fr/charms/inept.
The github repository is a mirror of the main branch.


Preparing the environment
-------------------------

You can prepare a (conda) virtual environment with:

.. code-block:: bash

  $ conda create -n inept pip
  $ conda activate inept


Install the development dependencies with:

.. code-block:: bash

  $ pip install -r requirements.txt

Run the tests with:

.. code-block:: bash

  $ pytest


Building the documentation
--------------------------

The documentation sources are in the :code:`docs/` directory:

.. code-block:: bash

  $ cd docs/

Install the sphinx dependencies with:

.. code-block:: bash

  $ cd docs/
  $ pip install -r requirements

Build the documentation with:

.. code-block:: bash

  $ make html

Open the file :code:`docs/_build/index.html` in your browser to see the result.


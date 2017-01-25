********
spanners
********

Environment setup
=================


C/C++ Dependenciess:
--------------------

Although much code runs Python, several external (non Python) libraries are
called from within Python. Make sure the following dependencies are made
available:

- python3.6-dev

Install these packages on Debian based distributions using:

.. code-block:: sh
    # apt-get install python3.6-dev


Python
------

It is highly recommended to run everything in an up-to-date virtualenv.
The environment can be set up using:

.. code-block:: sh

    $ TMP=$(mktemp -d)
    $ virtualenv "$TMP" --python=python3.6
    $ source "$TMP/bin/activate"


In order to run or deploy the project, it is necessary to download the
dependencies. These packages will be loaded as vendor modules at runtime.

The project can be installed using:

.. code-block:: sh

    $ pip install matplotlib~=1.5.3
    $ pip install -e .


The project can be installed in development mode using:

.. code-block:: sh

      $ pip install -r dev-requirements.txt

Windows version:
> python -m pip install -r dev-requirements.txt

Running
=======

To generate a data challenge file run the following command:

.. code-block:: sh

    $ spanners generate 1000 1000 40 20 data.txt

Or if in windows: service.generate(1000,1000,40,20,"data")
Note: first go to the correct directory, open python terminal and import service (from spanners import service)


To view the problem of a data challenge file run the following command:

.. code-block:: sh

    $ spanners show problem data.txt


To view the solution of a data challenge file run the following command:

.. code-block:: sh

    $ spanners show solution -a wspd -c data.txt



Tests
=====

Tests can be run using:

.. code-block:: sh

    $ tox

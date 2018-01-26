.. image:: https://img.shields.io/pypi/v/nerodia.svg
    :target: https://pypi.python.org/pypi/nerodia

.. image:: https://img.shields.io/pypi/pyversions/nerodia.svg
    :target: https://pypi.python.org/pypi/nerodia

.. image:: https://travis-ci.org/watir/nerodia.svg?branch=master
    :target: https://travis-ci.org/watir/nerodia

.. image:: https://ci.appveyor.com/api/projects/status/7go9s2tmp2av08sa?svg=true
    :target: https://ci.appveyor.com/project/joshmgrant/nerodia/branch/master


-----

Introduction
============
Nerodia is a Python port of the Watir ruby gem. https://github.com/watir/watir

Supported Python Versions
=========================

* Python 2.7
* Python 3.4+

Installing
==========

If you have `pip <https://pip.pypa.io/>`_ on your system, you can simply install or upgrade::

    pip install -U nerodia

Alternately, you can download the source distribution from `PyPI <http://pypi.python.org/pypi/nerodia>`_ (e.g. nerodia-1.0.0.tar.gz), unarchive it, and run::

    python setup.py install


API Documentation
=================

For specific documentation of Nerodia's API, `please see the Nerodia API Documentation <./api.html>`_.

Differences from Watir
======================

The goal of this project is to be as close to Watir as possible. In terms of functionality, it is equivalent; however, there are some syntax differences due to the nature of Python.

Containers
----------

The following containers cannot be used because either the singular or plural version is reserved by Python.

    +------------+-------------+
    |    Watir   |   Nerodia   |
    +============+=============+
    |  a         |  link       |
    +------------+-------------+
    |  as        |  links      |
    +------------+-------------+
    |  del       |  delete     |
    +------------+-------------+
    |  dels      |  deletes    |
    +------------+-------------+
    |  i         |  ital       |
    +------------+-------------+
    |  is        |  itals      |
    +------------+-------------+

Locators
--------

The following locators cannot be used because they are reserved by Python.

    +------------+-------------+
    |    Watir   |   Nerodia   |
    +============+=============+
    |  class     |  class_name |
    +------------+-------------+
    |  for       |  N/A*       |
    +------------+-------------+
    *\*This locator is only possible via the below options.*

Alternatively, if you are only using one locator you can pass them as individual arguments:

.. code-block:: python

    browser.div('class', 'spam')

A third option is to use a dictionary and unpack into the container:

.. code-block:: python

    locator = {'class': 'spam', 'index': 1}
    browser.div(**locator)

Blocks
------

Since Python does not have blocks, alternate methods are required.

Context
```````
For cases where we want to perform some actions inside of a different browser context without completely switching to that context, we use the context manager.

Consider the following Window switching Watir code:

.. code-block:: ruby

  browser.window(title: 'Spam and Ham!').use do
    browser.button(id: 'close').click
  end

In Nerodia, the equivalent would be:

.. code-block:: python

    with browser.window(title='Spam and Ham!'):
        browser.button(id='close').click()

The same would go for frames.

Waits
`````

For waits, we need to use ``lambdas`` or ``closures``.

Consider the following wait Watir code:

.. code-block:: ruby

  btn = browser.button(id: 'btn')
  btn.wait_until(timeout: 2, interval: 0.5) { btn.enabled }
  btn.click

In Nerodia, the equivalent would be:

.. code-block:: python

    btn = browser.button(id='btn')
    btn.wait_until(timeout=2, interval=0.5 method=lambda e: e.enabled)
    btn.click()

Also, ``while`` is reserved in Python. Therefore, the Nerodia equivalent of Watir's ``Wait.while`` is ``Wait.until_not``

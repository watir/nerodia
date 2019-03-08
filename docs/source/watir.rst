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
    btn.wait_until(timeout=2, interval=0.5, method=lambda e: e.enabled)
    btn.click()

Also, ``while`` is reserved in Python. Therefore, the Nerodia equivalent of Watir's ``Wait.while`` is ``Wait.until_not``

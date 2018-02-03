Examples
========

* `Navigate to a Website`_
* `Perform a Google Search`_
* `Select a Checkbox`_
* `Elements in Frames`_

Navigate to a Website
--------------

.. code-block:: python

    from nerodia.browser import Browser

    browser = Browser(browser='firefox')
    browser.goto('watir.com')

    browser.close()

Perform a Google Search
-----------------------

.. code-block:: python

    from nerodia.browser import Browser

    browser = Browser(browser='firefox')
    browser.goto('google.com')

    search_input = browser.text_field(title='Search')
    search_input.value = 'nerodia'
    browser.button(value='Google Search').click()

    browser.close()

Select a Checkbox
-------------------------

.. code-block:: python

    from nerodia.browser import Browser

    browser = Browser(browser='firefox')
    browser.goto('the-internet.herokuapp.com/checkboxes')

    checkbox1 = browser.checkbox()
    checkbox1.set()

    browser.close()

Elements in Frames
-------------------

.. code-block:: python

    from nerodia.browser import Browser

    browser = Browser(browser='firefox')
    browser.goto('the-internet.herokuapp.com/iframe')

    print(browser.iframe().p().text)
    print(browser.link(css='#page-footer a').text)

    browser.close()

Result:

.. code-block:: shell

    > Your content goes here.
    > Elemental Selenium

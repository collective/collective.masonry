Introduction
============

This add-on is inspeared by ContentWellPortlets_. Main differences are:

* You can add as many portlets as you want above and below the content body.
* There is only one manage portlet screen
* Portlets layout can be configured
* Portlets layout can be extended in many ways

Layout
======

Layout is controlled with many axes. The main idea is to force all portlets
in above and below the content to float from left to right.

But portlet has no forced width, so here you have many 'mode' you can configure
per page for above and below. Note 'above' and 'below' portlets can use a
different mode.

Availables modes:
* fixed with 220
* min-max: 220 - 300
* free

The height is not forced. This is where the jquery.masonry plugin comes in
action. Portlets will be moved to build a layout with a minimal height.
You can disable this behavior by just unactivate the corresponding javascript::

  <javascript id="++resource++collective.masonry/masonry.js" enabled="False" />


Some mode can force you to review the masonry configuration exposed in the 
viewlet configuration.

Credits
=======

Companies
---------

|makinacom|_

* `Planet Makina Corpus <http://www.makina-corpus.org>`_
* `Contact Makina Corpus <mailto:python@makina-corpus.org>`_

Authors
-------

- JeanMichel FRANCOIS aka toutpt <toutpt@gmail.com>

.. Contributors
.. ------------

.. |makinacom| image:: http://depot.makina-corpus.org/public/logo.gif
.. _makinacom:  http://www.makina-corpus.com
.. _masonry: http://desandro.com/resources/jquery-masonry
.. _ContentWellPortlets: http://pypi.python.org/pypi/Products.ContentWellPortlets

Django Enquiry
==============

A reusable Django app to host multilingual polls on your site.


Installation
------------

If you want to install the latest stable release from PyPi::

    $ pip install django-enquiry

If you feel adventurous and want to install the latest commit from GitHub::

    $ pip install -e git://github.com/bitmazk/django-enquiry.git#egg=enquiry

Add ``enquiry`` to your ``INSTALLED_APPS``::

    INSTALLED_APPS = (
        ...,
        'enquiry',
    )

Run the South migrations::

    ./manage.py migrate enquiry


URLs or Apphook
---------------

You can just add the enquiry urls to your ``urls.py`` or choose the
apphook in your django-cms page.


Templatetags
------------

render_current_poll
+++++++++++++++++++

This inclusion tag allows you to render the currently active poll anywhere
on your site::

    {% load enquiry_tags %}
    {% render_current_poll %}

If you want to customize the ouput of this tag, please override the
`enquiry/current_poll.html` template.

get_current_poll
++++++++++++++++

This assignment tag allows you to get the current poll and render it however
you like it::

    {% load enquiry_tags %}
    {% get_current_poll as poll %}
    <h1>{{ poll.get_translation.question }}</h1>


Contribute
----------

If you want to contribute to this project, please perform the following steps::

    # Fork this repository
    # Clone your fork
    $ mkvirtualenv -p python2.7 django-enquiry
    $ pip install -r requirements.txt
    $ ./logger/tests/runtests.sh
    # You should get no failing tests

    $ git co -b feature_branch master
    # Implement your feature and tests
    # Describe your change in the CHANGELOG.txt
    $ git add . && git commit
    $ git push origin feature_branch
    # Send us a pull request for your feature branch

Whenever you run the tests a coverage output will be generated in
``tests/coverage/index.html``. When adding new features, please make sure that
you keep the coverage at 100%.


Roadmap
-------

Check the issue tracker on github for milestones and features to come.

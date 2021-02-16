=============
Customisation
=============

SimpleVPN is written in a modular fashion, allowing for easy plugin development and implementation.


Writing Custom Modules (Plugins)
================================

You may write your module as any other Django Reusable App.
Refer to the `Django Documentation <https://docs.djangoproject.com/en/3.1/intro/reusable-apps/>`_
to learn more about it.

SimpleVPN provides utilities to let you write your own module to extend its capabilities.

Before listing them, keep in mind there currently are some limitations:
 - there's no standard way to add additional requirements. You either install them yourself or use the pre-installed ones.
 - Bootstrap is globally imported. This may very well interfere with a custom frontend design for your module.


Available Tools
---------------

By default, your module has access to the following tools:
 - `django-crispy-forms <https://django-crispy-forms.readthedocs.io/en/latest/>`_
 - `django-bootstrap-pagination <https://github.com/jmcclell/django-bootstrap-pagination>`_
 - `django-wireguard <https://thatsed.gitlab.io/django-wireguard/>`_
 - `whitenoise <http://whitenoise.evans.io/en/stable/>`_


Getting Started
---------------

First, create your app by running ``./manage.py startapp my_vpn_module`` (or use ``django-admin``)

Your package should look something like this:

.. code-block::

   my_vpn_module/
    |- migrations/
    |- templates/
    |  |- my_vpn_module
    |     |- index.html
    |- static/
    |- locale/
    |- admin.py
    |- apps.py
    |- forms.py
    |- models.py
    |- tests.py
    |- urls.py
    |- views.py


In the ``apps.py`` file, you can add some custom parameters for your App:

.. code-block:: python

   class MyVpnModuleConfig(AppConfig):
       name = 'my_vpn_module'
       verbose_name = _("My VPN Module")

       # all options are optional
       module_config = {
         'title': _("My VPN Module")
         'slug': 'my-vpn',
         'namespace': 'myvpn',
         'index': 'home'
       }


We will explain how to configure it in a bit.

In the ``__init__.py`` file, you should set the ``default_app_config``:

.. code-block:: python

   """My VPN Module Docstring"""
   default_app_config = 'my_vpn_module.apps.MyVpnModuleConfig'


In the ``urls.py`` file, set an ``app_name`` and a index url:

.. code-block:: python

   app_name = 'my_vpn_module'

    urlpatterns = [
        path('', views.IndexView.as_view(), name='home'),
        ...
    ]


Setup your base template by extending the ``base.html`` template.
Use this new template as a base for the other module's templates.

Provided blocks are all in this snippet:

.. code-block:: html

   {% extends "base.html" %}
   {% load i18n %}

   {% block module_css %}
     {% block extra_css %}{% endblock %}
   {% endblock %}

   {% block title %}{% trans "My VPN Module" %}{% endblock %}

   {% block module_content %}
     <div class="container">
       <nav aria-label="breadcrumb">
         <ol class="breadcrumb">
           <li class="breadcrumb-item"><a href="{{ current_module.index }}">{{ current_module.title }}</a></li>
             {% block breadcrumb_items %}{% endblock %}
           </ol>
         </nav>
         <ul class="nav nav-pills mb-4">
           <li class="nav-item">
             <a class="nav-link{% if request.resolver_match.url_name == 'index' %} active{% endif %}" href="{% url 'vpn_manager:index' %}">Home</a>
           </li>
         </ul>
         {% block content %}{% endblock %}
       </nav>
     </div>
   {% endblock %}

   {% block module_js %}
     {% block extra_js %}{% endblock %}
   {% endblock %}


Configuration Options
---------------------

Available Configuration Options:
 - ``title``: defaults to the AppConfig's ``verbose_name``.
 - ``slug``: URL path at which your module will be served.
   For example, ``my-vpn`` will be served at a base url of ``example.com/my-vpn/``
 - ``namespace``: the namespace for the URL resolve. Your module's ``urls.urlpatterns`` will be namespaced with this value.
   Defaults to the module's name.
   Example: if namespace is ``myvpn``, you can resolve your URLs using ``{% url 'myvpn:index' %}``
 - ``module_name``: don't override this value. It is used to resolve the plugin's python package.
 - ``index``: the index view name. This is the default redirect when selecting your module.
   Example: see the ``urls.py`` example above; to set the entrypoint to the view with ``name='home'``, use ``home`` as value for this option.


Enabling Plugins
----------------

To enable a plugin, add it in ``SimpleVPN.modules.MODULES``. You may override ``module_config`` options in the dictionary,
leave it empty to use the default ones specified either in its `AppConfig` or computed automatically.

.. code-block:: python

   MODULES = [
       ('vpn_manager', {}),
       ('my_vpn_module', {}),
   ]

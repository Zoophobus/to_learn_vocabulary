# to_learn_vocabulary
A Python Django project that provides a simple interface and databases for learning vocabulary

# The basic premise of this is that to provide a simple system and interface using django for learning vocabulary. The requirements for this are: 
  - multiple translations need to be allowed
  - categorisation of the vocabulary lists for learning is needed
  - specific translations can fall into multiple categories
  - need to be able to remove/delete translations

# All of these requirements are met in the provided codebase. 
An additional feature would be to add greater flexibility to add translations (also a better 
form for doing so) and a more powerful system for removing translations (removing whole 
categories and filtering the lists for specified categories)

# NOTE
this is rough and ready, testing is not provided and has not been performed beyond the basic 
efforts of "getting it to work". This is a poor approach to use and is a bad example, but this
is small, simple and mundane. It's mainly here to help my partner learn Dutch vocabulary, like
I have been using this myself!!


# INSTALLATION

For installation Python and Python Django are required, dependencies should be met from the
supplied libraries. For this it is of course recommended to create a container (`python -m venv 
path/to/VIRTUALENV`) and install Django in this container (using `source path/to/VIRTUALENV/bin/activate`
to load the environment, and `pip install django=4` to install Django).

Once Python and django are setup then one is required to create the Python Django project. For this the
Django environment needs to be loaded first (`source path/to/virtualenv/bin/activate`). Then a project 
needs to be created where you want to "install" the code (first move to the directory where you want to
"install" this, `cd xxxx` then create the project `django-admin startproject PROJECTNAME`). This creates
the basic Django file structure including the settings (that you'll need to modify to get the code to run).

With the Django project up and running you can create the app (move to the location of the django project 
`cd xxxx` and then execute `python manage.py startapp APPNAME`). This will create the directory structure
and the basic files required for an app, these are located in a directory named after APPNAME within the 
project. The files from this repository can be placed within this app directory (APPNAME) to "install" the
project. To get the files either download and unzip them from the browser, or (if you want to look "cool")
run `git clone https://github.com/Zoophobus/to_learn_vocabulary.git` (after installing the git cli, which
would be another task, although not difficult). Though, if you have been reading this file to this point 
I might suspect that you are not that cool, because someone truly cool would not bother to read this at all!

After this configuration needs to be performed for the project to be run. First of all you will need to find
the `settings.py` file in the django project (located in the `PROJECTNAME/` directory where the project was created).
Then under the section (The list/array) titled `INSTALLED_APPS` a line needs to be added with a text editor,
this line should look like `'APPNAME.apps.APPNAMEConfig',`, where APPNAME refers to the name given to the app.
Further down in this settings file you need to find the `TIME_ZONE` line and change this to the local timezone,
for myself this looks like `TIME_ZONE = 'Europe/Amsterdam'`. Sometimes I find difficulties with the urls and
redirection and include the line `APPEND_SLASH=False` at the bottom of the file.

Then, in the same location as the `settings.py` file there is a `urls.py` file. This needs to be altered to include
the app url, this can be done by finding the `urlpatterns` section (list/array) and adding the line 
`path('',include('APPNAME.urls')),`.

Finally, before you run the app the app databases need to be created. To do this you need to execute the django
command by running `python manage.py migrate` from within the django environment.

# Running!
At this point to run this you need to run the django server, which after loading the django environment (`source
path/to/VIRTUALENV/bin/activate`) can be done by executing `python manage.py runserver` from the location of the
python project. Then connect to the link with your favourite browser (either right click on the address `http://111.0.0.1:8000/`,
or copy and paste it into the browser).

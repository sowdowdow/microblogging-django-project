# MicroBlogging Project - Open Source

[![Build Status](https://travis-ci.org/sowdowdow/microblogging-django-project.svg?branch=master)](https://travis-ci.org/sowdowdow/microblogging-django-project)
[![Python Version](https://img.shields.io/badge/python-3.6.7-brightgreen.svg)](https://python.org)
[![Django Version](https://img.shields.io/badge/django-2.1.3-brightgreen.svg)](https://djangoproject.com)


> Authors :  
Simon Dormeau (Sowdowdow)
Lucille Tyrakowski (Tearaluna)
## Goal of the project
This project is (proudly ?) made in french.

The goal of this one is to learn **Python**, **Django** and **TDD** at the same time *ough* !
The concept is simple, a **public blog** where anybody can register and write some articles, delete or modify them.

- The practice of Test Driven Development is implemented through *Django* and tests are run by *TravisCI*.

- Users are implemented through Django's Users while Posts are made by hand.

- We use Bulma as css framework.

| Constraints |
|---------------------------------------------------------------------------------------------------------------------|
| As a user I can register an account and I can login |
| As a user I can login in order to create a new *entry* |
| As a user I can create a new *Post* in order to share informations with people. |
| As a user I can *modify* and *delete* my posts |
| As a visitor, I have access to a listing of latest posts on the index page |
| As a visitor I can see all the publications from a user (on many pages if necessary) in order to read more from him |

The subject can be found [here](https://www.delahayeyourself.info/modules/LP%20Web%20Dynamique/django/projet/).  
The presentation can be found [here](https://docs.google.com/presentation/d/1XHCNQMNqVo_lfPuM2SmqDILuf-K4GcYQjZnAFyZdq4I)

## Main features
 - Any user can register an account / login / lougout /change password
 - Any user can read any `Post`
 - Any user can create / update / delete his `Posts`
## Additionnal features
 - [RTF](https://fr.wikipedia.org/wiki/Rich_Text_Format) `Post` edition
 - Any user can `Comment` any `Post`
 - Any user can create / update / delete his `Comments`
 - Any user can `Like` any `Post`
 - Any user can delete his `Likes`

## Installation

To install this project you need to install `git`, `python3`, `pip` and `VirtualEnv` preferably on a Linux environment.  
Next, make a virtual env :  
 - `virtualenv -p python3 <foldername>`

Go into this folder, then activate the environment :  
 - `cd <foldername>`
 - `source bin/activate`

Clone the repository and go inside the folder :
 - `git clone https://github.com/sowdowdow/microblogging-django-project`
 - `cd microblogging-django-project/`

Install requirements :
 - `pip install -r requirements.txt`

Launch server :
 - `python manage.py runserver`

That's it ! now you can try it at http://127.0.0.1:8000/.

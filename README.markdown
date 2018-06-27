# Game of Buttholes: The Will of the Prophets

A web app for the board game played by the hosts of [The Greatest Generation](http://gagh.biz) that I'm a little embarrassed to be involved with.

[More information on Wikia.](http://greatestgen.wikia.com/wiki/DS9_Board_Game_(Game_of_Buttholes))

[![Build Status](https://www.travis-ci.org/craiga/will-of-the-prophets.svg?branch=master)](https://www.travis-ci.org/craiga/will-of-the-prophets)

# Getting Started

Once you've checked out this repository, getting this project up and running should be simple.

    pipenv install --dev
    pipenv run python manage.py loaddata buttholes special_squares rolls
    pipenv run python manage.py runserver

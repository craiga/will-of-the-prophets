# Game of Buttholes: The Will of the Prophets

A web app for the board game played by the hosts of [The Greatest Generation](http://gagh.biz) that I'm a little embarrassed to be involved with.

[More information on Wikia.](http://greatestgen.wikia.com/wiki/DS9_Board_Game_(Game_of_Buttholes))

[![Build Status](https://www.travis-ci.org/craiga/will-of-the-prophets.svg?branch=master)](https://www.travis-ci.org/craiga/will-of-the-prophets) [![Maintainability](https://api.codeclimate.com/v1/badges/ce9890b522fe6312945e/maintainability)](https://codeclimate.com/github/craiga/will-of-the-prophets/maintainability) [![Test Coverage](https://api.codeclimate.com/v1/badges/ce9890b522fe6312945e/test_coverage)](https://codeclimate.com/github/craiga/will-of-the-prophets/test_coverage)

# Getting Started

Once you've checked out this repository, getting this project up and running should be simple.

    pipenv install --dev
    pipenv run python manage.py migrate
    pipenv run python manage.py loaddata buttholes special_squares rolls
    pipenv run python manage.py runserver

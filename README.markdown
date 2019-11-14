# Game of Buttholes: The Will of the Prophets

A web app for the board game played by the hosts of [The Greatest Generation](http://gagh.biz) that I'm a little embarrassed to be involved with.

[More information on Wikia.](http://greatestgen.wikia.com/wiki/DS9_Board_Game_(Game_of_Buttholes))

![CircleCI branch](https://img.shields.io/circleci/project/github/craiga/will-of-the-prophets/master.svg) ![Security Headers](https://img.shields.io/security-headers?url=https%3A%2F%2Fwill-of-the-prophets.herokuapp.com)


# Getting Started

Once you've checked out this repository and installed [pipenv](http://pipenv.readthedocs.io), getting this project up and running should be simple.

    echo "DEBUG=1" > .env
    pipenv install --dev
    pipenv run python manage.py migrate
    pipenv run python manage.py loaddata buttholes special_squares rolls
    pipenv run python manage.py runserver

# Code Formatting

Code is formatted with [black](https://black.readthedocs.io/en/latest/):

    pipenv run black .

# Developing with CSS

CSS is built from Sass using django-sass-processor. To compile CSS, use the `compilescss` command.

When making changes to style.scss, remove style.css from the static directory and it will be rebuilt whenever a change is made.

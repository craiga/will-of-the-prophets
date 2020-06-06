# Game of Buttholes: The Will of the Prophets

A web app for the board game played by the hosts of [The Greatest Generation](http://gagh.biz) that I'm a little embarrassed to be involved with.

[More information on Wikia.](http://greatestgen.wikia.com/wiki/DS9_Board_Game_(Game_of_Buttholes))


# Getting Started

Once you've checked out this repository and installed [pipenv](http://pipenv.readthedocs.io), getting this project up and running should be simple.

```
make setup-dev
make
```

Run `make help` for descriptions of other commands!
`

# Developing with CSS

CSS is built from Sass using django-sass-processor. To compile CSS, run `make scss`.

When making changes to style.scss, remove style.css from the static directory and it will be rebuilt whenever a change is made.

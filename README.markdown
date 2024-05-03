# Game of Buttholes: The Will of the Caretaker

A web app for the board game played by the hosts of [The Greatest Generation](http://gagh.biz) that I'm a little embarrassed to be involved with.

[More information on Wikia.](<http://greatestgen.wikia.com/wiki/DS9_Board_Game_(Game_of_Buttholes)>)


# Developing with CSS

CSS is built from Sass using django-sass-processor. To compile CSS, run `make scss`.

When making changes to style.scss, remove style.css from the static directory and it will be rebuilt whenever a change is made.

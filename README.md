## About

Welcome!  For this project, I used the object-oriented approach.  The project structure looks like:

	.
	├── lib
	│   ├── classes.py  -->  Card, Deck, and Player classes
	│   ├── config.py  -->  global variables
	│   ├── decorate.py
	│   ├── game.py  -->  controls game flow (look at this file first)
	│   ├── utils.py
	│   └── validate.py  -->  error messages and input validation
	└── main.py  -->  kicks off the entire program

There is also a `data` folder that stores images and their corresponding generated ascii image strings.  The scripts `crop.py` and `html_to_pystring.py` automate part of the image generation.  The generate ascii image strings are checked into the repository, so there is no need to rebuild them, but feel free to look at the scripts if you so please.



## Installation

TLDR: Dependencies are

  * **[Python 3.7](https://www.python.org/downloads/release/python-372/)**
  * [colorama](https://pypi.org/project/colorama/#files)
  * [sty](https://github.com/feluxe/sty)



## Usage

Simply run the `main.py` script.  For example:

    cd card-game-matthew-lancellotti
    ./main.py




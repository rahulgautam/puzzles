About Puzzle
=============
cube is an HTML5 web-based tiny web application build on top of tonrnado.
Right now it has implemented a `Shaddy Puzzle <http://en.wikipedia.org/wiki/Nonogram>`_

Features include:
-----------------
    * Support sign in with google accounts.
    * Algorithm for shady puzzle is completely dynamic. ( Also supports multiple solution check )
    * Multiplayer with real time player score updates ( Web Sockets used for that)
    * Communication over HTTPS
    
How to Run:
-----------
     Python should be >= 2.6 , tornado >= 2.3
     # unzip cube_shaddy_puzzle.zip
     # cd cube_shaddy_puzzle
     # chmod +x cube.py
     # ./cube.py

URL: https://localhost:8000

Screenshots
-----------
.. figure:: http://i.imgur.com/ET1mr.png
    :align: center

    Single Player Mode

.. figure:: http://i.imgur.com/IeQDh.png
    :align: center

    Choose Game Type

.. figure:: http://i.imgur.com/NBTIG.png
    :align: center

    Login Page


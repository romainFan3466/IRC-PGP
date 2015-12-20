IRC-PGP
=======
IRC-PGP encryption project - Software Dev 4th - IT Carlow

irc-client script 
--------------------

|  Short form          | Long form     | Explanation | Default |
 ----------------- | ---------------------------- | ------------------|--------------------------
| `-h` | `--help`| Display help | |
| `-m` | `--mode`| Set the mode : listener or sender. | listener |
| `-ho`| `--host` | IRC Server host. | Romain's server host |
| `-ch` | `--channel` |IRC Server channel to join. Must start by #  | |
| `-nick` | `--nickname` |Client nickname | |
|`-po`| `--port` | IRC Server port. | 6666 |
|`-pw`|`--password`| IRC Server password if required | |


Executable
--------------
An executable has been compiled and no libraries are required. 
Unzip `ConnectionWidget.zip` then move into the folder ConnectionWidget

Then run the executable : 
    
    ./ConnectionWidget


Script
--------
To execute the script, move into `app` folder then run : 

	python3 ConnectionWidget.py
    
> **Note:** Make sure all dependencies are installed

Dependencies
------------------
 - [PyQt5](https://riverbankcomputing.com/software/pyqt/download5)
 - [Jaraco Irc 13.2](https://github.com/jaraco/irc) 

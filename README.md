[license-shield]: https://img.shields.io/badge/License-GPL3.0-green.svg
[license]: https://github.com/MauricePascal/WhatsApp-Chat-AI/tree/main/LICENSE

[ ![license-shield][] ][license]
# WhatsApp-Chat-AI
Artificial Intelligence for WhatsApp Chats. Let your WhatsApp contacts chat with an AI

## Getting Started
If you downloaded the program, you have to download the needed depenencies:
- selenium
- numpy
- nltk
- torch

After you installed all the dependencies successfully, you have to train the ai
```
$ python ./ai/train.py
```
Then you have to run the main file with
```
$ python ./main.py
```
If you did everything right, there should open a chrome window with a QR code. Scan this QR code an look in the console. Type the name of the contact who wants to chat with the ai. 

If the program could find the user, your contact can chat with the implemented AI ("Artificial Intelligence")

## License
This program is licensed under the [GNU General Public License v3.0][license]

## Notes
- There is currently a problem with the message receiver. Im on it!

_Copyright (C) 2020 by Maurice-Pascal Larivière. All rights reserved_

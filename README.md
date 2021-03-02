# suttas_text_and_audio

Experimental client for processing text and audio of the pali canon and of its english translations by Venerable Sujato. The translations and root texts have been forked from https://github.com/suttacentral/bilara-data

Important note: At the moment only the suttas from the long, the middle-length, the numbered, and the linked discourse are working. The interface for the Pali is not finished yet.

Usage: 
- Run a local webserver in chrome and serve index.html
- Pressing space-bar advances a reading from the sutta line by line
- Use the text input at the top to load a sutta. 

Use the following format for looking up a sutta:
'mn', 'dn', an, sn, followed by the index number of the sutta.
For example, 'mn1' loads the first sutta of the middle-length discourses, 'dn1' loads the first sutta of the long discourses. 

Plans:
- better navigation
- use of regular expressions to search and to analyze the text of the suttas
- voice navigation
- a map and images of places mentioned in the sutta that is selected for reading
- links to explantions, for example about the names of venerables and lay-persons mentioned in the suttas
- sutta classification, for example according to the simile used, or according to a core teaching, such as the four noble truths, the noble eightfold path, dependent origination, and rebirth.

This app uses p5.js and p5.speech.js
Thanks to Daniel Shiffman for the demos of p5.speech

Jetavana image attribution:
myself, CC BY-SA 2.5 <https://creativecommons.org/licenses/by-sa/2.5>, via Wikimedia Commons
https://commons.wikimedia.org/wiki/File:Jetavana.jpg
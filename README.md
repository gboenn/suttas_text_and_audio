# suttas_text_and_audio

Experimental client for processing text and audio of the pali canon and of its english translations by Venerable Sujato. Data copied from SuttaCentral github repo.

Run a local webserver in chrome and serve index.html

Pressing space-bar advances a reading from the sutta line by line

Use the text input at the top to load a sutta. 
Use the following format for looking up a sutta:
'mn' followed by three digits for the number of the sutta.
For example, 'mn001' loads the first sutta of the middle-length discourses, 'mn002' the second, 'mn003' the third, until 'mn152' for the last sutta of the middle-length discourses.

Plans:
- better navigation
- use regular expressions to search and to analyze the text of the suttas
- voice navigation
- a map and images of places mentioned in the sutta that is selected for reading
- links to explantions, for example about the names of venerables and lay-persons mentioned in the suttas
- sutta classification, for example according to the simile used, or core teachings, such as the four noble truths, noble eightfold path, dependent origination, and rebirth

This app uses p5.js and p5.speech.js
Credit to Daniel Shiffman for the demo of p5.speech

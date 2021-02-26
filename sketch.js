// http://127.0.0.1:8887/
// Georg Boenn, 2021

// Daniel Shiffman
// http://codingtra.in
// http://patreon.com/codingtrain
// Code for: https://youtu.be/v0CHV33wDsI

let speech;
// let txt = "Better than a thousand useless words is a single word that brings you peace.";
// let txt = "Should a person do good, let them do it again and again."
let txt = "Don’t run back to the past, don’t hope for the future. What’s past is left behind"; 
let txt1 = "the future has not arrived; and phenomena in the present are clearly seen in every case. Knowing this, foster it—unfaltering, unshakable.";
let txt2 = "Today’s the day to keenly work—who knows, tomorrow may bring death! For there is no bargain to be struck with Death and his mighty hordes.";
let txt3 = "The peaceful sage explained it’s those who keenly meditate like this, tireless all night and day, who truly have that one fine night.";

let verse = [];
let voice;
let counter = 0;
let voiceId =  54;

  //Tessa 36
  //Google UK English Female 49
  //Google UK English Male 50
  //Samantha 32
  //Google US English 48
  //Karen 17
  //Moira 28
  //Tessa 36
  //Veena (ind) 39
  //Google हिन्दी 54

let sutta_po;

function preload() { 
  sutta_po = loadStrings('./suttas/sc-data-master/po_text/pli-en/mn/mn131.po');
  console.log(sutta_po);
}

function parse() {
  let verse_count = 0;
  for (let i = 0; i < sutta_po.length; i++){
    v = sutta_po[i].split('"');
    if (v[0] === "msgstr " && v[1] !== "" ) {
      console.log(v[1]);
      verse[verse_count++] = v[1];
    }
  }
  console.log(verse);
}

function setup() {
  createCanvas(400, 100);
  background(0);
  parse();
  console.log(verse);

  speech = new p5.Speech(); // speech synthesis object
  speech.onLoad = voiceReady;

  speech.interrupt = true;
  speech.started(startSpeaking);
  speech.ended(endSpeaking);

  function startSpeaking() {
    background(0, 255, 0);
  }

  function endSpeaking() {
    background(0);
  }

  function voiceReady() {
    voice =  speech.voices[voiceId];
    console.log('voice ready');
    console.log(speech.voices);
  }
}

function keyPressed() {
  console.log(key);
  if (key == " ") {
    speak_now();
  }
}

function speak_now () {
  speech.setRate(1);
  speech.setPitch(1);
  speech.setVoice(voice.name);
  speech.speak(verse[counter]); 
  createP(verse[counter]);
  counter+=1;
  if (counter == verse.length) {
     counter = 0;
  }
}

function mousePressed() {
  speak_now();
}

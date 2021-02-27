// http://127.0.0.1:8887/
// Georg Boenn, 2021

// after an example by
// Daniel Shiffman
// http://codingtra.in
// http://patreon.com/codingtrain
// Code for: https://youtu.be/v0CHV33wDsI

let speech;
// let txt = "Better than a thousand useless words is a single word that brings you peace.";
// let txt = "Should a person do good, let them do it again and again."
// let txt = "Don’t run back to the past, don’t hope for the future. What’s past is left behind"; 
// let txt1 = "the future has not arrived; and phenomena in the present are clearly seen in every case. Knowing this, foster it—unfaltering, unshakable.";
// let txt2 = "Today’s the day to keenly work—who knows, tomorrow may bring death! For there is no bargain to be struck with Death and his mighty hordes.";
// let txt3 = "The peaceful sage explained it’s those who keenly meditate like this, tireless all night and day, who truly have that one fine night.";

let verse = [];
let pali = [];
let voice;
let counter = 0;
let pali_counter = 0;
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
let bg_img_1;
let sentence;

let sutta_string = './suttas/sc-data-master/po_text/pli-en/mn/';



function preload() { 
  sutta_po = loadStrings('./suttas/sc-data-master/po_text/pli-en/mn/mn002.po');
  bg_img_1 = loadImage('./img/jetavana.jpg');
  //console.log(sutta_po);
}

function parse(sutta) {
  verse = [];
  pali = [];
  verse_count = 0;
  pali_count = 0;
  for (let i = 0; i < sutta.length; i++){
    v = sutta[i].split('"');
    if (v[0] === "msgstr " && v[1] !== "" ) {
      console.log(v[1]);
      verse[verse_count++] = v[1];
    }
    if (v[0] === "msgid " && v[1] !== "" ){
      pali[pali_count++] = v[1];
    }
  }
  console.log(verse);
  //console.log(pali);
}

function setup() {
  //createCanvas(2500, 1875);
  // sutta_po = await loadStrings('./suttas/sc-data-master/po_text/pli-en/mn/mn002.po');
  createCanvas(1250,938);
  background(bg_img_1);
  //load default sutta
  parse(sutta_po);
  console.log(verse);

  speech = new p5.Speech(); // speech synthesis object
  speech.onLoad = voiceReady;

  speech.interrupt = true;
  speech.started(startSpeaking);
  speech.ended(endSpeaking);

  function voiceReady() {
    voice =  speech.voices[voiceId];
    console.log('voice ready');
    console.log(speech.voices);
  }
}

function startSpeaking() {
  background(bg_img_1);
  drawText ();
}

function endSpeaking() {
  
}

function keyPressed() {
  console.log(key);
  if (key == " ") {
    speak_now();
  }
  if (key == "b") {
    bhasati();
  }
  if (key == "z") {
    loadNewSutta().
      then(result => {
        
        let a_new_sutta = result.got_sutta;
        console.log(a_new_sutta.length);
        for (let i = 0; i < a_new_sutta.length; i++){
          console.log(a_new_sutta[i]);
        }
        // createP (a_new_sutta);
        // console.log(a_new_sutta[31]);
        //parse(result.got_sutta);
      }).
      catch(err => console.error(err));
  }
}

async function loadNewSutta() {
  let new_sutta = await loadStrings('./suttas/sc-data-master/po_text/pli-en/mn/mn131.po');
  return {
    got_sutta: new_sutta
  }
}

function bhasati () {
  // google voices have no Pali voice yet
  // speech.setRate(1);
  // speech.setPitch(1);
  // speech.setVoice(voice.name);
  // speech.speak(pali[pali_counter]); 
  sentence = pali[pali_counter];
  // createP(verse[counter]);
  pali_counter+=1;
  if (pali_counter == pali.length) {
    pali_counter = 0;
  }
}

function speak_now () {
  speech.setRate(1);
  speech.setPitch(1);
  speech.setVoice(voice.name);
  speech.speak(verse[counter]); 
  sentence = verse[counter];
  // createP(verse[counter]);
  counter+=1;
  pali_counter = counter;
  if (counter == verse.length) {
     counter = 0;
  }
}

function mousePressed() {
  // speak_now();
}

function drawText () {
  let fontsize = 16;
  //sentence += ' ';
  let textlength = textWidth(sentence + ' ');
  if (counter === 1){
    textlength *= 2;
  }
  console.log(textlength)
  if (textlength > width) {
    drawText_extra();
  } else {
    textFont("Helvetica", fontsize);
    noStroke();
    fill(255);
    rect(0, height - (height*0.618), textlength*1.06, fontsize*2);
    fill(0);
    text(sentence, 10, height - (height*0.618) + fontsize + 6);
  }
}

function drawText_extra () {
  let fontsize = 16;
  //sentence += ' ';
  
  let splitString = split(sentence, '.');
  console.log(splitString);
  for (let i = 0 ; i < splitString.length; i++) {
    if (splitString[i] === " ") {
      continue;
    }
    let textlength = textWidth(splitString[i] + ' ');
  // console.log(textlength);
    textFont("Helvetica", fontsize);
    noStroke();
    fill(255);
    rect(0, (height+i*fontsize*2) - (height*0.618), textlength*1.06, fontsize*2);
    fill(0);
    text(splitString[i], 10, (height+i*fontsize*2) - (height*0.618) + fontsize + 6);
  }
  
}

// function draw () {
//   drawText ();
// }
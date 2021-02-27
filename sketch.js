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
let a_new_sutta;
let new_sutta_loaded = false;
let input;
let button;

function preload() { 
  sutta_po = loadStrings('./suttas/sc-data-master/po_text/pli-en/mn/mn001.po');
  bg_img_1 = loadImage('./img/jetavana.jpg');
}

function parse(sutta) {
  verse = [];
  pali = [];
  verse_count = 0;
  pali_count = 0;
  for (let i = 0; i < sutta.length; i++){
    v = sutta[i].split('"');
    if (v[0] === "msgstr " && v[1] !== "" ) {
      verse[verse_count++] = v[1];
    }
    if (v[0] === "msgid " && v[1] !== "" ){
      pali[pali_count++] = v[1];
    }
  }
  counter = 0;
  pali_counter = 0;
  //console.log(verse);
  //console.log(pali);
}

function ask_for_Sutta() {
  input = createInput("mn001");
  input.position(20, 65);
  
  button = createButton('submit');
  button.position(input.x + input.width, 65);
  button.mousePressed(loadSutta);
}

function setup() {
  createCanvas(1250,938);
  background(bg_img_1);
  // create ui for sutta query
  ask_for_Sutta();
  // load mn 1 by default
  parse(sutta_po);

  speech = new p5.Speech(); 
  speech.onLoad = voiceReady;
  speech.interrupt = true;
  speech.started(startSpeaking);
  speech.ended(endSpeaking);

  function voiceReady() {
    voice =  speech.voices[voiceId];
    console.log('voice ready');
  }
}

function loadSutta() {
  loadNewSutta().
      then(result => {
        a_new_sutta = result.got_sutta;
        console.log(a_new_sutta);
      }).
      catch(err => console.error(err));
  new_sutta_loaded = true;
}


function startSpeaking() {
  background(bg_img_1);
  drawText ();
}

function endSpeaking() {
  speech.cancel();
}

function keyPressed() {
  console.log(key);
  if (key == " ") {
    if (new_sutta_loaded) {
      // the parsing has to be decoupled from the loading
      parse(a_new_sutta);
      new_sutta_loaded = false;
    }
    speak_now();
  }
  // if (key == "b") {
  //   bhasati();
  // }
  // if (key == "z") {
  //   speech.cancel();
  //   loadSutta();
  // }
}

async function loadNewSutta() {
  let sutta_number = input.value();
  let new_sutta_path = sutta_string + sutta_number + '.po';
  // let new_sutta = await loadStrings('./suttas/sc-data-master/po_text/pli-en/mn/mn131.po');
  let new_sutta = await loadStrings(new_sutta_path);
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
  counter+=1;
  pali_counter = counter;
  if (counter == verse.length) {
     counter = 0;
  }
}

function drawText () {
  let fontsize = 16;
  let textlength = textWidth(sentence + ' ');
  if (counter === 1){
    textlength *= 2;
  }
  // console.log(textlength)
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
  let splitString = split(sentence, '.');
  if (splitString.length === 2) {
    splitString = [];
    splitString = split(sentence, ',');
  }

  console.log(splitString);
  for (let i = 0 ; i < splitString.length; i++) {
    if (splitString[i] === " ") {
      continue;
    }
    let textlength = textWidth(splitString[i] + ' ');
    textFont("Helvetica", fontsize);
    noStroke();
    fill(255);
    rect(0, (height+i*fontsize*2) - (height*0.618), textlength*1.06, fontsize*2);
    fill(0);
    text(splitString[i], 10, (height+i*fontsize*2) - (height*0.618) + fontsize + 6);
  }
  
}

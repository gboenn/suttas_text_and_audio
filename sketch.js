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

// let sutta_po;
let bg_img_1;
let sentence;
let sutta_string = './bilara-data-published/translation/en/sujato/sutta/';
let a_new_sutta;
let new_sutta_loaded = false;
let input;
let button;

function preload() { 
  ask_for_Sutta();
  loadSutta();
  bg_img_1 = loadImage('./img/jetavana.jpg');
}

function parse(sutta) {
  verse = [];
  pali = [];
  let verse_count = 0;
  let pali_count = 0;

  for (line in sutta) {
    verse[verse_count++] = sutta[line];
  }  

  counter = 0;
  pali_counter = 0;
  //console.log(verse);
  //console.log(pali);
}

function ask_for_Sutta() {
  input = createInput("mn1");
  input.position(20, 65);
  
  button = createButton('submit');
  button.position(input.x + input.width, 65);
  button.mousePressed(loadSutta);
}

function setup() {
  createCanvas(1250,938);
  background(bg_img_1);

  speech = new p5.Speech(); 
  speech.onLoad = voiceReady;
  // one can forward verses only with interrupt = true;
  // otherwise speak calls are queued
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
  //speech.cancel();
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
}

async function loadNewSutta() {
  let sutta_number = input.value();
  let pitaka = resolve_pitaka (sutta_number); // resolve pitika folder "mn/";
  // let new_sutta_path = sutta_string + pitaka + sutta_number + '_translation-en-sujato.json';
  let new_sutta_path = sutta_string + pitaka + '_translation-en-sujato.json';
  let response = await fetch(new_sutta_path);
  let new_sutta = await response.json();
  return {
    got_sutta: new_sutta
  }
}

function resolve_pitaka (sutta_number) {
  let folder = "";
  let result = sutta_number.match('^mn');
  if (result && result.index === 0) { 
    folder = "mn/" + sutta_number;
    return folder;
  }
  result = sutta_number.match('^dn');
  if (result && result.index === 0) { 
    folder = "dn/" + sutta_number;
    return folder;
  }

  result = sutta_number.match('^an');
  if (result && result.index === 0) { 
    folder = "an/";
    // then resolve subfolders
    // an1 an2 an3 ... an11
    let m_exp = new RegExp(/^an(\d+)\.(\d+)-?(\d+)?/); 
    num = sutta_number.match(m_exp);
    console.log(num);
    if (num) { 
      sub_num = num[1];
      if (sub_num < 1 || sub_num > 11) {
        console.error("Sutta not found");
      } else {
        folder += "an" + sub_num + "/" + sutta_number;;
      }
      console.log(folder);
      return folder;
    }
  }

  // kn suttas are named after the tags and the path where they are stored must be resolved
  //  kn/
  //   // dhp/ iti/ kp/ thag/ thig/ ud/
  //   // iti -> vagga1 vagga2 ... vagga11
  //   // ud -> vagga1 vagga2 ... vagga8
  result = sutta_number.match('^dhp');  
  if (result && result.index === 0) { 
    folder = "kn/dhp/";
    let m_exp = new RegExp(/^dhp(\d+)/); 
    num = sutta_number.match(m_exp);
    console.log(num);
    if (num) { 
      sub = num[1];
      if (sub < 1 || sub > 423) {
        console.error("Sutta not found");
      } else {
        if (sub >= 1 && sub <= 20) {
          sutta_number = "dhp1-20"
        }
        if (sub >= 21 && sub <= 32) {
          sutta_number = "dhp21-32"
        }
        if (sub >= 33 && sub <= 43) {
          sutta_number = "dhp33-43"
        }
        if (sub >= 44 && sub <= 59) {
          sutta_number = "dhp44-59"
        }
        if (sub >= 60 && sub <= 75) {
          sutta_number = "dhp60-75"
        }
        if (sub >= 76 && sub <= 89) {
          sutta_number = "dhp76-89"
        }
        if (sub >= 90 && sub <= 99) {
          sutta_number = "dhp90-99"
        }
        if (sub >= 100 && sub <= 115) {
          sutta_number = "dhp100-115"
        }
        if (sub >= 116 && sub <= 128) {
          sutta_number = "dhp116-128"
        }
        if (sub >= 129 && sub <= 145) {
          sutta_number = "dhp129-145"
        }

        folder += sutta_number;
        console.log(folder);
        return folder;
      }
      
    }
  }
  result = sutta_number.match('^kp');  
  if (result && result.index === 0) { 
    folder = "kn/kp/";
    return folder;
  }
  result = sutta_number.match('^thag');  
  if (result && result.index === 0) { 
    folder = "kn/thag/";
    return folder;
  }
  result = sutta_number.match('^thig');  
  if (result && result.index === 0) { 
    folder = "kn/thig/";
    return folder;
  }

  result = sutta_number.match('^sn');
  if (result && result.index === 0) { 
    folder = "sn/";
    // then resolve subfolders
    // sn1 sn2 sn3 ... sn56
    let m_exp = new RegExp(/^sn(\d+)\.(\d+)-?(\d+)?/); 
    num = sutta_number.match(m_exp);
    console.log(num);
    if (num) { 
      sub_num = num[1];
      if (sub_num < 1 || sub_num > 56) {
        console.error("Sutta not found");
      } else {
        folder += "sn" + sub_num + "/" + sutta_number;
      }
      console.log(folder);
      return folder;
    }
  }
  return folder;
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
  sentence = verse[counter];
  // need to split up verses that are long lists > 299 charachters
  console.log("length: " + sentence.length);
  if (sentence.length > 299) {
    let utterance = sentence.split(',');
    verse.splice(counter, 1, utterance[0]); 
    for (let i = 1; i < utterance.length; i++){
      verse.splice(counter+i, 0, utterance[i]); 
    }
  } 
  sentence = verse[counter];
  speech.setRate(1);
  speech.setPitch(1);
  speech.setVoice(voice.name);
  speech.speak(sentence);
  
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

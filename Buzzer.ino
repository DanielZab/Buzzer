#include <Tone.h> //Einbinden der tone library

//Initialiesierung beider Buzzer
Tone tone1;
Tone tone2;

//Strings, welche die Frequenzen bzw. Tondauern enthalten werden erstellt
String frequencies = ""; //Frequenzen es ersten Buzzers
String secondFrequencies = ""; //Frequenzen des zweiten Buzzers
String durations = ""; //Tonlängen des ersten Buzzers
String secondDurations = ""; //Tonlängen des zweiten Buzzers

bool Play = false; //Bool, der den Code zurückhält, bis alle nötigen Daten übertragen wurden, wird erstellt

float tempo = 120; //Tempo des Liedes der Vierteln, dh. hier werden 120 Vierteln pro Minute gespielt
float tempoMult; //Multiplikator mit dem die Notenlängen multipliziert werden, damit sie an das Tempo angepasst werden.

void setup() {
  

  Serial.begin(9600);
  tone1.begin(5); //Der Pin 5 wird als Buzzer definiert
  tone2.begin(7); //Der Pin 7 wird als Buzzer definiert
  Serial.setTimeout(50); //Stellt die Zeit ein, die das Programm wartet, wenn ein Input gelesen werden soll
  
  tempoMult = 60 / tempo * 1000; // Tempomultiplikator wird berechnet
}

bool pausing = false; //Wenn true hat der erste Buzzer eine Pause
bool pausing2 = false;//Wenn true hat der zweite Buzzer eine Pause
long millisToPause; //Speichert den Zeitpunkt des Beginns einer Pause des ersten Buzzers
long millisToPause2;//Speichert den Zeitpunkt des Beginns einer Pause des zweiten Buzzers
int firstToneToPlay = 0; //Zählt, welcher Ton beim ersten Buzzer gespielt werden soll
int secondToneToPlay = 0; //Zählt, welcher Ton beim zweiten Buzzer gespielt werden soll


void loop() {
  //Teste ob etwas in den seriellen Monitor geschickt wurde und wenn ja, starte die Funktion getInput
  if(Serial.available() > 0){
    getInput();
  }
  
  //Pausiere den Code, bis alle Daten empfangen wurden
  if(!Play){return;}
  
  //Teste ob der Buzzer eine Pause hat und wenn ja, ob diese bereits vorüber ist
  //Dies geschieht indem die Millisekunden zu Beginn der Pause von den jetzigen Millisekunden der Laufzeit des Programms subtrahiert werden. Ist dieser Wert größer als die Pausenlänge, hört die Pause auf
  //Die Funktion split, die später im Code definiert ist, gibt einen bestimmten Teil eines Strings aus. Dies ist nötig, da der Input im seriellen Monitor ein langer String mit verschiedenen Notenlängen oder Notenhöhen ist, welche jeweils durch ein Komma voneinander getrennt werden.
  //Der String ist somit eine Art Array und die Funktion split gibt den gewünschten Wert von einem bestimmten Index aus.
  if (pausing && millis() - millisToPause >= split(durations,',',firstToneToPlay - 1).toFloat()*tempoMult) {
    pausing = false;
  }

  //Teste ob der erste Buzzer nicht (mehr) spielt und keine Pause macht. Falls ja, teile ihm eine neue Note zu
  if (!tone1.isPlaying() && !pausing) {
    //Teste ob die nächste Note ein  
    if (split(frequencies,',',firstToneToPlay).toInt() == 0) {
      millisToPause = millis();
      firstToneToPlay++;
      pausing = true;
      goto tone2;
    }
    tone1.play(split(frequencies,',',firstToneToPlay).toInt(), split(durations,',',firstToneToPlay).toFloat()*tempoMult);
    firstToneToPlay++;
  }
  
tone2:

  if (pausing2 && millis() - millisToPause2 >= split(secondDurations,',',secondToneToPlay - 1).toFloat()*tempoMult) {
    pausing2 = false;
  }
  
  if (!tone2.isPlaying() && !pausing2) {
    if (split(secondFrequencies,',',secondToneToPlay).toInt() == 0) {
      millisToPause2 = millis();
      secondToneToPlay++;
      pausing2 = true;
      goto End;
    }
    
    tone2.play(split(secondFrequencies,',',secondToneToPlay).toInt(), split(durations,',',secondToneToPlay).toFloat()*tempoMult);
    secondToneToPlay++;

  }
  
End:
  if(countCommas(frequencies)+1 <= firstToneToPlay && !tone1.isPlaying()){
      tone1.stop();
      tone2.stop();
      Play = false;
      firstToneToPlay = 0;
      secondToneToPlay = 0;
      Serial.println("Ready");
    }
  

}

int countCommas(String text){
  int index=0;
  int from = 0;
  int to = -1;
  while (true){
    from = to + 1;
    to = text.indexOf(",", from);
    if(to == -1){break;}
    index++;
  }
  return index;
}

String split(String text, char splitter, int index){
  int splitterCount = 0;
  int from = 0;
  int to = -1;
  while(index >= splitterCount){
    from = to + 1;
    to = text.indexOf(splitter, from);
    if(to == -1 && splitterCount == 0){
      return text;  
    }
    if(index == splitterCount){
      if(to == -1){return text.substring(from);}
      return text.substring(from,to);
    }
    else splitterCount++;
  }
  return ""; 
}



int whichInput = 0;
void getInput(){
  switch(whichInput){
    case 0:
      frequencies = Serial.readString();
      break;
    case 1:
      secondFrequencies = Serial.readString();
      break;
    case 2:
      durations = Serial.readString();
      break;
    case 3: 
      secondDurations = Serial.readString();

      whichInput=-1;
      Play = true;
      break;
  }
  whichInput += 1;
  Serial.println("Ready");
}

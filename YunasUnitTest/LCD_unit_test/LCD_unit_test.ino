#include <LiquidCrystal.h>

const int rs = 2, en = 3, d4 = 4, d5 = 5, d6 = 6, d7 = 7;
LiquidCrystal lcd(rs, en, d4, d5, d6, d7);

char char_array[666];
int ind1;
int ind2;
String text;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  //Serial.println("Serial Comms is ready to receive");
  Serial.setTimeout(1);
  lcd.begin(16, 2);
  lcd.clear();
}

void loop() {
  if (Serial.available() > 0) {
    String data = Serial.readStringUntil('\n');
    ind1 = data.indexOf('(');
    ind2 = data.indexOf(')');
    text = data.substring(ind1+1, ind2);
    Serial.print("You sent me confirmed: ");
    Serial.println(text);
    //updateDisplay(text)
  }
  // put your main code here, to run repeatedly:
  //displayLCD();
}

void displayLCD(){
   String song = "";
   String artist = "";
   String strArr[16];
   String receivedCharToString = "";
   if (Serial.available()) {
          while (Serial.available()) {
              delay(2);
              char receivedChar = Serial.read();
              receivedCharToString += receivedChar;
          }
   }
   
   int stringStart = 0;
   int arrayIndex = 0;
   
   for (int i = 0; i  < receivedCharToString.length(); i++) {
         if (receivedCharToString.charAt(i) == ',') {
            strArr[arrayIndex] = "";
            strArr[arrayIndex] = receivedCharToString.substring(stringStart, i);
            stringStart = (i + 1);
            arrayIndex++;
          }
          song = strArr[0];
          artist = strArr[1];
          lcd.setCursor(0, 0); 
          lcd.print(song);
          lcd.setCursor(0, 1);
          lcd.print(artist);
          //Serial.print(receivedCharToString);
                   
   }
   Serial.print(receivedCharToString);
   //Serial.println(song);
   ///Serial.println(artist); 
   //Serial.println("in display");
 }

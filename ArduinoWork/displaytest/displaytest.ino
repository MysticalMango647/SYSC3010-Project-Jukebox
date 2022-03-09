#include <LiquidCrystal.h>
// initialize the library by associating any needed LCD interface pin
// with the arduino pin number it is connected to
const int rs = 42, en = 38, d4 = 28, d5 = 26, d6 = 24, d7 = 22;
LiquidCrystal lcd(rs, en, d4, d5, d6, d7);
char char_array[666];
void setup() {
  Serial.begin(9600);
  lcd.begin(16, 2);
  char Str6[15] = "Demo Test";
  lcd.print(Str6);
}

void loop() {

updateDisplay();
  
}

void updateDisplay() {
  
    if (Serial.available() ) {
        String toDisplay = Serial.readStringUntil('\n');
        //int strLen= toDisplay.length() + 1;
        //char char_array[strLen];
        Serial.print(toDisplay);
        lcd.clear();
        //toDisplay.toCharArray(char_array,strLen);
        while (Serial.available() > 0){
        lcd.setCursor(0, 1);
        lcd.write(Serial.read());
        }
    }  

}

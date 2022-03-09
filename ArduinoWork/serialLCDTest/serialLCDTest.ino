#include <LiquidCrystal.h>
const int rs = 42, en = 38, d4 = 28, d5 = 26, d6 = 24, d7 = 22;
LiquidCrystal lcd(rs, en, d4, d5, d6, d7);
char char_array[666];
int ind1;
int ind2;
String text;
void setup() {
  Serial.begin(9600);
  lcd.begin(16, 2);
}
void loop() {
  if (Serial.available() > 0) {
    String data = Serial.readStringUntil('\n');
    ind1 = data.indexOf('(');
    ind2 = data.indexOf(')');
    text = data.substring(ind1+1, ind2);
    Serial.print("You sent me confirmed: ");
    Serial.println(text);
    updateDisplay(text)
  }
}

void updateDisplay(String toDisplay) {

        int strLen= toDisplay.length() + 1;
        char char_array[strLen];
        lcd.clear();
        toDisplay.toCharArray(char_array,strLen);
        lcd.setCursor(0, 1);
        lcd.write(toDisplay);
} 

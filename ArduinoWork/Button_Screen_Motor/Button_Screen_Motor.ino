
#include <LiquidCrystal.h>

const int rs = 2, en = 3, d4 = 4, d5 = 5, d6 = 6, d7 = 7;
LiquidCrystal lcd(rs, en, d4, d5, d6, d7);

String text;
String songString = "";
String artistString = "";

String song = "";
String artist = "";
String strArr[16];


//Motor Push Button Components Pin Declaration
const int m1 = 9, m2 = 10, m3 = 11, m4 = 12;
const int button = A0;
int step_number = 0;
int buttonState;
int lastPress = LOW;
int ledState = HIGH;
unsigned long lastDebounceTime = 0;
unsigned long debounceDelay = 100;
bool spinOfMotorDirection = false; //false for counter clockwise, true for clockwise
const int MotorSpinTime = 1000;
unsigned long previousMillis = 0;
unsigned long activeMotorTime = 0;
bool wasButtonPressed = false;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  //Serial.println("Serial Comms is ready to receive");
  //setting up screening and input output for the motors
  Serial.setTimeout(1);
  lcd.begin(16, 2);
  lcd.clear();

  pinMode(m1, OUTPUT);
  pinMode(m2, OUTPUT);
  pinMode(m3, OUTPUT);
  pinMode(m4, OUTPUT);
  pinMode(button, INPUT);
}

void loop() {
  //constantly updating display if it detects the lcd
  displayLCD();
  //checking for button press constantly
  bool wasPressed = listenForButton();
  //if button was pressed we rotoate our motors for a set abmount of time
  if (wasPressed) {
    if ((millis() - activeMotorTime) < MotorSpinTime) {
      actuateMotor(spinOfMotorDirection);
      delay(2);
    }
    //if the motor acttive threshold time is up, we stop rotating the motors
    if (millis() - activeMotorTime >= MotorSpinTime) {
      stopMotor();
    }
  }
}

//displayLcd function will read a serial input and update the display accordingly 
void displayLCD() {
  String song = "";
  String artist = "";
  String strArr[16];
  String receivedCharToString = "";
  //received the input and storeed in a char that will later be converted to a string
  if (Serial.available()) {
    while (Serial.available()) {
      delay(2);
      char receivedChar = Serial.read();
      receivedCharToString += receivedChar;
    }
  }

  int stringStart = 0;
  int arrayIndex = 0;
  //Parsing the string by "," to seperate between song name and artist name
  //this method was derived from a online tutorial that is linked at the bottom
  for (int i = 0; i  < receivedCharToString.length(); i++) {
    if (receivedCharToString.charAt(i) == ',') {
      strArr[arrayIndex] = "";
      strArr[arrayIndex] = receivedCharToString.substring(stringStart, i);
      stringStart = (i + 1);
      arrayIndex++;
    }
    song = strArr[0];
    artist = strArr[1];
    //updating the string accordlingly to the display
    lcd.clear();
    lcd.setCursor(0, 0);
    lcd.print(song);
    lcd.setCursor(0, 1);
    lcd.print(artist);
    //Serial.print(receivedCharToString);


  }
  Serial.print(receivedCharToString);
  //Serial.println(song);
  //Serial.println(artist);
  //Serial.println("in display");
}

//listen for button press we use a debouncing that originated with one of the arduino example code
boolean listenForButton() {
  int listening = digitalRead(button);
  if (listening != lastPress) {
    lastDebounceTime = millis();
  }
  if ((millis() - lastDebounceTime) > debounceDelay) {
    if (listening != buttonState) {
      buttonState = listening;
      if (buttonState == HIGH) {
        spinOfMotorDirection = !spinOfMotorDirection;
        //we store the currentt time for the motor to know how long to spin for
        activeMotorTime = millis();
        wasButtonPressed = true;

      }
    }
  }
  //else{
  ///wasButtonPressed = false;
  //}
  lastPress = listening;
  //Serial.println(ledState);
  return (wasButtonPressed);
}

//stopMotor will stop the motor operations after it reachs the spin time threshold
void stopMotor() {
  digitalWrite(m1, LOW);
  digitalWrite(m2, LOW);
  digitalWrite(m3, LOW);
  digitalWrite(m4, LOW);
}

//actuate motor will spin the stepper motor and requires an input for the direction
// direction input is boolean and rotates clockwise for true and counterclockwise for false
//this method was derived from a youtube video that is linked at the bottom of the code
//the arduino stepper motor library is not compatible with the BYJ stepper motor
void actuateMotor(bool rotateDirection) {
  //Serial.println("moving motor");
  //clockwise roation
  if (rotateDirection) {
    switch (step_number) {
      case 0:
        digitalWrite(m1, HIGH);
        digitalWrite(m2, LOW);
        digitalWrite(m3, LOW);
        digitalWrite(m4, LOW);
        break;
      case 1:
        digitalWrite(m1, LOW);
        digitalWrite(m2, HIGH);
        digitalWrite(m3, LOW);
        digitalWrite(m4, LOW);
        break;
      case 2:
        digitalWrite(m1, LOW);
        digitalWrite(m2, LOW);
        digitalWrite(m3, HIGH);
        digitalWrite(m4, LOW);
        break;
      case 3:
        digitalWrite(m1, LOW);
        digitalWrite(m2, LOW);
        digitalWrite(m3, LOW);
        digitalWrite(m4, HIGH);
        break;
    }
  }
  //counterclockwise rotation 
  else {
    switch (step_number) {
      case 0:
        digitalWrite(m1, LOW);
        digitalWrite(m2, LOW);
        digitalWrite(m3, LOW);
        digitalWrite(m4, HIGH);
        break;
      case 1:
        digitalWrite(m1, LOW);
        digitalWrite(m2, LOW);
        digitalWrite(m3, HIGH);
        digitalWrite(m4, LOW);
        break;
      case 2:
        digitalWrite(m1, LOW);
        digitalWrite(m2, HIGH);
        digitalWrite(m3, LOW);
        digitalWrite(m4, LOW);
        break;
      case 3:
        digitalWrite(m1, HIGH);
        digitalWrite(m2, LOW);
        digitalWrite(m3, LOW);
        digitalWrite(m4, LOW);
    }
  }
  //we have 4 poles for the stepper motor, so we use a step counter
  //once we reached step3 (4 total steps starts at step 0) we reset the step to 1
  step_number++;
  if (step_number > 3) {
    step_number = 0;
  }
}



//sources used in project
//debouncing with push button:
//https://www.arduino.cc/en/Tutorial/BuiltInExamples/Debounce
//serial communication
//https://eecs.blog/sending-multiple-values-over-serial-to-arduino/
//rgb lighting
//https://github.com/adafruit/Adafruit_NeoPixel
//microphone test
//https://learn.sparkfun.com/tutorials/sound-detector-hookup-guide/software-example
//stepper motor
//https://www.youtube.com/watch?v=avrdDZD7qEQ&t=190s

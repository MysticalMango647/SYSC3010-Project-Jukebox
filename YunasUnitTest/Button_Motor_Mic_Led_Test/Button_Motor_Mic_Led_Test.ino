//Motor Push Button Components Pin Declaration
const int m1 = 3, m2 = 4, m3 = 5, m4 = 6; 
const int button = 2;
int step_number = 0;
int buttonState;
int lastPress = LOW;
int ledState = HIGH;
unsigned long lastDebounceTime = 0;
unsigned long debounceDelay = 100;
bool spinOfMotorDirection = false; //false for counter clockwise, true for clockwise
const int MotorSpinTime = 5000;
unsigned long previousMillis = 0; 
unsigned long activeMotorTime = 0;
bool wasButtonPressed = false;

//microphone declaration
#define PIN_GATE_IN 8
#define IRQ_GATE_IN  0
#define PIN_LED_OUT 13
#define PIN_ANALOG_IN A0
unsigned long  micActiveTime = 0;
int micValueThreshold = 1000;
int lastValue = 0;


// rgb lights
#include <Adafruit_NeoPixel.h>
#ifdef __AVR__
 #include <avr/power.h> // Required for 16 MHz Adafruit Trinket
#endif

#define PIN        7
#define NUMPIXELS 150
Adafruit_NeoPixel pixels(NUMPIXELS, PIN, NEO_GRB + NEO_KHZ800);
int DELAYVAL = 25;

//demo test iteration
bool buttonDemo = false;

//Code for sound detector used later to interupt
void soundISR()
{
  int pin_val;
  pin_val = digitalRead(PIN_GATE_IN);
  digitalWrite(PIN_LED_OUT, pin_val);   
}


void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  pinMode(m1, OUTPUT);
   pinMode(m2, OUTPUT);
   pinMode(m3, OUTPUT);
   pinMode(m4, OUTPUT);
   pinMode(button, INPUT);

     //  Configure LED pin as output
  pinMode(PIN_LED_OUT, OUTPUT);

  // configure input to interrupt
  pinMode(PIN_GATE_IN, INPUT);
  attachInterrupt(IRQ_GATE_IN, soundISR, CHANGE);

  //configure led
  #if defined(__AVR_ATtiny85__) && (F_CPU == 16000000)
    clock_prescale_set(clock_div_1);
  #endif
  pixels.begin();
  
  //Demo Test iteration
 
  Serial.println("Starting Demo Test, Please check each component is work visually");
  Serial.println("Testing Red Leds on RGB Strip");
  testRed();
  delay(1500);
  Serial.println("Testing Blue Leds on RGB Strip");
  testBlue();
  delay(1500);
  Serial.println("Testing Green Leds on RGB Strip");
  testGreen();
  delay(1500);
  Serial.println("Turning of all Leds on RGB Strip");
  testClear();
  delay(1500);

  Serial.println("Testing Push Button to see detection");
  Serial.println("Please press button");
  bool wasPressed = false;
  while (wasPressed != true){
      buttonDemo = listenForButton();
      if(buttonDemo == true){
        Serial.println("Button Detected");
        break;
       }
  }
  delay(1500);

  Serial.println("Testing Motor to move clockwise");
  for (int i = 0; i< 1000; i++){
  actuateMotor(true);
  delay(2);
  }
  delay(1000);
  stopMotor();
  
  Serial.println("Testing Motor to move clockwise");
  for (int j = 0; j< 1000; j++){
  actuateMotor(false);
  delay(2);
  }
  delay(1000);
  stopMotor();

  Serial.println("Testing Microphone for input(range 30-400)");
  int DemoTestMic = microphoneDetection();
  Serial.println("Microphone reading shows: ");
  Serial.print(DemoTestMic);
  }
  

void testClear(){
  pixels.clear();
  for(int i=0; i<NUMPIXELS; i++) { 
    pixels.setPixelColor(i, pixels.Color(0, 0, 0));
    pixels.show();
  }}

void testBlue(){
  pixels.clear();
  for(int i=0; i<NUMPIXELS; i++) { 
    pixels.setPixelColor(i, pixels.Color(0, 0, 150));
    pixels.show(); 
  } 
}
void testRed(){
  pixels.clear();
  for(int i=0; i<NUMPIXELS; i++) { 
    pixels.setPixelColor(i, pixels.Color(150, 0, 0));
    pixels.show();
  }
  
}

void testGreen(){
  pixels.clear();
  for(int i=0; i<NUMPIXELS; i++) { 
    pixels.setPixelColor(i, pixels.Color(0, 150, 0));
    pixels.show();
  }
  
}


void loop() {
  // put your main code here, to run repeatedly:
  bool wasPressed = listenForButton();

  if(wasPressed){
    if ((millis() - activeMotorTime) < MotorSpinTime){
      actuateMotor(spinOfMotorDirection);
      delay(2);
      }
    if (millis() - activeMotorTime >= MotorSpinTime){
      stopMotor();
    }
  }

  
  //if (millis()- micActiveTime > micActiveTime){
    int micCheck = microphoneDetection();
   //Serial.println(micCheck);
    //}
    DELAYVAL = micCheck;
    ///lightUpLed(DELAYVAL);
}

int microphoneDetection(){
  int value;
  value = analogRead(PIN_ANALOG_IN);
  if (lastValue != value){
    micActiveTime=millis();
  }
  lastValue = value;
  //Serial.println(value);
  return (value); 
}

void lightUpLed(int lightDelay){
  pixels.clear();
  for(int i=0; i<NUMPIXELS; i++) { 
    if (i%2 == 0){
    pixels.setPixelColor(i, pixels.Color(0, 0, 150));}
    if(i%2 == 1){
    pixels.setPixelColor(i, pixels.Color(150, 0, 0));}
    pixels.show(); 
  }
  delay(lightDelay);
  pixels.clear();
  for(int i=150; i>0; i--) {
    if (i%2 == 0){
    pixels.setPixelColor(i, pixels.Color(150, 0, 0));}
    if(i%2 == 1){
    pixels.setPixelColor(i, pixels.Color(0, 0, 150));}
    pixels.show(); 
  }
}

boolean listenForButton(){
  int listening = digitalRead(button);
  if (listening != lastPress){
    lastDebounceTime = millis();   
  }
  if ((millis() - lastDebounceTime) > debounceDelay) {
      if (listening != buttonState){
        buttonState = listening;
        if (buttonState == HIGH){
          spinOfMotorDirection = !spinOfMotorDirection;
          activeMotorTime = millis(); 
          wasButtonPressed = true;
          buttonDemo = true;
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


void stopMotor(){
  digitalWrite(m1, LOW);
  digitalWrite(m2, LOW);
  digitalWrite(m3, LOW);
  digitalWrite(m4, LOW);
  }

void actuateMotor(bool rotateDirection){
  //Serial.println("moving motor");
    if(rotateDirection){
switch(step_number){
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
  }else{
    switch(step_number){
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
step_number++;
  if(step_number > 3){
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

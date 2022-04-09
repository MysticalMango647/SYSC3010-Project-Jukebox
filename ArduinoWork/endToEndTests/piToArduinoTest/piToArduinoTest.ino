//This script runs on the arduino connected the the LCD screen, and tests communication between the Jukebox Pi and the Arduino
//Written by: Corbin Garlough
void setup() {
  Serial.begin(9600);
}

void loop() {
  // read messages from the Pi and reply with what was recieved
  if (Serial.available() > 0) {
    String data = Serial.readStringUntil('\n');
    Serial.print("The Arduino recieved: ");
    Serial.println(data);
  }
}

#include <Wire.h>
#include <SDPArduino.h>

void setup(){
  SDPsetup();
  helloWorld();
}

void runAllMotors(){
  Serial.println("Running all motors");
  motorForward(0, 50);
  motorForward(1, 50);
  motorForward(2, 50);
  motorForward(3, 50);
  delay(2500);
  motorAllStop();
}

void testKicker(int x){
  Serial.println("Kick");
  motorForward(3, x);
  delay(1000);
  Serial.println("Reset");
  motorBackward(3, x);
  delay(1000);
}


//backward is forwards
//right motor goes faster than left motor
void goFw(){
  motorBackward(0, 94);
  motorBackward(1, 80);
  delay(2500);
}

void loop(){
  //runAllMotors();
  //testKicker(100);
  goFw();
}

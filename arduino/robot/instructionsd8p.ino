#include <SoftwareSerial.h>
#include <Wire.h>
#include <stdlib.h>
#include <math.h>
#include <SDPArduino.h>

#include "hardware.h"

void setup() {
  hardwareSetup();
  Serial.println(F("READY")) ;
}

void checkMotors() {
  Serial.println("Testing Left Motor");
  greenMotorMove(ROT_LH_MOTOR_IDX, 100, MOTOR_FWD);
  delay(2000);
  greenMotorMove(ROT_LH_MOTOR_IDX, 100, MOTOR_BWD);
  delay(2000);
  Serial.println("Stopping Left Motor");
  greenMotorMove(ROT_LH_MOTOR_IDX, 100, MOTOR_BRAKE);
  
  Serial.println("Testing Right Motor");
  greenMotorMove(ROT_RH_MOTOR_IDX, 100, MOTOR_FWD);
  delay(2000);
  greenMotorMove(ROT_RH_MOTOR_IDX, 100, MOTOR_BWD);
  delay(2000);
  Serial.println("Stopping Right Motor");
  greenMotorMove(ROT_RH_MOTOR_IDX, 100, MOTOR_BRAKE);
}

void loop() {
  //checkMotors();
  Serial.println("Kick");
  greenMotorMove(ROT_FINGER_IDX , 100, MOTOR_FWD);
  delay(2000);
  greenMotorMove(ROT_FINGER_IDX , 100, MOTOR_BWD);
  delay(2000);
  Serial.println("Unkick");
  greenMotorMove(ROT_FINGER_IDX , 100, MOTOR_BRAKE);
  
}

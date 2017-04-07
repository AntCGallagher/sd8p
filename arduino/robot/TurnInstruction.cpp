#include "TurnInstruction.h"
#include "global.h"
#include "compass.h"
#include "SDPArduino.h"

//#define DEBUG_PRINT_TURN

void TurnInstruction::initFromCommand(Command cmd) {
  TurnInstruction *turn = new TurnInstruction();
  turn->deg = byteArrToSignedInt(cmd.params, 0);
#ifdef DEBUG_PRINT_TURN
  Serial.print(F("Turn "));
  Serial.println(turn->deg);
#endif
  appendInstruction(turn);
}

void TurnInstruction::halt(void) {
  greenMotorMove(LH_IDX, 0, MOTOR_FLOAT);
  greenMotorMove(RH_IDX, 0, MOTOR_FLOAT);
  greenMotorMove(REAR_IDX, 0, MOTOR_FLOAT);
  greenMotorMove(GRABBER_IDX, 0, MOTOR_FLOAT);
}

float mode(int a[], int size) {
  for(int i=0; i<(size-1); i++) {
    for(int o=0; o<(size-(i+1)); o++) {
      if(a[o] > a[o+1]) {
        int t = a[o];
        a[o] = a[o+1];
        a[o+1] = t;
      }
    }
  }
  return a[4];
}

int finalCompassReading, initialCompassReading;
int upperLimit, lowerLimit;

bool TurnInstruction::progress() {
  // if this is the first call to progress
  if (this->begun == false) {
    this->begun = true;
    if (this->deg == 0)
      return true;

    int sum[10];
    for (int i = 0; i < 10; i++){
      compass_scalled_reading();
      compass_heading();
      sum[i] = bearing;
    }
    initialCompassReading = mode(sum, 10);
    finalCompassReading = (int)(abs(initialCompassReading + this->deg)) % 360;

    int x = 10;
    if (this->deg > 0) {
      upperLimit = finalCompassReading + x;
      lowerLimit = finalCompassReading - x;
      if (upperLimit >= 360) 
        upperLimit = upperLimit % 360;
      if (lowerLimit < 0)
        lowerLimit += 360;
    }
    else if (this->deg < 0) {
      if (initialCompassReading + this->deg < 0) {
        finalCompassReading = initialCompassReading + this->deg + 360;
      }
      else
        finalCompassReading = initialCompassReading + this->deg;
      upperLimit = finalCompassReading + x;
      lowerLimit = finalCompassReading - x;
    }  

    /*Serial.print(F("Begin turn "));
    Serial.print(this->deg);
    Serial.println(F(" deg"));
    Serial.print(F("Initial reading: "));
    Serial.print(initialCompassReading);
    Serial.println(F(" deg"));
    Serial.print(F("Final reading: "));
    Serial.print(finalCompassReading);
    Serial.println(F(" deg"));
    Serial.print(F("Lower limit: "));
    Serial.println(lowerLimit);
    Serial.print(F("Upper limit: "));
    Serial.println(upperLimit);*/

    int power = 70;   
    greenMotorMove(LH_IDX, -power, (this->deg > 0) ? MOTOR_BWD : MOTOR_FWD);
    greenMotorMove(RH_IDX, power, (this->deg > 0) ? MOTOR_BWD : MOTOR_FWD);
    greenMotorMove(REAR_IDX, -power, (this->deg > 0) ? MOTOR_BWD : MOTOR_FWD);
    greenMotorMove(GRABBER_IDX, 30, MOTOR_BWD);
  }

  int sum[10];
  for (int i = 0; i < 10; i++){
    compass_scalled_reading();
    compass_heading();
    sum[i] = bearing;
  }
  int avgBearing = mode(sum, 10);
  //Serial.println(avgBearing);
  
  if (avgBearing > lowerLimit && avgBearing < upperLimit) {
    greenMotorMove(LH_IDX, 100, MOTOR_BRAKE);
    greenMotorMove(RH_IDX, 100, MOTOR_BRAKE);
    greenMotorMove(REAR_IDX, 100, MOTOR_BRAKE);
    greenMotorMove(GRABBER_IDX, 100, MOTOR_BRAKE);
    motorStop(GRABBER_IDX);
    
    /*Serial.print(F("The last last angle: "));
    Serial.print(avgBearing);
    Serial.println(F(" deg"));*/
    
    return true;
  }

  return false;
}

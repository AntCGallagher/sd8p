#include "GoInstruction.h"
#include "compass.h"

float initialBearing;
int lowPowerMotor, highPowerMotor, lowPower, highPower;
int count = 0;

void GoInstruction::initFromCommand(Command cmd) {
  Serial.println(F("GO Initiating"));
  GoInstruction *fwd = new GoInstruction();
  fwd->cmdID = cmd.id;
  appendInstruction(fwd);
  Serial.println(F("GO Initiated"));
}

void GoInstruction::halt(void) {
  greenMotorMove(LH_IDX, 0, MOTOR_FLOAT);
  greenMotorMove(RH_IDX, 0, MOTOR_FLOAT);
}

bool GoInstruction::progress() {
  if (this->begun == false) {
    this->begun = true;
    this->startTime = millis();
  }

  if (count == 1) {
    getCompass();
    initialBearing = bearing;
    Serial.println(F("Initial Bearing"));
    Serial.print(initialBearing);
  }
  
  lowPower = 75;
  highPower = 80;

  getCompass();
  Serial.print(F("Initial Bearing:"));
  Serial.println(initialBearing);
  Serial.print(F("Bearing:"));
  Serial.println(bearing);
  Serial.print(F("Difference:"));
  Serial.println(bearing - initialBearing);
  
  if (bearing - initialBearing > 15) {
    lowPowerMotor = LH_IDX;
    highPowerMotor = RH_IDX;
  }
  else if (bearing - initialBearing < -15){
    lowPowerMotor = RH_IDX;
    highPowerMotor = LH_IDX;
  }
  else{
    lowPower = highPower;
  }

  if (count == 0) {
    greenMotorMove(LH_IDX, 100, MOTOR_FWD);
    greenMotorMove(RH_IDX, 100, MOTOR_FWD);
  }
  else
    forward(lowPowerMotor, highPowerMotor, lowPower, highPower);
  count++;
  return false;
}

void GoInstruction::forward(int lowPowerMotor, int highPowerMotor, int lowPower, int highPower){
  greenMotorMove(lowPowerMotor, lowPower, MOTOR_FWD);
  greenMotorMove(highPowerMotor, highPower, MOTOR_FWD);
  delay(1000);
  greenMotorAllStop();
}





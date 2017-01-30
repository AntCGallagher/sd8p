#include "ReverseInstruction.h"

// 180 clicks per rotation, one rotation is 26.5cm dist
#define CLICKS_PER_CM (180.0/26.5)

void ReverseInstruction::initFromCommand(Command cmd) {
  ReverseInstruction *rev = new ReverseInstruction();
  rev->dist = byteArrToUnsignedInt(cmd.params, 0);
  rev->cmdID = cmd.id;
  appendInstruction(rev);
}

void ReverseInstruction::halt(void) {
  greenMotorMove(LH_IDX, 0, MOTOR_FLOAT);
  greenMotorMove(RH_IDX, 0, MOTOR_FLOAT);
}

bool ReverseInstruction::brake(void) {

  updateMotorPositions();
  
  int clicks = positions[LH_IDX] + positions[RH_IDX];
  
  // first call to brake()
  if (!this->braking) {
    greenMotorMove(LH_IDX, 100, MOTOR_BRAKE);
    greenMotorMove(RH_IDX, 100, MOTOR_BRAKE);
    greenMotorMove(REAR_IDX, 100, MOTOR_BRAKE);
    this->braking = true;
    this->brakeLastClicksTime = millis();
    this->brakeLastClicks = clicks;
    return false;
  } 
  
  // new clicks arrived, reset timer
  if (abs(clicks) > abs(this->brakeLastClicks)) {
    this->brakeLastClicks = clicks;
    this->brakeLastClicksTime = millis();
    return false;
  }
  
  // if no clicks in last 50ms
  if (millis() - this->brakeLastClicksTime > 50) {
    // float motors
    this->halt();
    return true; 
  }
  
  return false;
}

bool ReverseInstruction::progress() {

  updateMotorPositions();
  
  if (this->begun == false) {
    this->begun = true;
    this->braking = false;
    this->startTime = millis();
    positions[LH_IDX] = 0;
    positions[RH_IDX] = 0;
    greenMotorMove(LH_IDX, 100, MOTOR_BWD);
    greenMotorMove(RH_IDX, 100, MOTOR_BWD);
  }
  
  // note both values are expected to be -ve
  int totalClicks = positions[LH_IDX] + positions[RH_IDX];
  int clicksRequired = this->dist * CLICKS_PER_CM * (-2);
  
  if (totalClicks <= clicksRequired) {
    return this->brake();
  }
  
  return false;
}





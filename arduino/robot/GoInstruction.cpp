#include "GoInstruction.h"

void GoInstruction::initFromCommand(Command cmd) {
  Serial.println(F("GO Initiating"));
  GoInstruction *fwd = new GoInstruction();
  fwd->cmdID = cmd.id;
  appendInstruction(fwd);
  Serial.println(F("GO Initiated"));
}

void GoInstruction::halt(void) {
  greenMotorMove(ROT_LH_MOTOR_IDX, 0, MOTOR_FLOAT);
  greenMotorMove(ROT_RH_MOTOR_IDX, 0, MOTOR_FLOAT);
}

bool GoInstruction::progress() {
  if (this->begun == false) {
    this->begun = true;
    this->startTime = millis();
    greenMotorMove(ROT_LH_MOTOR_IDX, 100, MOTOR_FWD);
    greenMotorMove(ROT_RH_MOTOR_IDX, 100, MOTOR_FWD);
  }

  return false;
}

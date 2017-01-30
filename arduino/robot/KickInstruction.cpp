#include "KickInstruction.h"
#include "PauseInstruction.h"

// number of clicks after prep pos that we know we've kicked
#define KICKED_AFTER_PREP_POS 4
#define GUARANTEED_TO_KICK (24/3)

void KickInstruction::initFromCommand(Command cmd) {
  // kick
  KickInstruction *kick = new KickInstruction();
  //kick->strength = byteArrToUnsignedShort(cmd.params, 0);
  appendInstruction(kick);
}

void KickInstruction::halt(void) {
  //retract motor
  greenMotorMove(ROT_FINGER_IDX, 100, MOTOR_BWD);
  PauseInstruction *pause = new PauseInstruction();
  pause->pause = 1000;
  appendInstruction(pause);
  //stop motor
  greenMotorMove(ROT_FINGER_IDX, 0, MOTOR_FLOAT);
}

bool KickInstruction::progress(void) {
  //kick
  greenMotorMove(ROT_FINGER_IDX, 100, MOTOR_FWD);
  PauseInstruction *pause = new PauseInstruction();
  pause->pause = 1000;
  appendInstruction(pause);
  //unkick
  greenMotorMove(ROT_FINGER_IDX, 100, MOTOR_BWD);
}

// given initialPos and kick strength, returns position at which kick will have occurred
int kickedPos(int initialPos, unsigned int stren) {
  return 0;
  //int distAheadOfPrepPos = distanceAhead(prepPos(stren), initialPos);

  // wasn't prepared correctly, make any kick lobe travel over it.
  //if (distAheadOfPrepPos > KICKED_AFTER_PREP_POS)
    //return initialPos + GUARANTEED_TO_KICK;

  //return initialPos + (KICKED_AFTER_PREP_POS - distAheadOfPrepPos);
}

bool KickInstruction::positionAcceptable(int pos, unsigned int stren, bool moving) {
  return true;
  //return (pos >= kickedPos(this->initialPosition, stren));
}

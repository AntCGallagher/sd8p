#include "KickInstruction.h"
#include "PauseInstruction.h"

// number of clicks after prep pos that we know we've kicked
#define KICKED_AFTER_PREP_POS 4
#define GUARANTEED_TO_KICK (24/3)

void KickInstruction::initFromCommand(Command cmd) {

  // pause so that grabber "relaxes"
  PauseInstruction *pause = new PauseInstruction();
  pause->pause = 200;
  appendInstruction(pause);

  // kick
  KickInstruction *kick = new KickInstruction();
  //kick->strength = byteArrToUnsignedShort(cmd.params, 0);
  appendInstruction(kick);

}

void KickInstruction::halt(void) {
  //retract motor
  greenMotorMove(ROT_FINGER_IDX, 0, MOTOR_BWD);
  //stop motor
  greenMotorMove(ROT_FINGER_IDX, 0, MOTOR_FLOAT);
}

bool KickInstruction::progress(void) {
  //kick
  greenMotorMove(ROT_FINGER_IDX, 0, MOTOR_FWD);
  //unkick
  greenMotorMove(ROT_FINGER_IDX, 0, MOTOR_BWD);
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


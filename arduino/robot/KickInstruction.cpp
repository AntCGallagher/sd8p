#include "SDPArduino.h"

#include "KickInstruction.h"
#include "PauseInstruction.h"


// number of clicks after prep pos that we know we've kicked
#define KICKED_AFTER_PREP_POS 4
#define GUARANTEED_TO_KICK (24/3)

void KickInstruction::initFromCommand(Command cmd) {
  updateMotorPositions();
  // kick
  KickInstruction *kick = new KickInstruction();
  //kick->strength = byteArrToUnsignedShort(cmd.params, 0);
  appendInstruction(kick);
  positions[KICKER_IDX] = 0;
}

void KickInstruction::halt(void) {
  //retract motor
  greenMotorMove(KICKER_IDX, 100, MOTOR_BRAKE);
  PauseInstruction *pause = new PauseInstruction();
  pause->pause = 1000;
  appendInstruction(pause);
}

bool KickInstruction::progress(void) {
  Serial.println("kicking");
  //while(positions[KICKER_IDX] < 120){
    greenMotorMove(KICKER_IDX, 100, MOTOR_BWD);
    //Serial.println(F(positions[KICKER_IDX]));
  //}
  delay(1825);
  Serial.println("stopping");
  greenMotorMove(KICKER_IDX, 100, MOTOR_BRAKE);
  //motorBackward(GRABBER_IDX, 20);
  //delay(200);

  return true;
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


#ifndef KICKINSTRUCTION_H
#define KICKINSTRUCTION_H

#include "hardware.h"

class KickInstruction : public Instruction {
public:
  static void initFromCommand(Command cmd);
  virtual bool positionAcceptable(int pos, unsigned int stren, bool moving);
  //int preparedForKickOfStrength(int pos);
};

#endif

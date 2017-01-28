#ifndef KICKINSTRUCTION_H
#define KICKINSTRUCTION_H

#include "hardware.h"
#include <stdlib.h>
#include "Comms.h"
#include "Instruction.h"

class KickInstruction : public Instruction {
public:
  static void initFromCommand(Command cmd);
  virtual bool positionAcceptable(int pos, unsigned int stren, bool moving);
  virtual void halt();
  virtual bool progress();
  //int preparedForKickOfStrength(int pos);
};

#endif


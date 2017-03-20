#ifndef TURNINSTRUCTION_H
#define TURNINSTRUCTION_H

#include "hardware.h"
#include "Instruction.h"

class TurnInstruction : public Instruction {
public:
  float deg;
  //int correctionsRemaining;
  
  int clicksAtBrake;
  int lastClicks;
  unsigned long lastClickTime;
  
  virtual void halt(void);
  virtual bool progress();
  static void initFromCommand(Command cmd);
};

#endif






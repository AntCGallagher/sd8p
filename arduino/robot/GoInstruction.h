#ifndef GOINSTRUCTION_H
#define GOINSTRUCTION_H

#include "hardware.h"
#include "Instruction.h"
#include "global.h"

class GoInstruction : public Instruction {
public:
  virtual void halt(void);
  virtual bool progress();
  static void initFromCommand(Command cmd);
  void forward(int lowPowerMotor, int highPowerMotor, int lowPower, int highPower);
  float getOffset();
};

#endif






#include "GoInstruction.h"
#include "compass.h"

float offset, heading, error;
int count;

void GoInstruction::initFromCommand(Command cmd) {
  //Serial.println(F("GO Initiating"));
  GoInstruction *fwd = new GoInstruction();
  fwd->cmdID = cmd.id;
  appendInstruction(fwd);
  //Serial.println(F("GO Initiated"));
}

void GoInstruction::halt(void) {
  greenMotorMove(LH_IDX, 0, MOTOR_FLOAT);
  greenMotorMove(RH_IDX, 0, MOTOR_FLOAT);
  greenMotorMove(REAR_IDX, 0, MOTOR_FLOAT);
}

bool GoInstruction::progress() {
  if (this->begun == false) {
    this->begun = true;
    this->startTime = millis();
    resetMotorPositions();
    offset = getOffset();
    //Serial.println();
    //Serial.print("Initial heading: ");
    //Serial.print(offset);
    heading = offset;
  }

  error = offset - heading;
  
  greenMotorMove(LH_IDX, 100, MOTOR_FWD);
  greenMotorMove(RH_IDX, 100, MOTOR_FWD);
  
  if (IRSensor.getDistanceCentimeter() < 10) {
    Serial.println(F("$BALL;"));
    return true;
  }

  int power = 60;
  if (offset < 180 /*&& abs(error) > 5*/) {
    if (heading > offset && heading < offset + 180)
      greenMotorMove(REAR_IDX, power, MOTOR_BWD);
    else
      greenMotorMove(REAR_IDX, power, MOTOR_FWD);
  }
  else if (offset > 180 /*&& abs(error) > 5*/) {
    if (heading < offset && heading > offset - 180)
      greenMotorMove(REAR_IDX, power, MOTOR_FWD); //BWD is right (clockwise); FWD is left (cclockwise);
    else
      greenMotorMove(REAR_IDX, power, MOTOR_BWD);
  }
  delay(275);
  greenMotorMove(REAR_IDX, 0, MOTOR_FLOAT);
  delay(500);

  heading = getOffset();
  //Serial.println(heading);
  return false;
}

//Helper function - returns 'mode'.
//Poorly named, as there was a name clash with another function..
float mod(int a[], int size) {
  for(int i=0; i<(size-1); i++) {
    for(int o=0; o<(size-(i+1)); o++) {
      if(a[o] > a[o+1]) {
        int t = a[o];
        a[o] = a[o+1];
        a[o+1] = t;
      }
    }
  }
  return a[4];
}
//Should be called getCompassReadings() 
float GoInstruction::getOffset(){
  int sum[10];
  for (int i = 0; i < 10; i++){
    compass_scalled_reading();
    compass_heading();
    sum[i] = bearing;
  }
  return mod(sum, 10);
}


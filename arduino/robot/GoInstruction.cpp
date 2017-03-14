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

  if (offset < 180 && abs(error) > 5) {
    if (heading > offset && heading < offset + 180)
      greenMotorMove(REAR_IDX, 100, MOTOR_BWD);
    else
      greenMotorMove(REAR_IDX, 100, MOTOR_FWD);
  }
  else if (offset > 180 && abs(error) > 5) {
    if (heading < offset && heading > offset - 180)
      greenMotorMove(REAR_IDX, 80, MOTOR_FWD); //BWD is right (clockwise); FWD is left (cclockwise);
    else
      greenMotorMove(REAR_IDX, 80, MOTOR_BWD);
  }
  delay(500);
  greenMotorMove(REAR_IDX, 0, MOTOR_FLOAT);
  delay(1000);

  heading = getOffset();
  //Serial.println(heading);
  return false;
}

/*
bool GoInstruction::progress() {
  if (this->begun == false) {
    this->begun = true;
    this->startTime = millis();
    resetMotorPositions();
  }
  int pow1, pow2, turn;
  float error;
  float Kp = 0.8;
  float offset = getOffset() - 180;
  Serial.println();
  Serial.print("Offset:");
  Serial.println(offset);
  int tp = 70;
  while(true){
    getCompass();
    error = bearing - offset - 180;
    Serial.print("Error: ");
    Serial.println(error);
    turn = Kp * error;
    pow1 = tp - turn;
    pow2 = tp + turn;
    Serial.print("Turn: ");
    Serial.println(turn);
    Serial.print("LH power: ");
    Serial.println(pow1);
    Serial.print("RH power: ");
    Serial.println(pow2);
    halt();
    greenMotorMove(LH_IDX, pow1, MOTOR_FWD);
    greenMotorMove(RH_IDX, pow2, MOTOR_FWD);
    delay(500);
    //halt();
  }
  return false;
}*/



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

float GoInstruction::getOffset(){
  int sum[10];
  for (int i = 0; i < 10; i++){
    compass_scalled_reading();
    compass_heading();
    sum[i] = bearing;
  }
  return mod(sum, 10);
}


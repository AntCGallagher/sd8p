#include <SDPArduino.h>

#include <SoftwareSerial.h>
#include <Wire.h>
#include <stdlib.h>

#include "SDPArduino.h"
#include "Comms.h"
#include "Instruction.h"
#include "MemoryFree.h"
#include "compass.h"


Comms comms;
unsigned long memPrintTimer;
int distance;

void setup() {
  hardwareSetup();

  // set instructions array to NULL pointers
  deleteAllInstructions();

  memPrintTimer = millis();

  // let PC know we've started up and to send commands with ID starting at 1
  comms.sendArdReset();

  Serial.print(F("READY")) ;

  motorAllStop();

  compass_x_gainError = 0.86;
  compass_y_gainError = 0.67;
  compass_z_gainError = 0.54;
  compass_x_offset = 571.45;
  compass_y_offset = 854.89;
  compass_z_offset = 1026.79;

  compass_init(2);
  //compass_offset_calibration(3);

}

void loop() {
  // calls progress method on instruction at index 0
  progressInstruction();

  comms.readSerial();

  // check memory level every second
  if (millis() - memPrintTimer > 1000) {
    int memAvail = freeMemory();
    if (memAvail < 512) {
      Serial.println(F("Low Memory "));
      Serial.println(freeMemory());
    }
   memPrintTimer = millis();
  }

//  distance = Dist.getDistanceCentimeter();
//  Serial.print("Distance in centimeters: ");
//  Serial.println(distance);
//  delay(1000);

  //updateMotorPositions();
  //printMotorPositions();
  //delay(1000);

  //greenMotorMove(LH_IDX, 50, MOTOR_FWD);
  //greenMotorMove(RH_IDX, 50, MOTOR_FWD);
  //greenMotorMove(REAR_IDX, 50, MOTOR_FWD);

  //getCompass();

}

// converts single byte to int
int byteArrToUnsignedShort(byte arr[], int firstByteIdx) {
  return arr[firstByteIdx];
}

// given an array of bytes (most significant first), takes 2 bytes to
// form an unsigned integer
unsigned int byteArrToUnsignedInt(byte arr[], int firstByteIdx) {
  return arr[firstByteIdx] << 8 | arr[firstByteIdx+1];
}

// given an array of bytes (most significant first), takes 4 bytes to
// form an unsigned integer
unsigned long byteArrToUnsignedLong(byte arr[], int fbi) {
  return (unsigned long)arr[fbi] << 24 | (unsigned long)arr[fbi+1] << 16 | (unsigned long)arr[fbi+2] << 8 | (unsigned long)arr[fbi+3];
}

// given an array of bytes (most significant first), takes 2 bytes to
// form a signed integer
int byteArrToSignedInt(byte arr[], int firstByteIdx) {
  // cast to signed char so that int will interpret it in 2s compliment
  return static_cast<signed char>(arr[firstByteIdx]) << 8 | arr[firstByteIdx+1];
}

void printVector(Vector v) {
  print("(");
  print(v.x);
  print(",");
  print(v.y);
  println(")");
}

Vector makeVector(double x, double y) {
  Vector v;
  v.x = x;
  v.y = y;
  return v;
}

void printPoint(Point p) {
  print("(");
  print(p.x);
  print(",");
  print(p.y);
  println(")");
}

Point makePoint(int x, int y) {
  Point p;
  p.x = x;
  p.y = y;
  return p;
}

void printPosition(Position p) {
  print("(");
  print(p.coor.x);
  print(",");
  print(p.coor.y);
  print(") ");
  println(p.head);
}

Position makePosition(int x, int y, int h) {
  Position p;
  p.coor = makePoint(x, y);
  p.head = h;
  return p;
}

Position makePosition(Point point, int h) {
  Position p;
  p.coor = point;
  p.head = h;
  return p;
}

double toRad(double deg) {
  return (deg/180)*M_PI;
}

double toDeg(double rad) {
  return rad * 180/M_PI;
}

// if heading u, to get to v, turn by x degrees
double vectorAngle(Vector u, Vector v) {
  double dot  = (u.x*v.x) + (u.y*v.y);
  double det = (u.x*v.y) - (u.y*v.x);
  double angle = atan2(det,dot);
  return toDeg(angle);
}

int pointToPointDistance(Point a, Point b) {
  return sqrt(pow(a.x-b.x, 2) + pow(a.y-b.y,2));
}


// Printing

#define IGNORE_PRINTS false

void println(char *c) {
  if (IGNORE_PRINTS)
    return;
  Serial.println(c);
}

void println(const char *c) {
  if (IGNORE_PRINTS)
    return;
  Serial.println(c);
}

void println(__FlashStringHelper *c) {
  if (IGNORE_PRINTS)
    return;
  Serial.println(c);
}

void println(int i) {
  if (IGNORE_PRINTS)
    return;
  Serial.println(i);
}

void println(long l) {
  if (IGNORE_PRINTS)
    return;
  Serial.println(l);
}

void println(unsigned long l) {
  if (IGNORE_PRINTS)
    return;
  Serial.println(l);
}

void println(float f) {
  if (IGNORE_PRINTS)
    return;
  Serial.println(f);
}

void println(double d) {
  if (IGNORE_PRINTS)
    return;
  Serial.println(d);
}

void println(bool b) {
  if (IGNORE_PRINTS)
    return;
  Serial.println(b);
}

void print(char *c) {
  if (IGNORE_PRINTS)
    return;
  Serial.print(c);
}

void print(const char *c) {
  if (IGNORE_PRINTS)
    return;
  Serial.print(c);
}

void print(__FlashStringHelper *c) {
  if (IGNORE_PRINTS)
    return;
  Serial.print(c);
}

void print(int i) {
  if (IGNORE_PRINTS)
    return;
  Serial.print(i);
}

void print(long l) {
  if (IGNORE_PRINTS)
    return;
  Serial.print(l);
}

void print(unsigned long l) {
  if (IGNORE_PRINTS)
    return;
  Serial.print(l);
}

void print(float f) {
  if (IGNORE_PRINTS)
    return;
  Serial.print(f);
}

void print(double d) {
  if (IGNORE_PRINTS)
    return;
  Serial.print(d);
}

void print(bool b) {
  if (IGNORE_PRINTS)
    return;
  Serial.print(b);
}

 /* END */

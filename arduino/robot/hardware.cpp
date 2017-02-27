#include "hardware.h"
#include "global.h"

#include "SDPArduino.h"

#include <Wire.h>

// Reference the HMC5883L Compass Library
#include "HMC5883L.h"

// Store our compass as a variable.
HMC5883L compass;
// Record any errors that may occur in the compass.
int error = 0;

MagnetometerScaled valueOffset;

void hardwareSetup() {

 //Initial set up for arduino connected to the power board.
 pinMode(2,INPUT);
 pinMode(3,OUTPUT);
 pinMode(4,INPUT);
 pinMode(5,OUTPUT);
 pinMode(6,OUTPUT);
 pinMode(7,INPUT);
 pinMode(8,OUTPUT);
 pinMode(9,OUTPUT);
 pinMode(10,INPUT);
 pinMode(11,INPUT);
 pinMode(12,INPUT);
 pinMode(13,INPUT);
 pinMode(A0,INPUT);
 pinMode(A1,INPUT);
 pinMode(A2,INPUT);
 pinMode(A3,INPUT);
 digitalWrite(8,HIGH); //Pin 8 must be high to turn the radio on!
 Serial.begin(115200); // Serial rate the radio is configured to.
 Wire.begin(); //Makes arduino master of the I2C line.
 greenMotorAllStop();
 resetMotorPositions();
}

/* COMPASS */

// calibrate offset of x, y and z
void compassCalibrate(void){
  //Serial << ">>>> calibrate the compass\n";
  Serial.println("calibrate the compass");
  MagnetometerScaled valueMax = {0, 0, 0};
  MagnetometerScaled valueMin = {0, 0, 0};

  // calculate x, y and z offset

  //Serial << "please rotate the compass" << endl;
  Serial.println("please rotate the compass");
  int xcount = 0;
  int ycount = 0;
  int zcount = 0;
  boolean xZero = false;
  boolean yZero = false;
  boolean zZero = true;
  MagnetometerScaled value;
  while (xcount < 3 || ycount < 3 /*|| zcount < 3*/) {
    //Serial.println(xcount);
    //Serial.println(ycount);
    //Serial.println(zcount);
    greenMotorMove(LH_IDX, 70, MOTOR_FWD);
    greenMotorMove(RH_IDX, 70, MOTOR_BWD);

    value = compass.readScaledAxis();
    if ((fabs(value.XAxis) > 600) || (fabs(value.YAxis) > 600) || (fabs(value.ZAxis) > 600)) {
      continue;
    }

    if (valueMin.XAxis > value.XAxis) {
      valueMin.XAxis = value.XAxis;
    } else if (valueMax.XAxis < value.XAxis) {
      valueMax.XAxis = value.XAxis;
    }

    if (valueMin.YAxis > value.YAxis) {
      valueMin.YAxis = value.YAxis;
    } else if (valueMax.YAxis < value.YAxis) {
      valueMax.YAxis = value.YAxis;
    }

    if (valueMin.ZAxis > value.ZAxis) {
      valueMin.ZAxis = value.ZAxis;
    } else if (valueMax.ZAxis < value.ZAxis) {
      valueMax.ZAxis = value.ZAxis;
    }


    if (xZero) {
      if (fabs(value.XAxis) > 50) {
        xZero = false;
        xcount++;
      }
    } else {
      if (fabs(value.XAxis) < 40) {
        xZero = true;
      }
    }

    if (yZero) {
      if (fabs(value.YAxis) > 50) {
        yZero = false;
        ycount++;
      }
    } else {
      if (fabs(value.YAxis) < 40) {
        yZero = true;
      }
    }

    if (zZero) {
      if (fabs(value.ZAxis) > 50) {
        zZero = false;
        zcount++;
      }
    } else {
      if (fabs(value.ZAxis) < 40) {
        zZero = true;
      }
    }

    delay(30);
  }
  greenMotorMove(LH_IDX, 0, MOTOR_BRAKE);
  greenMotorMove(RH_IDX, 0, MOTOR_BRAKE);
  greenMotorAllStop();

  valueOffset.XAxis = (valueMax.XAxis + valueMin.XAxis) / 2;
  valueOffset.YAxis = (valueMax.YAxis + valueMin.YAxis) / 2;
  valueOffset.ZAxis = (valueMax.ZAxis + valueMin.ZAxis) / 2;
#if 0
  Serial << "max: " << valueMax.XAxis << '\t' << valueMax.YAxis << '\t' << valueMax.ZAxis << endl;
  Serial << "min: " << valueMin.XAxis << '\t' << valueMin.YAxis << '\t' << valueMin.ZAxis << endl;
  Serial << "offset: " << valueOffset.XAxis << '\t' << valueOffset.YAxis << '\t' << valueOffset.ZAxis << endl;

  Serial << "<<<<" << endl;
#endif
  Serial.print("max: ");
  Serial.print(valueMax.XAxis);
  Serial.print(valueMax.YAxis);
  Serial.println(valueMax.ZAxis);
  Serial.print("min: ");
  Serial.print(valueMin.XAxis);
  Serial.print(valueMin.YAxis);
  Serial.println(valueMin.ZAxis);
  Serial.print("offset: ");
  Serial.print(valueOffset.XAxis);
  Serial.print(valueOffset.YAxis);
  Serial.println(valueOffset.ZAxis);
}

void getCompass(){
  // Retrive the raw values from the compass (not scaled).
  MagnetometerRaw raw = compass.readRawAxis();
  // Retrived the scaled values from the compass (scaled to the configured scale).
  MagnetometerScaled scaled = compass.readScaledAxis();

  scaled.XAxis -= valueOffset.XAxis;
  scaled.YAxis -= valueOffset.YAxis;
  scaled.ZAxis -= valueOffset.ZAxis;

  // Values are accessed like so:
  int MilliGauss_OnThe_XAxis = scaled.XAxis;// (or YAxis, or ZAxis)

  // Calculate heading when the magnetometer is level, then correct for signs of axis.
  float yxHeading = atan2(scaled.YAxis, scaled.XAxis);
  float zxHeading = atan2(scaled.ZAxis, scaled.XAxis);

  float heading = yxHeading;

  // Once you have your heading, you must then add your 'Declination Angle', which is the 'Error' of the magnetic field in your location.
  // Find yours here: http://www.magnetic-declination.com/
  // Mine is: -2��37' which is -2.617 Degrees, or (which we need) -0.0456752665 radians, I will use -0.0457
  // If you cannot find your Declination, comment out these two lines, your compass will be slightly off.
  float declinationAngle = -0.0457;
  heading += declinationAngle;

  // Correct for when signs are reversed.
  if(heading < 0)
    heading += 2*PI;

  // Check for wrap due to addition of declination.
  if(heading > 2*PI)
    heading -= 2*PI;

  // Convert radians to degrees for readability.
  float headingDegrees = heading * 180/M_PI;

  float yxHeadingDegrees = yxHeading * 180 / M_PI;
  float zxHeadingDegrees = zxHeading * 180 / M_PI;

  // Output the data via the serial port.
  Output(raw, scaled, heading, headingDegrees);

//  Serial << scaled.XAxis << ' ' << scaled.YAxis << ' ' << scaled.ZAxis << endl;
//  Serial << "arctan y/x: " << yxHeadingDegrees << " \tarctan z/x: " << zxHeadingDegrees << endl;

  //Serial.print(scaled.XAxis);
  //Serial.print(scaled.YAxis);
  //Serial.println(scaled.ZAxis);

  Serial.print("arctan y/x: ");
  Serial.println(yxHeadingDegrees);
  //Serial.print("arctan z/x: ");
  //Serial.print(zxHeadingDegrees);

  // Normally we would delay the application by 66ms to allow the loop
  // to run at 15Hz (default bandwidth for the HMC5883L).
  // However since we have a long serial out (104ms at 9600) we will let
  // it run at its natural speed.
  delay(1000);//of course it can be delayed longer.
}

// Output the data down the serial port.
void Output(MagnetometerRaw raw, MagnetometerScaled scaled, float heading, float headingDegrees){
   Serial.print("Raw:\t");
   Serial.print(raw.XAxis);
   Serial.print("   ");
   Serial.print(raw.YAxis);
   Serial.print("   ");
   Serial.println(raw.ZAxis);
   
   Serial.print("Scaled:\t");
   Serial.print(scaled.XAxis);
   Serial.print("   ");
   Serial.print(scaled.YAxis);
   Serial.print("   ");
   Serial.println(scaled.ZAxis);

   Serial.print("Heading:\t");
   Serial.print(heading);
   Serial.print(" Radians   \t");
   Serial.print(headingDegrees);
   Serial.println(" Degrees   \t");
}



/* MOTORS */

long int positions[ROTARY_COUNT] = {0};

void updateMotorPositions() {
  // Request motor position deltas from rotary slave board

  Wire.requestFrom(ROTARY_SLAVE_ADDRESS, ROTARY_COUNT);

  // Update the recorded motor positions
  for (int i = 0; i < ROTARY_COUNT; i++) {
    positions[i] += (int8_t) Wire.read();  // Must cast to signed 8-bit type
  }
}

void resetMotorPositions() {
  updateMotorPositions() ;
  memset(positions , 0 , sizeof(positions)) ;
}

void printMotorPositions() {
  Serial.print("Motor positions: ");
  int i ;
  for ( i = 0; i < ROTARY_COUNT; i++) {
    Serial.print(positions[i]);
    Serial.print(" ");
  }
  Serial.println("");
}

void greenMotorAllStop() {
  motorAllStop();
}

// motorNo in range [1,8]
// motorPower in range [0,100]
// dir: 0 float, 1 fwd, 2 bckw, 3 brake
void greenMotorMove(int motorNum, int motorPower, enum MOTOR_DIR dir) {

 if (motorNum > 6 || motorNum < 0)
   return;

 if (motorPower < 0) {
   motorPower = abs(motorPower);
   if (dir == MOTOR_FWD) dir = MOTOR_BWD;
   else if (dir == MOTOR_BWD) dir = MOTOR_FWD;
 }
 if (motorPower > 100)
   motorPower = 100;

 //if (motorNum == LH_IDX){
   //if (dir == MOTOR_FWD) dir = MOTOR_BWD;
   //else if (dir == MOTOR_BWD) dir = MOTOR_FWD;
 //}

 if (motorNum == LH_IDX){
   motorPower = motorPower*95/100;
 }

 //adapting the code base to work with the motor board we are using
 if(dir == MOTOR_FWD) motorForward(motorNum, motorPower);
 else if (dir == MOTOR_BWD) motorBackward(motorNum, motorPower);
 //float break and normal break are treated the same way
 else if (dir == MOTOR_FLOAT)
   motorStop(motorNum);
 else {
   motorForward(motorNum, 100);
   motorStop(motorNum);
 }

}

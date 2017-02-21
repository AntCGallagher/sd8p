#ifndef HARDWARE_H
#define HARDWARE_H

#define LH_IDX 3
#define RH_IDX 5
#define KICKER_IDX 2
#define GRABBER_IDX 1                                                                                                                                                                                                                                                   
#define REAR_IDX 4


// // Arduino direct I/O
// #define SONAR_GRABBER_TRIG 3
// #define SONAR_GRABBER_ECHO A3
// #define REED_SWITCH_GRABBER 5

void hardwareSetup();


/* MOTORS / ROTARY ENCODERS */

enum MOTOR_DIR {
	MOTOR_FLOAT = 0,
	MOTOR_FWD = 1,
	MOTOR_BWD = 2,
	MOTOR_BRAKE = 3
};

#define ROTARY_SLAVE_ADDRESS 5
#define ROTARY_COUNT 6
#define PRINT_DELAY 200

extern long int positions[ROTARY_COUNT];// = {0};

void resetMotorPositions();
void updateMotorPositions();
void printMotorPositions();

void greenMotorMove(int motorNum, int motorPower, enum MOTOR_DIR dir);
void greenMotorAllStop(void);


// /* SONAR */
// int sonarDistance(int trigPin, int echoPin, int maxDist);
// bool ballInReach(int *counter, int countsRequired);
//

/* GRABBER */
bool hasBall();


#endif


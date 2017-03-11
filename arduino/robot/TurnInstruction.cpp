#include "TurnInstruction.h"
#include "global.h"
#include "compass.h"

// used for SpeedRecorder
#define CLICKS_TIME_PERIOD 30 // ms
#define CLICKS_TIME_SLOTS 10

// used for small turns only
#define SMALL_TURN_LIMIT 3    // clicks
// time at which to brake
#define TIME_UNTIL_1_CLICK 70 // ms
#define TIME_UNTIL_2_CLICK (TIME_UNTIL_1_CLICK+30) // ms
#define TIME_UNTIL_3_CLICK (TIME_UNTIL_2_CLICK+25) // ms

// if we don't see a click for x amount of time, assume robot has stopped
#define MAX_CLICK_PERIOD_FOR_STOPPED 100 // ms

#define CORRECTION_TOLERANCE 1 // clicks

//#define DEBUG_PRINT_TURN 

/* increase denominator to make robot turn more
 * it's rare this will have to be changed
 * occasions will include:
 *   changing wheel geometry or
 *   changing power ratio between side wheels and rear wheel
 */
#define DEG_PER_CLICK (360.0/92.0)

void TurnInstruction::initFromCommand(Command cmd) {
  TurnInstruction *turn = new TurnInstruction();
  turn->deg = byteArrToSignedInt(cmd.params, 0);
#ifdef DEBUG_PRINT_TURN
  Serial.print(F("Turn "));
  Serial.println(turn->deg);
#endif
  turn->correctionsRemaining = byteArrToUnsignedShort(cmd.params, 2);
  turn->cmdID = cmd.id;
  appendInstruction(turn);
}

void TurnInstruction::halt(void) {
  greenMotorMove(LH_IDX, 0, MOTOR_FLOAT);
  greenMotorMove(RH_IDX, 0, MOTOR_FLOAT);
  greenMotorMove(REAR_IDX, 0, MOTOR_FLOAT);
}

float clicksToDeg(float clicks) {
  return clicks * DEG_PER_CLICK;
}

float degToClicks(float deg) {
  return deg / DEG_PER_CLICK;
}

float projectedAdditionalClicksFromSum(int sum) {
  if (sum == 0)
    return 0;
  // See which work better than others
  float proj = 1.981*log(abs(sum)) + 3.449;
  //float proj = 1.239*log(abs(sum)) + 2.061;
  //float proj = 1.334*log(abs(sum)) + 1.039;
  if (sum < 0)
    return -1*proj;
  return proj;
}

long unsigned turnLastP;

bool TurnInstruction::progress() {

  updateMotorPositions();

  getCompass();
  float initialCompassReading = bearing;

  // if this is the first call to progress
  if (this->begun == false) {
    this->begun = true;
    this->startTime = millis();
    this->brakeTime = 0;
    this->braking = false;
    if (this->deg == 0)
      return true;

    this->clicksAtBrake = 0;
    this->lastClicks = 0;
    this->lastClickTime = millis();

    // reset motor position counter
    positions[REAR_IDX] = 0;

#ifdef DEBUG_PRINT_TURN
    Serial.print(F("Begin turn "));
    Serial.print(degToClicks(this->deg));
    Serial.print(F(" clicks ("));
    Serial.print(this->deg);
    Serial.println(F(" deg)"));
#endif

    greenMotorMove(LH_IDX, -70, (this->deg > 0) ? MOTOR_BWD : MOTOR_FWD);
    greenMotorMove(RH_IDX, 70, (this->deg > 0) ? MOTOR_BWD : MOTOR_FWD);
    greenMotorMove(REAR_IDX, -100, (this->deg > 0) ? MOTOR_BWD : MOTOR_FWD);
    greenMotorMove(GRABBER_IDX, 30, MOTOR_BWD);
  }

  float totalClicksRequired = degToClicks(this->deg);
  float travelled = positions[REAR_IDX] + projectedAdditionalClicksFromSum(positions[REAR_IDX]);

  //Serial.print(F("Travelled:"));
  //Serial.println(travelled);

  // keep effective timer of when a click occurs
  if (positions[REAR_IDX] != this->lastClicks) {
    this->lastClickTime = millis();
    this->lastClicks = positions[REAR_IDX];
  }

  if (this->braking) {

    // haven't seen any clicks in over x ms
    if (millis() - max(this->lastClickTime, this->brakeTime) > MAX_CLICK_PERIOD_FOR_STOPPED) {

      // return motors to floating
      greenMotorMove(LH_IDX, 0, MOTOR_FLOAT);
      greenMotorMove(RH_IDX, 0, MOTOR_FLOAT);
      greenMotorMove(REAR_IDX, 0, MOTOR_FLOAT);
      greenMotorMove(GRABBER_IDX, 0, MOTOR_FLOAT);

#ifdef DEBUG_PRINT_TURN
      Serial.print(F("Braking covered "));
      Serial.print(positions[REAR_IDX] - clicksAtBrake);
      Serial.print(F(" clicks ("));
      Serial.print(clicksToDeg(positions[REAR_IDX] - clicksAtBrake));
      Serial.print(F(" deg) total "));
      Serial.print(positions[REAR_IDX]);
      Serial.print(F(" clicks ("));
      Serial.print(clicksToDeg(positions[REAR_IDX]));
      Serial.println(F(" deg)"));
#endif

     float miss = totalClicksRequired - positions[REAR_IDX];
     if (abs(miss) >= CORRECTION_TOLERANCE && this->correctionsRemaining > 0) {
       TurnInstruction *nextTurn = new TurnInstruction();
       nextTurn->deg = clicksToDeg(miss);
       nextTurn->correctionsRemaining = this->correctionsRemaining - 1;
       insertInstruction(nextTurn, 1);
     } else {
       // let PC know we're done
       if (this->cmdID > -1) {
         comms.sendInstructionComplete(this->cmdID);
         this->cmdID = -1;
       }
     }
      return true;
    }
    return false;
  }

  // signs must be same
  bool travelledPos = (travelled >= 0);
  bool toTravelPos = (totalClicksRequired >= 0);
  bool signsEqual = !(travelledPos ^ toTravelPos);

  // for small turns, clicks are not granular enough, so use time
  bool smallTurnTimeElapsed = false;
  if (abs((int)totalClicksRequired) <= SMALL_TURN_LIMIT) {
    unsigned long timeElapsed = millis() - this->startTime;

    switch (abs((int)totalClicksRequired)) {
      case 1:
        smallTurnTimeElapsed = (timeElapsed >= TIME_UNTIL_1_CLICK);
        break;
      case 2:
        smallTurnTimeElapsed = (timeElapsed >= TIME_UNTIL_2_CLICK);
        break;
      case 3:
        smallTurnTimeElapsed = (timeElapsed >= TIME_UNTIL_3_CLICK);
        break;
      default:
        smallTurnTimeElapsed = (timeElapsed >= (TIME_UNTIL_1_CLICK*abs(totalClicksRequired)));
        break;
    }
  }

  // check if complete - either by clicks or by duration (small turns only)
  getCompass();
  float finalCompassReading = bearing;
  if ((signsEqual && abs(travelled) >= abs(totalClicksRequired)) || smallTurnTimeElapsed && (finalCompassReading - initialCompassReading >= this->deg)) {

    this->brakeTime = millis();
    this->braking = true;
    clicksAtBrake = positions[REAR_IDX];

    greenMotorMove(LH_IDX, 100, MOTOR_BRAKE);
    greenMotorMove(RH_IDX, 100, MOTOR_BRAKE);
    greenMotorMove(REAR_IDX, 100, MOTOR_BRAKE);
    greenMotorMove(GRABBER_IDX, 40, MOTOR_BRAKE);

#ifdef DEBUG_PRINT_TURN
    Serial.print(F("BRAKING at"));
    Serial.print(clicksAtBrake);
    Serial.print(F(" clicks ("));
    Serial.print(clicksToDeg(clicksAtBrake));
    Serial.println(F(" deg)"));
    //Serial.print(F("Estimating "));
    //Serial.print((positions[REAR_IDX]));
    //Serial.println(F(" extra clicks"));
    //if (smallTurnTimeElapsed)
      //Serial.println(F(StoppedSerial.print(F(" turning ")); based on time for small turn));
#endif
  }

  // sensible debug print interval
  if (millis() - turnLastP > 300) {
    turnLastP = millis();

  }

  return false;
}

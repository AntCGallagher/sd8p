#include <SoftwareSerial.h>
#include <Wire.h>
#include <stdlib.h>

#include "Comms.h"
#include "Instruction.h"
#include "MemoryFree.h"

Comms comms;
unsigned long memPrintTimer;

void setup() {
  Serial.begin(115200);  
  
  // set instructions array to NULL pointers
  deleteAllInstructions();
  memPrintTimer = millis();
  
  // let PC know we've started up and to send commands with ID starting at 1
  comms.sendArdReset();
  
  Serial.print(F("READY")) ;
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
}

void setup() {
  Serial.begin(115200);
  Serial.print(F("Ready!"));
}

void loop() {
  if (Serial.available() > 0) {
    String msg = Serial.readString();
    if (msg == "ping") {
      Serial.print(F("Pong!"));
    }      
  }
}



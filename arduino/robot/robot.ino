void setup() {
  Serial.begin(115200);
  Serial.println(F("Hello, World!"));
}

void loop() {
  if (Serial.available() > 0) {
    String msg = Serial.readString();
    Serial.println(msg);
    if (msg == "ping") {
      Serial.println(F("Pong!"));
    }      
  }
}



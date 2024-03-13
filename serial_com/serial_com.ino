#include <dummy.h>

// Pin connected to X0 on ESP32
const int X0_PIN = 0; // Change this to the appropriate pin number

void setup() {
  // Initialize serial communication
  Serial.begin(9600);
  
  // Set X0 pin as input
  pinMode(X0_PIN, INPUT);
}

void loop() {
  // Read the state of X0 pin
  int x0State = digitalRead(X0_PIN);
  
  // Check if X0 is set
  if (x0State == LOW) {
    // Print "OK" to Serial Monitor
    Serial.println("OK");
  }
  
  // Add a small delay to avoid flooding the Serial Monitor
  delay(100);
}

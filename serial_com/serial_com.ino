#include <dummy.h>

// Pin connected to X0 on ESP32
const int X0_PIN = 26; // Change this to the appropriate pin number for X0
// Pin connected to X1 on ESP32
const int X1_PIN = 27; // Change this to the appropriate pin number for X1
// Pin connected to X2 on ESP32
const int X2_PIN = 32; // Change this to the appropriate pin number for X2
// Pin connected to X3 on ESP32
const int X3_PIN = 33; // Change this to the appropriate pin number for X3
// Pin connected to X4 on ESP32
const int X4_PIN = 34; // Change this to the appropriate pin number for X4
// Pin connected to X5 on ESP32
const int X5_PIN = 35; // Change this to the appropriate pin number for X5
// Pin connected to X6 on ESP32
const int X6_PIN = 36; // Change this to the appropriate pin number for X6
// Pin connected to X7 on ESP32
const int X7_PIN = 39; // Change this to the appropriate pin number for X7

bool prev[8] = {LOW}; // Array to store previous state of each pin

void setup() {
  // Initialize serial communication
  Serial.begin(9600);
  
  // Set all X pins as input
  pinMode(X0_PIN, INPUT);
  pinMode(X1_PIN, INPUT);
  pinMode(X2_PIN, INPUT);
  pinMode(X3_PIN, INPUT);
  pinMode(X4_PIN, INPUT);
  pinMode(X5_PIN, INPUT);
  pinMode(X6_PIN, INPUT);
  pinMode(X7_PIN, INPUT);
}

void loop() {
  // Array of pin numbers
  const int pins[8] = {X0_PIN, X1_PIN, X2_PIN, X3_PIN, X4_PIN, X5_PIN, X6_PIN, X7_PIN};

  // Loop through each pin
  for (int i = 0; i < 8; i++) {
    // Read the state of the pin
    int xState = digitalRead(pins[i]);

    // Check if pin is set
    if (xState == HIGH) {
      Serial.print("x");
      Serial.print(i);
      Serial.println(" on");
    } else {
      Serial.print("x");
      Serial.print(i);
      Serial.println(" off");
    }

    prev[i] = xState;
  }

  // Add a small delay to avoid flooding the Serial Monitor
  delay(1000);
}

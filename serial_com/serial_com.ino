#include <dummy.h>

// Pin connected to X0 on ESP32
const int X0_PIN = 0; // Change this to the appropriate pin number
bool prev = LOW;
int x = 0; // Initialize x to 0

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
  if (prev == LOW && x0State == HIGH) {
    // Increment x and print to Serial Monitor
    x++;
    Serial.println("OKAY\r\n");
  }

  if (prev == HIGH && x0State == LOW){
    // Increment x and print to Serial Monitor
    x++;
    Serial.println("not okay \r\n");
  }
  prev = x0State;
  
  // Add a small delay to avoid flooding the Serial Monitor
  //delay(1000);
}

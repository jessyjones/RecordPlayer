

const int analogInPin = A0;  // Analog input pin that the first potentiometer is attached to
const int analogInPin1 = A1;  // Analog input pin that the second potentiometer is attached to
const int analogInPin2 = A2;  // Analog input pin that the third potentiometer is attached to
const int analogInPin3 = A3;  // Analog input pin that the fourth potentiometer is attached to

double sensorValue = 0;        // value read from the potentiometer
int outputValue = 0;        // value scaled from 0 to 100

void setup() {
  // initialize serial communications at 9600 bps:
  Serial.begin(9600);
}

void loop() {
  // Read the value from the first potentiometer
  sensorValue = analogRead(analogInPin);
  // Map it between 0 and 100
  outputValue = map(sensorValue, 0, 1023, 0, 100);
  // Output it to Serial
  // Serial.print("sensor 0 = ");
  Serial.print(outputValue);
  Serial.print(",");
  // Give the analog/digital converter a little time to settle down - not sure that this step is needed but the sample code had it so ...
  delay(2);
  // Do the same operations for each potentiometer
  sensorValue = analogRead(analogInPin1);
  outputValue = map(sensorValue, 0, 1023, 0, 100);
  //Serial.print(" sensor 1 = ");
  Serial.print(outputValue);
  Serial.print(",");
  delay(2);
  sensorValue = analogRead(analogInPin2);
  outputValue = map(sensorValue, 0, 1023, 0, 100);
  //Serial.print(" sensor 2 = ");
  Serial.print(outputValue);
  Serial.print(",");
  delay(2);
  sensorValue = analogRead(analogInPin3);
  outputValue = map(sensorValue, 0, 1023, 0, 100);
  //Serial.print(" sensor 3 = ");
  Serial.print(outputValue);
  Serial.println();
  // Wait for a bit, and go back to the beginning of the loop
  delay(200);
}

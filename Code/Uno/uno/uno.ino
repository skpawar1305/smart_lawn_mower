#include <Servo.h>
#include <NewPing.h>

// Include Arduino Wire library for I2C
#include <Wire.h>

// Define Slave I2C Address
#define SLAVE_ADDR 9

//hc-sr04 sensor
#define trig 5
#define echo 4
#define max_distance 50
NewPing sonar(trig, echo, max_distance);

//ir sensor
#define irRight 2
#define irLeft 3

bool boundary1 = false;
bool boundary2 = false;

//motors
int motor1pin1 = 9;
int motor1pin2 = 10;
int motor1en = A2;
int motor2pin1 = 11;
int motor2pin2 = 12;
int motor2en = A3;
int servopin = 6;

int val = 0;
int distance = 0;

Servo servo;

int previous_millis = 0;
int duration = 0;
void setup() {
  pinMode(trig , OUTPUT);
  pinMode(echo , INPUT);
  Serial.begin(9600);
  servo.attach(servopin);
  servo.write(90);

  pinMode(motor1pin1, OUTPUT);
  pinMode(motor1pin2, OUTPUT);
  pinMode(motor2pin1, OUTPUT);
  pinMode(motor2pin2, OUTPUT);
  pinMode(motor1en, OUTPUT);
  pinMode(motor2en, OUTPUT);
  analogWrite(motor1en, 128);
  analogWrite(motor2en, 128);

  pinMode(irLeft , INPUT);
  pinMode(irRight , INPUT);

  //I2C
  // Initialize I2C communications as Slave
  Wire.begin(SLAVE_ADDR);

  // Function to run when data received from master
  Wire.onReceive(receiveEvent);

  // Setup Serial Monitor
  Serial.begin(115200);
}

void receiveEvent() {
  // read one character from the I2C
  val = Wire.read();
  // Print value of incoming data
  Serial.println(val);
}

void loop() {
  if (val == 1) {
    if (digitalRead(irLeft) != 0) {
      moveLeft();
    }
    if (digitalRead(irRight) != 0) {
      moveRight();
    }
    objectAvoid();
  } else if (val == 2) {
    Stop();
  } else if (val == 2) {
    charge_station();
  }
}

void objectAvoid() {
  delay(70);
  distance = sonar.ping_cm();
  Serial.println(distance);
  if (distance == 0) {
    distance = 30;
  }
  if (distance <= 25) {
    //Serial.println("Stop");
    Stop();

    int leftDistance = lookLeft();
    int rightDistance =  lookRight();

    if (rightDistance <= leftDistance) {
      //left
      moveLeft();
      //Serial.println("moveLeft");
    } else {
      //right
      moveRight();
      //Serial.println("moveRight");
    }
    //delay(100);
    //} else if (val == 1) {
    //forword
    //Serial.println("moveforword");
  } else {
    moveForward();
  }
}

void charge_station() {
  if (digitalRead(irLeft) != 0) {
    boundary1 = true;
  }
  if (digitalRead(irRight) != 0) {
    boundary2 = true;
  }
  if ((digitalRead(irLeft) == 0) && (digitalRead(irRight) == 0)) {
    moveForward();
  }
  if ((digitalRead(irLeft) != 0) && (digitalRead(irRight) != 0)) {
    Stop();
  } else if (boundary1 && boundary2) {
    if (digitalRead(irLeft) != 0) {
      moveRight();
    }
    if (digitalRead(irRight) != 0) {
      moveLeft();
    }
  }
}

int lookLeft () {
  //lock left
  servo.write(150);
  delay(500);
  delay(70);
  int leftDistance = sonar.ping_cm();
  servo.write(90);
  return leftDistance;
  delay(100);
}

int lookRight() {
  //lock right
  servo.write(30);
  delay(500);
  delay(70);
  int rightDistance = sonar.ping_cm();
  servo.write(90);
  return rightDistance;
  delay(100);
}

void Stop() {
  digitalWrite(motor1pin1, LOW);
  digitalWrite(motor1pin2, LOW);

  digitalWrite(motor2pin1, LOW);
  digitalWrite(motor2pin2, LOW);
}

void moveForward() {
  digitalWrite(motor1pin1, HIGH);
  digitalWrite(motor1pin2, LOW);

  digitalWrite(motor2pin1, HIGH);
  digitalWrite(motor2pin2, LOW);
}
void moveBackward() {
  digitalWrite(motor1pin1, LOW);
  digitalWrite(motor1pin2, HIGH);

  digitalWrite(motor2pin1, LOW);
  digitalWrite(motor2pin2, HIGH);
}

void moveRight() {
  digitalWrite(motor1pin1, HIGH);
  digitalWrite(motor1pin2, LOW);

  digitalWrite(motor2pin1, LOW);
  digitalWrite(motor2pin2, HIGH);

  delay(400);
}
void moveLeft() {
  digitalWrite(motor1pin1, LOW);
  digitalWrite(motor1pin2, HIGH);

  digitalWrite(motor2pin1, HIGH);
  digitalWrite(motor2pin2, LOW);

  delay(400);
}

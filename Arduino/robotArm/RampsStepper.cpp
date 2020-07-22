#include "RampsStepper.h"
#include <Arduino.h>




RampsStepper::RampsStepper(int aStepPin, int aDirPin) {
  setReductionRatio(1, 3200);
  stepPin = aStepPin;
  dirPin = aDirPin;
  
  stepperStepPosition = 0;
  stepperStepTargetPosition;
  pinMode(stepPin, OUTPUT);
  pinMode(dirPin, OUTPUT);

}

bool RampsStepper::isOnPosition() const {
  return stepperStepPosition == stepperStepTargetPosition;
}

int RampsStepper::getPosition() const {
  return stepperStepPosition;
}

void RampsStepper::setPosition(int value) {
  stepperStepPosition = value;
  stepperStepTargetPosition = value;
}

void RampsStepper::stepToPosition(int value) {
  stepperStepTargetPosition = value;
}

void RampsStepper::stepRelative(int value) {
  value += stepperStepPosition;
  stepToPosition(value);
}

float RampsStepper::getPositionRad() const {
  return stepperStepPosition / radToStepFactor;
}

void RampsStepper::setPositionRad(float rad) {
  setPosition(rad * radToStepFactor);
}

void RampsStepper::stepToPositionRad(float rad) {
  stepperStepTargetPosition = rad * radToStepFactor;
}

void RampsStepper::stepRelativeRad(float rad) {
  stepRelative(rad * radToStepFactor);
}

void RampsStepper::update() {   
  while (stepperStepTargetPosition < stepperStepPosition) {  
    digitalWrite(dirPin, HIGH);
    delayMicroseconds(5);
    digitalWrite(stepPin, HIGH);
    delayMicroseconds(25);
    digitalWrite(stepPin, LOW);
    delayMicroseconds(5);
    stepperStepPosition--;
  }
  while (stepperStepTargetPosition > stepperStepPosition) {    
    digitalWrite(dirPin, LOW);
    delayMicroseconds(5);
    digitalWrite(stepPin, HIGH);
    delayMicroseconds(25);
    digitalWrite(stepPin, LOW);
    delayMicroseconds(5);
    stepperStepPosition++;
  }
}

void RampsStepper::setReductionRatio(float gearRatio, int stepsPerRev) {
  radToStepFactor = gearRatio * stepsPerRev / 2 / PI;
};

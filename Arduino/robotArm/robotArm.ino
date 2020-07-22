#include "pinout.h"
#include "robotGeometry.h"
#include "interpolation.h"
#include "RampsStepper.h"
#include "queue.h"
#include "command.h"


RampsStepper stepperRotate(Z_STEP_PIN, Z_DIR_PIN);
RampsStepper stepperLower(Y_STEP_PIN, Y_DIR_PIN);
RampsStepper stepperHigher(X_STEP_PIN, X_DIR_PIN);

RobotGeometry geometry;
Interpolation interpolator;
Queue<Cmd> queue(15);
Command command;


void setup() {
  Serial.begin(9600);
  
  //reduction of steppers..
  stepperHigher.setReductionRatio(32.0 / 9.0, 200 * 16);  //big gear: 32, small gear: 9, steps per rev: 200, microsteps: 16
  stepperLower.setReductionRatio( 32.0 / 9.0, 200 * 16);
  stepperRotate.setReductionRatio(32.0 / 9.0, 200 * 16);

  //start positions..
  stepperHigher.setPositionRad(PI / 2.0);  //90°
  stepperLower.setPositionRad(0);          // 0°
  stepperRotate.setPositionRad(0);         // 0°
  
  //init..
  interpolator.setInterpolation(0,19.5,134,0, 0,19.5,134,0);
  
  Serial.println("start");
}

void loop () {
  //update and Calculate all Positions, Geometry and Drive all Motors...
  interpolator.updateActualPosition();
  geometry.set(interpolator.getXPosmm(), interpolator.getYPosmm(), interpolator.getZPosmm());
  
  stepperRotate.stepToPositionRad(geometry.getRotRad());
  stepperLower.stepToPositionRad (geometry.getLowRad());
  stepperHigher.stepToPositionRad(geometry.getHighRad());

  stepperRotate.update();
  stepperLower.update();
  stepperHigher.update(); 

  
  if (!queue.isFull()) {
    //command.message="g1 x140 y0 z140"; //to send locaitons
    if (command.handleGcode()) {
      queue.push(command.getCmd());
      printOk();
    }
  }
  if ((!queue.isEmpty()) && interpolator.isFinished()) {
    executeCommand(queue.pop());
  }
    
  if (millis() %500 <250) {
    digitalWrite(LED_PIN, HIGH);
  } else {
    digitalWrite(LED_PIN, LOW);
  }
}

void cmdMove(Cmd (&cmd)) {
  interpolator.setInterpolation(cmd.valueX, cmd.valueY, cmd.valueZ, cmd.valueE, cmd.valueF);
}
void cmdDwell(Cmd (&cmd)) {
  delay(int(cmd.valueT * 800));
}

void handleAsErr(Cmd (&cmd)) {
  printComment("Unknown Cmd " + String(cmd.id) + String(cmd.num) + " (queued)"); 
  printFault();
}

void executeCommand(Cmd cmd) {
  if (cmd.id == -1) {
    String msg = "parsing Error";
    printComment(msg);
    handleAsErr(cmd);
    return;
  }
  
  if (cmd.valueX == NAN) {
    cmd.valueX = interpolator.getXPosmm();
  }
  if (cmd.valueY == NAN) {
    cmd.valueY = interpolator.getYPosmm();
  }
  if (cmd.valueZ == NAN) {
    cmd.valueZ = interpolator.getZPosmm();
  }
  if (cmd.valueE == NAN) {
    cmd.valueE = interpolator.getEPosmm();
  }
  
   //decide what to do
  if (cmd.id == 'G') {
    switch (cmd.num) {
      case 0: cmdMove(cmd); break;
      case 1: cmdMove(cmd); break;
      case 4: cmdDwell(cmd); break;
      //case 21: break; //set to mm
      //case 90: cmdToAbsolute(); break;
      //case 91: cmdToRelative(); break;
      //case 92: cmdSetPosition(cmd); break;
      default: handleAsErr(cmd); 
    }
  }
  else {
    handleAsErr(cmd); 
  }
}

from everywhereml.arduino import Sketch, Ino, H
import os

def arduino1_PID_control_uploader(arduino_script_path, com_port):
    '''
    INPUT
    -----
    arduino_script_path: real string with save path for the generated arduino script.
    com_port: string specifying the COM port of receiver arduino. 
    
    DESCRIPTION
    -----------
    Uses the everywhereml package (python wrapper for arduino CMI (command line interace) 
    to upload arduino script directly from python. This is quite useful if you have multiple experiments requiring 
    different arduino code, or are averse to using the arduino IDE. 
    
    ARDUINO SCRIPT DESCRIPTION
    --------------------------
    This script controls arduino1 during PID testing. Functionality is largely outlined by the comments below. 
    In general, arduino1 switches the mineral oil and odor pin of choice, then commands the PID collector to begin 
    collecting data from the PID via the analog input pin. 
    
    DEPENDENCIES
    ------------
    Must download and install the arduino CMI package. The folder for the generated .ino file must be located in the same folder as the 
    CMI package. 
    must install everywhere.ml package 
    script based off of this tutorial: https://eloquentarduino.com/python-arduino/
    '''
    
    
    os.chdir(arduino_script_path)
    
    # define a Sketch object 
    sketch = Sketch(name="odor_final_valve_trigger_PID")
    
    sketch += Ino('''
    int moPin = 10;  // designate the mineral oil pin ID
    int finalValvePin = 11;
    int finalValveReporter = 22;
    int odorPin = 10;
    int respPin = A3;  // specify the analog input pin for the respiration data
    int PIDpin = 2;

    void setup() {
      //set all of the pins to output mode and set the value to zero
      for (int i = 3; i < 13; i++) {
        pinMode(i, OUTPUT);
        digitalWrite(i, 0);
      }
      // set the final valve Reporter pin to zero
      digitalWrite(finalValveReporter, 0);

      // begin serial monitoring to accept input from pySerial command
      Serial.begin(9600);
    }

    void loop() {
      // continue monitoring serial port for incoming command
      if (Serial.available() > 0) {
        int odorIn = Serial.read();
        // set the odor in based on input from Python
        switch (odorIn) {
          case '1':  // vial 1 (min oil valve)
            odorPin = 10;
            break;
          case '2':  // vial 2
            odorPin = 9;
            break;
          case '3':  // vial 3
            odorPin = 8;
            break;
          case '4':  // vial 4
            odorPin = 7;
            break;
          case '5':  // vial 5
            odorPin = 6;
            break;
          case '6':  // vial 6
            odorPin = 5;
            break;
          case '7':  // vial 7
            odorPin = 4;
            break;
          case '8':  // vial 8
            odorPin = 3;
            break;
        }

        // write the PID pin to high to start collecting PID data
        digitalWrite(PIDpin, HIGH);
        Serial.println(1);

        // if the input odor is not mineral oil (>0), then switch the M.O. and designated odor pin
        if (odorPin < 10) {
          digitalWrite(moPin, 1);
          digitalWrite(odorPin, 1);  // open odor pin
          delay(4000);               //delay 4 seconds so that odor equilibrates in system
        }

        if (odorPin == 10) {
          delay(4000);
        }

        digitalWrite(finalValvePin, HIGH);
        //digitalWrite(finalValveReporter, HIGH);
        delay(1000);
        digitalWrite(finalValvePin, LOW);
        //digitalWrite(finalValveReporter, LOW);

        delay(2000);
        // after the final valve closes, set all pins to zero. This returns to M.O. open.
        for (int i = 3; i < 13; i++) {
          pinMode(i, OUTPUT);
          digitalWrite(i, 0);
        }

        // Write the PID pin to low to stop collecting PID data
        Serial.println(2);
        digitalWrite(PIDpin, LOW);
      }
    }
    '''
    )
    ##Compile sketch for Arduino Mega board.
    ##The board you target must appear in the `arduino-cli board listall` command.
    ##If you know the FQBN (Fully Qualified Board Name), you can use that too.
    if sketch.compile(board='Arduino Mega or Mega 2560').is_successful:
        print('Log', sketch.output)
        print('Sketch stats', sketch.stats)
    else:
        print('ERROR', sketch.output)

    # Upload the sketch to the correct COM port 
    sketch.upload(port= com_port)

    print(sketch.output)
    
    
def arduino2_PID_control_uploader(arduino_script_path, com_port):
    '''
    INPUT
    -----
    arduino_script_path: real string with save path for the generated arduino script.
    com_port: string specifying the COM port of receiver arduino. 
    
    DESCRIPTION
    -----------
    Uses the everywhereml package (python wrapper for arduino CMI (command line interace) 
    to upload arduino script directly from python. This is quite useful if you have multiple experiments requiring 
    different arduino code, or are averse to using the arduino IDE. 
    
    ARDUINO SCRIPT DESCRIPTION
    --------------------------
    This script controls arduino2 during PID testing. Functionality is largely outlined by the comments below. 
    In general, arduino2 waits for digital command from arduino1. Arduino1 will send a digital command for Arduino2 to start collecting data 
    from the analog input pin connected to the PID. It then relays this data over the serial port to the PID GUI. 
    
    DEPENDENCIES
    ------------
    Must download and install the arduino CMI package. The folder for the generated .ino file must be located in the same folder as the 
    CMI package. 
    must install everywhere.ml package 
    script based off of this tutorial: https://eloquentarduino.com/python-arduino/
    '''
    
    
    os.chdir(arduino_script_path)
    
    # define a Sketch object 
    sketch = Sketch(name="PID_collector")
    
    sketch += Ino('''
    int inPin = 2;  // input pin to start data collection
    int PIDinPin = A3; // analog pin to read in data from the PID 
    int val = 0;
    int PIDsignal = 0;

    void setup() {
      pinMode(inPin, INPUT);           // sets the digital pin 2 as input
    }

    void loop() {
      int start_serial = 0;
      val = digitalRead(inPin); // arduino1 will set inPin to 1 when ready to record data 
      while (val == 1){
        if (start_serial == 0){ // start serial communication with PID GUI 
          Serial.begin(9600);
          start_serial = 1;
        }
        PIDsignal = analogRead(PIDinPin); // send PID data over serial port 
        Serial.println(PIDsignal); 
        val = digitalRead(inPin);
        delay(2); 
      }
      Serial.flush();
      Serial.end(); // when finished with trial, close the serial connection
    }
    '''
    )
    ##Compile sketch for Arduino Uno board.
    ##The board you target must appear in the `arduino-cli board listall` command.
    ##If you know the FQBN (Fully Qualified Board Name), you can use that too.
    if sketch.compile(board='Arduino Uno').is_successful:
        print('Log', sketch.output)
        print('Sketch stats', sketch.stats)
    else:
        print('ERROR', sketch.output)

    # Upload the sketch to the correct COM port 
    sketch.upload(port= com_port)

    print(sketch.output)
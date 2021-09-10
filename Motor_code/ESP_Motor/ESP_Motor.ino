
/*---------------------------------------------------------------------------------------------

  File to receive OSC messages from Raspberry Pi Camera
  Then to move the motor 
  The movement of the motor moves the camera to three positions which 
  slowly oscillate over time.
  On the first iteration the slider uses the whole with of the slider.
  The width used decreases until a point and then increases again.

  Tecnique based on EG Projects approach here:
  https://www.engineersgarage.com/nodemcu-esp8266-stepper-motor-interfacing/
  
--------------------------------------------------------------------------------------------- */
#ifdef ESP8266
#include <ESP8266WiFi.h>
#else
#include <WiFi.h>
#endif
#include <WiFiUdp.h>
#include <OSCMessage.h>
#include <OSCBundle.h>
#include <OSCData.h>

/////////////////////////////////////////////////////////////////

char ssid[] = "Fefes_Wifi";                                      // your network SSID (name)
char pass[] = "*******";  

/////////////////////////////////////////////////////////////////

// A UDP instance to let us send and receive packets over UDP
WiFiUDP Udp;
const IPAddress outIp(192,168,8,126);        // remote IP (not needed for receive)
const unsigned int outPort = 8001;          // remote port to receive OSC
const unsigned int localPort = 8006;
OSCErrorCode error;

/////////////////////////////////////////////////////////////////

int esp_trigger = 0; // variable used to trigger the motor to move. 0 = no movement, 1 = movement
bool clockwise = true; // Boolean used to control whether the camera moves to the right or to the left
int Step = 0; //GPIO0---D3 of Nodemcu--Step of stepper motor driver
int Dir  = 2; //GPIO2---D4 of Nodemcu--Direction of stepper motor driver
int value = LOW;
int movementCounter=0; // used to check when to move the slider left or right
int num_steps; // stores the number of steps the camera should slide next
int distance_left; // checks how much distance is left to move so that the slider does not 'over rotate'
int overall_distance=0; // keeps a store of how far the slider has moved per set of three movements
bool firstLoop = true; // 
int lengthOfSlider = 1100; // number of steps for whole slider
int difference=lengthOfSlider/3; // difference stores the 
bool differenceSmaller=true;

/*
   In setup we initialise the serial, setup the width of the slider, 
  tell the program which pins the motor is connected on,
  set the motor to no movement, connect the ESP to wifi, and start the 
  UDP for OSC messaging
*/
void setup(){

    Serial.begin(9600); //    Initialise the serial
    distance_left = lengthOfSlider; // number of steps for whole slider
    Serial.print("num_steps =: ");
    Serial.println(num_steps);
    Serial.print("distance_left =: ");
    Serial.println(distance_left);
  
    delay(10);
    pinMode(Step, OUTPUT); //Step pin as output
    pinMode(Dir,  OUTPUT); //Direcction pin as output
    digitalWrite(Step, LOW); // Currently no stepper motor movement
    digitalWrite(Dir, LOW);  
    
    // Connect to WiFi network
    Serial.println();
    Serial.println();
    Serial.print("Connecting to ");
    Serial.println(ssid);
    WiFi.begin(ssid, pass);
  
    while (WiFi.status() != WL_CONNECTED) {
      delay(500);
      Serial.print(".");
    }
    Serial.println("");

    Serial.println("WiFi connected");
    Serial.println("IP address: ");
    Serial.println(WiFi.localIP());

    Serial.println("Starting UDP");
    Udp.begin(localPort);
    Serial.print("Local port: ");
    #ifdef ESP32
      Serial.println(localPort);
    #else
      Serial.println(Udp.localPort());
    #endif
      delay(2000);
}

/////////////////////////////////////////////////////////////////
void message(OSCMessage &msg2) {
    //////////////////
    // RECEIVE CALL TO MOVE AND CHANGE AMOUNT OF MOVEMENT EACH ITERATION
    // This function is run when a message is received to move the slider
    // The message is from the camera and is only sent when the camera has
    // finished processing the images
    
    if(difference<5){differenceSmaller=false;} // flip the direction of movement when difference is too small
    if(difference>lengthOfSlider/3){differenceSmaller=true;} // flip the direction of movement when difference is too big
      
    if(movementCounter%3==0&& firstLoop==false){ // every three movements change the direction of movement
      Serial.print("flip direction =: ");
      clockwise= !clockwise;
      if(!clockwise){
        distance_left=lengthOfSlider-distance_left;
        }
      if(clockwise){
        distance_left = lengthOfSlider - distance_left;
      }
    
    overall_distance=0;
    if(differenceSmaller){difference=difference-random(20);}
    if(differenceSmaller==false){difference=difference+random(20);}
    }

    num_steps = difference;
    Serial.print("difference is:");
    Serial.print(difference);
    
    distance_left = distance_left-num_steps;
  

    if(num_steps>distance_left){num_steps=distance_left;}

    // Print Values to Serial for testing
    Serial.print("num_steps =: ");
    Serial.println(num_steps);
    Serial.print("distance_left =: ");
    Serial.println(distance_left);
    Serial.print("movementCounter =: ");
    Serial.println(movementCounter);
    firstLoop =false;

    esp_trigger=1; // change the esp_trigger to start up the motor
}

/////////////////////////////////////////////////////////////////
void loop()
{
    /*
    CORE LOOP
    only move the motor when a message from the camera is received
    */
    if(esp_trigger==1){ 
      overall_distance=overall_distance+num_steps; // add the new number of steps to the overall distance moved 
      Serial.print("Overall Distance Travelled =: ");
      Serial.println(overall_distance); //print distance moved for testing

      // move stepper clockwise or anticlockwise
        if (clockwise){
            digitalWrite(Dir, HIGH); //Rotate stepper motor in clock wise direction
          for(int i=1;i<=num_steps;i++){
              digitalWrite(Step, HIGH);
              delay(10);
              digitalWrite(Step, LOW);
              delay(10);
            }
          value = HIGH;
          }
         if(!clockwise){
            digitalWrite(Dir, LOW); //Rotate stepper motor in anti clock wise direction
            for(int i=1;i<=num_steps;i++){
                digitalWrite(Step, HIGH);
                delay(10);
                digitalWrite(Step, LOW);
                delay(10);
              }
             value = LOW;
          }
         
        // send message back to camera to say movement is completed
        OSCMessage msg("/return_to_camera");
        msg.add(esp_trigger);
        Udp.beginPacket(outIp, outPort);
        msg.send(Udp);
        Udp.endPacket();
        msg.empty();
        
        esp_trigger=0; // stop the movement until a new OSC message is received
        movementCounter=movementCounter+1; // keep track of how many movements have been completed
      }

      // listen for OSC messages
      OSCMessage msg2;
      int size = Udp.parsePacket();
      if(size>0){
        Serial.print("triggered ");
          while (size--) {
            msg2.fill(Udp.read());
          }
          if (!msg2.hasError()) {
            msg2.dispatch("/move_me/", message);
          } else {
            error = msg2.getError();
            Serial.print("error: ");
          }
       }


}
///////////////////////////////////////////////////////////////////

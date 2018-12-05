//Program connects to a serial port, reads sequentially sent color data, and outputs
//  it to a pair of neopixel LED strips.  The setup lokks something like this:
//
//       Left Strip                       Right Strip
//···O═O═O═O═O═O═O═O═O═O═O═O═O═O═O═╦═O═O═O═O═O═O═O═O═O═O═O═O═O═O═O···
//                               ║
//                           ┌╌╌╌╨╌╌╌┐
//                           ┊Arduino┊
//                           └╌╌╌╌╌╌╌┘
//
//Author: Ryan Slater and Owen O'Connor
//Date: 6 October 2018

//This code has been tested on an Arduino Uno with up to 150 neopixels per strip. YMMV

#include <Adafruit_NeoPixel.h>

#define PIN0 5
#define PIN1 3
#define PIXELS_PER_STRIP 150

//Create the two strips
//Left strip
Adafruit_NeoPixel strip1 = Adafruit_NeoPixel(PIXELS_PER_STRIP, PIN1, NEO_GRB + NEO_KHZ800);

//Right strip
Adafruit_NeoPixel strip0 = Adafruit_NeoPixel(PIXELS_PER_STRIP, PIN0, NEO_GRB + NEO_KHZ800);

//The arduino doesn't have enough memeory to store all of the caolor data at a time,
//  so it has to read one byte at a time, and write to one pixel at a time
//These variable provide stately information for this process
short currentPxl = 0;
byte currentChnl = 0,
    r = 0,
    g = 0,
    b = 0;



void setup() {
  pinMode(13, OUTPUT);
  digitalWrite(13, HIGH);

  //Set the strips up, and clear them...
  strip0.begin();
  strip1.begin();
  strip0.show();
  strip1.show();

//uncomment to flash the strips white -> red/blue -> white
//  for (int i = 0; i < 300; i++) {
//    outputColor(i, 100, 100, 100);
//  }
//
//  updateStrips();
//  delay(500);
//
//  for (int i = 0; i < 300; i++) {
//    outputColor(i, i < 150 ? 100 : 0, 0, i < 150 ? 0 : 100);
//  }
//
//  updateStrips();
//  delay(500);
//
//  for (int i = 0; i < 300; i++) {
//    outputColor(i, 100, 100, 100);
//  }
//
//  updateStrips();
//  delay(500);

  //Once all initialization is done, open the serial port.
  Serial.begin(115200);  //Gotta go fast!
}



void loop() {
  //If there is a byte of data availble from the serial port,
  // read it into the corresponding channel color variable
  if(Serial.available() != 0) {

    //Read red
    if(currentChnl == 0) {
      r = Serial.read() * 2;
      currentChnl++;
    }

    //Read green
    else if(currentChnl == 1) {
      g = Serial.read() * 2;
      currentChnl++;
    }

    //Read blue
    else if(currentChnl == 2) {
      b = Serial.read() * 2;
      currentChnl = 0;

      //Since the blue pixel was just read, all of the colors channels are now set,
      //  so push them to the current pixel on the LED strips
      outputColor(currentPxl, r, g, b);

      //go to the next pixel
      currentPxl++;

      //If we have reached the end of the strips, wrap around to the beginning
      if(currentPxl >= PIXELS_PER_STRIP * 2) {
        currentPxl = 0;
        updateStrips();
      }
    }
  }
}



//Function to push a specified color to the speciefied pixel along on strips
//Note that in order for the new color to be displayed, updateStrips() must be called
void outputColor(int pxl, byte r, byte g, byte b) {
  //If writing to the left strip, the pixel indexes are flipped, so correct for that
  if (pxl < PIXELS_PER_STRIP) {
    strip0.setPixelColor(PIXELS_PER_STRIP - (pxl + 1), r, g, b);
  }

  //If writing to the right strip, the pixel indexes are offset, so correct for that
  else {
    strip1.setPixelColor(pxl - PIXELS_PER_STRIP, r, g, b);
  }
}



//Function to tell the strips to update.
//Shocking, right?
void updateStrips() {
  strip0.show();
  strip1.show();
}

//-☃, the Unicode Snowman

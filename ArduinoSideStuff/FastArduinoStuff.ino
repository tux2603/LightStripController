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

#include <FastLED.h>

// How many leds in your strip?
#define PIXELS_PER_STRIP 150

// For led chips like Neopixels, which have a data line, ground, and power, you just
// need to define DATA_PIN.  For led chipsets that are SPI based (four wires - data, clock,
// ground, and power), like the LPD8806 define both DATA_PIN and CLOCK_PIN
#define LEFT_DATA_PIN 5
#define RIGHT_DATA_PIN 3

// Define the array of leds
CRGB left_leds[PIXELS_PER_STRIP];
CRGB right_leds[PIXELS_PER_STRIP];

short currentPxl = 0;
uint8_t currentChnl = 0,
    r = 0,
    g = 0,
    b = 0;

void setup() {
  	  FastLED.addLeds<NEOPIXEL, LEFT_DATA_PIN>(left_leds, PIXELS_PER_STRIP);
  	  FastLED.addLeds<NEOPIXEL, RIGHT_DATA_PIN>(right_leds, PIXELS_PER_STRIP);
      Serial.begin(115200);
}

void loop() {
  // Now turn the LED off, then pause
  // for(int i = 0; i < NUM_LEDS; i++) { leds2[i] = CRGB::Black; leds1[i] = CRGB::Black; }
  // FastLED.show();
  //
  // for(int j = 1; j < NUM_LEDS; j++) {
  //   // Turn the LED on, then pause
  //   leds1[j] = CRGB::White; leds2[j] = CRGB::White;
  //   leds1[j-1] = CRGB::Black; leds2[j-1] = CRGB::Black;
  //   FastLED.show();
  // }

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
      if (currentPxl < PIXELS_PER_STRIP) {
        left_leds[PIXELS_PER_STRIP - (currentPxl + 1)] = CRGB(r, g, b);
      }

      //If writing to the right strip, the pixel indexes are offset, so correct for that
      else {
        right_leds[currentPxl - PIXELS_PER_STRIP] = CRGB(r, g, b);
      }

      //go to the next pixel
      currentPxl++;

      //If we have reached the end of the strips, wrap around to the beginning
      if(currentPxl >= PIXELS_PER_STRIP * 2) {
        currentPxl = 0;
        FastLED.show();
      }
    }
  }
}

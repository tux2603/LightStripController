#include <FastLED.h>

#define NUM_PIXELS 450
#define BUFFER_SIZE 5
#define PIN 3

// Define the array of leds
CRGB leds[NUM_PIXELS];
uint8_t buffer[BUFFER_SIZE];  // addr, addr, r, g, b

uint16_t current_pixel = 0;
uint8_t r = 0,
        g = 0,
        b = 0;

void setup() {
  FastLED.addLeds<NEOPIXEL, PIN>(leds, NUM_PIXELS);
  Serial.begin(9600);
}

void loop() {
  if (Serial.available() != 0) {
    Serial.readBytes(buffer, BUFFER_SIZE);
    current_pixel = *(uint16_t *)buffer;
    r = buffer[2];
    g = buffer[3];
    b = buffer[4];

    leds[current_pixel] = CRGB(r, g, b);

    // TODO Send sync message when done writing
    if (current_pixel == NUM_PIXELS - 1)
      FastLED.show();
  }
}

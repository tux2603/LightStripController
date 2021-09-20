#include <FastLED.h>

#define NUM_PIXELS 450
#define PIN 3

// Define the array of leds
CRGB leds[NUM_PIXELS];

uint16_t current_pixel = 0;
uint8_t current_channel = 0,
        r = 0,
        g = 0,
        b = 0;

void setup() {
    FastLED.addLeds<NEOPIXEL, PIN>(leds, NUM_PIXELS);
    Serial.begin(9600);
}

uint

void loop() {
    if (Serial.available() != 0) {

        // Read red
        if (current_channel == 0) {
            r = Serial.read() * 2;
            current_channel++;
        }

        // Read green
        else if (current_channel == 1) {
            g = Serial.read() * 2;
            current_channel++;
        }

        // Read blue
        else if (current_channel == 2) {
            b = Serial.read() * 2;
            current_channel = 0;

            // Since the blue pixel was just read, all of the colors channels are now set,
            // so push them to the current pixel on the LED strips
            leds[current_pixel] = CRGB(r, g, b);

            // Go to the next pixel
            current_pixel++;

            // If we have reached the end of the strips, wrap around to the beginning
            if (current_pixel >= NUM_PIXELS) {
                current_pixel = 0;
                FastLED.show();
            }
        }
    }
}

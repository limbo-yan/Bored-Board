#include <Adafruit_NeoPixel.h>
#ifdef __AVR__
#include <avr/power.h> // Required for 16 MHz Adafruit Trinket
#endif

#define PIN  6
#define NUMPIXELS 8

Adafruit_NeoPixel pixels(NUMPIXELS, PIN, NEO_GRB + NEO_KHZ800);

#define DELAYVAL 500 // Time (in milliseconds) to pause between pixels

int col[] = {0, 1, 2};
int row[] = {3, 4, 5};


void setup() {
 for (int i = 0; i < sizeof(col) / sizeof(col[0]); i ++) {
  pinMode(col[i], INPUT);
 }
 for (int i = 0; i < sizeof(row) / sizeof(row[0]); i ++) {
  pinMode(row[i], OUTPUT);
 }
 pixels.begin(); 
 pixels.clear();
 pixels.show();
}

void loop() {
  for (int i = 0; i < sizeof(row) / sizeof(row[0]); i ++) {
    digitalWrite(row[i], LOW);
    for (int j = 0; j < sizeof(col) / sizeof(col[0]); j ++) {
      int buttonState = digitalRead(col[j]);
      int pixelIdx = i * 3 + j;
      if (buttonState == LOW) {
        pixels.setPixelColor(pixelIdx, pixels.Color(0, 150, 0));
        pixels.show();
      } else {
        pixels.setPixelColor(pixelIdx, pixels.Color(150, 0, 0));
        pixels.show();
      }
  }
  digitalWrite(row[i], HIGH);
  }
}
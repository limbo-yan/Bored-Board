#include <Adafruit_NeoPixel.h>
#ifdef __AVR__
#endif

#define PIN  6
#define NUMPIXELS 8

Adafruit_NeoPixel pixels(NUMPIXELS, PIN, NEO_GRB + NEO_KHZ800);

// Pins for rows and cols of switches
int col[] = {0, 1, 2};
int row[] = {3, 4, 5};

int rowSize = sizeof(row) / sizeof(row[0]);
int colSize = sizeof(col) / sizeof(col[0]);

void setup() {
  // Set all columns as input
  for (int i = 0; i < colSize; i ++) {
    pinMode(col[i], INPUT);
  }
  // Set all rows as output
  for (int i = 0; i < rowSize; i ++) {
    pinMode(row[i], OUTPUT);
  }

  pixels.begin(); 
  pixels.clear();
  pixels.show();
}

void loop() {
  for (int i = 0; i < rowSize; i ++) {
    // For each iteration, set each row as LOW first
    digitalWrite(row[i], LOW);
    for (int j = 0; j < colSize; j ++) {
      // Read every column's pin to check if the switch is pressed or not
      int buttonState = digitalRead(col[j]);
      // Convert the switch location to LED's location
      int pixelIdx = i * rowSize + j;
      if (buttonState == LOW) {
        // Light up the specific LED when the switch is pressed
        if(pixels.getPixelColor(pixelIdx) == 0x000000) {
          pixels.setPixelColor(pixelIdx, pixels.Color(0, 150, 0));
        }
      }
      pixels.show();
    }
    // Set this row as HIGH and continue to check another row
    digitalWrite(row[i], HIGH);
  }
}
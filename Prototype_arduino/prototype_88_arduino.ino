#include <Adafruit_NeoPixel.h>
#ifdef __AVR__
#endif

#define LOWIN 0
#define DETECTPIN 4 
#define PIN  9
#define NUMPIXELS 24

Adafruit_NeoPixel pixels(NUMPIXELS, PIN, NEO_GRB + NEO_KHZ800);

// Pins for rows and cols of switches
int col[] = {5, 6, 7};
int row[] = {1, 2, 3};

int rowSize = sizeof(row) / sizeof(row[0]);
int colSize = sizeof(col) / sizeof(col[0]);

void setup() {
  for (int i = 0; i < colSize; i ++) {
    pinMode(col[i], OUTPUT);
  }
  pinMode(LOWIN, OUTPUT);
  digitalWrite(LOWIN, LOW);

  for (int i = 0; i < rowSize; i ++) {
    pinMode(row[i], OUTPUT);
  }
  pinMode(DETECTPIN, INPUT);

  pixels.begin(); 
  pixels.clear();
  pixels.show();
}

void loop() {
  for (int rowNum = 0; rowNum < 8; rowNum ++) {
    int tempRowNum = rowNum;
    // Set specific row pins
    for (int i = 0; i < rowSize; i ++) {
      digitalWrite(row[i], tempRowNum % 2);
      tempRowNum /= 2;
    }
   
    for (int colNum = 0; colNum < 8; colNum ++) {
      int tempColNum = colNum;
      for (int j = 0; j < colSize; j ++) {
        digitalWrite(col[j], tempColNum % 2);
        tempColNum /= 2;
      }
     
      if (digitalRead(DETECTPIN) == LOW) {
        // Convert the switch location to LED's location
        int pixelIdx = 8 * rowNum + colNum;
        if (rowNum == 1) {
          pixelIdx = 8 + (7 - colNum);
        }

        // Light up the specific LED when the switch is pressed
        if(pixels.getPixelColor(pixelIdx) == 0x000000) {
          pixels.setPixelColor(pixelIdx, pixels.Color(0, 150, 0));
        }
        pixels.show();
      }
    }
  }
}
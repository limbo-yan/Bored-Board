#include <Adafruit_NeoPixel.h>
#ifdef __AVR__
#endif

#define LOWIN 8
#define DETECTPIN 10 
#define PIN  9
#define NUMPIXELS 64

Adafruit_NeoPixel pixels(NUMPIXELS, PIN, NEO_GRB + NEO_KHZ800);

// Pins for rows and cols of switches
int col[] = {5, 6, 7};
int row[] = {4, 3, 2};

int rowSize = sizeof(row) / sizeof(row[0]);
int colSize = sizeof(col) / sizeof(col[0]);

int player = 1;
int PvC = 0;

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

  Serial.begin(115200);
  Serial.setTimeout(1);
}

void light(int rowNum, int colNum, int p) {
  int pixelIdx = 8 * rowNum + colNum;

  // Light up the specific LED when the switch is pressed
  if(pixels.getPixelColor(pixelIdx) == 0x000000) {
    if (p == 1) {
      pixels.setPixelColor(pixelIdx, pixels.Color(0, 150, 0));
    } else if (p == 2){
      pixels.setPixelColor(pixelIdx, pixels.Color(0, 0, 150));
    } else {
      pixels.setPixelColor(pixelIdx, pixels.Color(150, 0, 0));
    }
    pixels.show();
    if (rowNum % 2 == 1) {
      colNum = 7 - colNum;
    }

    if (PvC == 0) {
      if (p == 1) player = 2;
      else if (p == 2) player = 1;
    }

    Serial.print(rowNum);
    Serial.print(",");
    Serial.print(colNum);
  }
}

void loop() {
  if (Serial.available() > 0) {
    String str = Serial.readString();

    if (str == "end") {
      pixels.clear();
      pixels.show();
    }

    int rowNumAI = str.charAt(0) - '0';
    int colNumAI = str.charAt(1) - '0';

    if (rowNumAI % 2 == 1) {
      colNumAI = 7 - colNumAI;
    }
    
    light(rowNumAI, colNumAI, 3);
  }
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
        if (rowNum % 2 == 1) {
          colNum = 7 - colNum;
        }
        
        light(rowNum, colNum, player);
      }
    }
  }
}
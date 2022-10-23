int bRow[] = {0, 1, 2};
int bCol[] = {3, 4, 5};

int ledRow[] = {9, 10, 11};
int ledCol[] = {6, 7, 8};

void setup() {
  // put your setup code here, to run once:
  for (int i = 0; i < sizeof(bRow) / sizeof(bRow[0]); i ++) {
    pinMode(bRow[i], INPUT);
  }

  for (int i = 0; i < sizeof(bCol) / sizeof(bCol[0]); i ++) {
    pinMode(bCol[i], OUTPUT);
  }

  for (int i = 0; i < sizeof(ledRow) / sizeof(ledRow[0]); i ++) {
    pinMode(ledRow[i], OUTPUT);
    digitalWrite(ledRow[i], HIGH);
  }
  
  for (int i = 0; i < sizeof(ledCol) / sizeof(ledCol[0]); i ++) {
    pinMode(ledCol[i], OUTPUT);
  }

}

void loop() {
  for (int i = 0; i < sizeof(bCol) / sizeof(bCol[0]); i ++) {
    digitalWrite(bCol[i], LOW);
    for (int j = 0; j < 3; j ++) {
      int buttonState = digitalRead(bRow[j]);
      if (buttonState == LOW) {
        digitalWrite(ledRow[i], LOW);
        digitalWrite(ledCol[j], HIGH);
      } else {
        digitalWrite(ledRow[i], HIGH);
        digitalWrite(ledCol[j], LOW);
      }
    }
    digitalWrite(bCol[i], HIGH);
  }
}

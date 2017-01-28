#include <stdlib.h> // for malloc and free
#include <OctoWS2811.h>

const int ledsPerStrip = 28 * 4; //total 28*28// 7 strips

DMAMEM int displayMemory[ledsPerStrip * 6];
int drawingMemory[ledsPerStrip * 6];

const int config = WS2811_GRB | WS2811_800kHz;

OctoWS2811 leds(ledsPerStrip, displayMemory, drawingMemory, config);

void setup() {
  Serial.begin(9600);
  leds.begin();
  leds.show();
}

byte incomingFrameSequence = 200;
short currentmode = 0;//0 - Waiting for first seqbyte, 1 - Waiting for first lengthbyte, 2 - Waiting for second lengthbyte, 3 - Waiting for modebyte, 4 - Receiving Frame
short transmissionLength[2];
int frameLength;
int currentFrameLength = 0;
short frameType;
byte * frame;
void loop() {
  byte incomingByte;
  if (Serial.available() > 0) {
    incomingByte = Serial.read();
    if (currentmode == 0 and incomingFrameSequence == incomingByte) {
      Serial.println("rcvnew");
      currentmode = 1;
    } else if (currentmode == 1) {
      transmissionLength[0] = incomingByte;
      currentmode = 2;
    } else if (currentmode == 2) {
      transmissionLength[1] = incomingByte;
      frameLength = (transmissionLength[0] * 255) + transmissionLength[1];
      Serial.println("rcvlen" + String(frameLength));
      currentFrameLength = 0;
      currentmode = 3;
    } else if (currentmode == 3) {
      frameType = incomingByte;
      currentmode = 4;
      Serial.println("rcvtype" + String(frameType));
    } else if (currentmode == 4) {
      if (currentFrameLength <= (frameLength - 1)) {
        if (frameType == 0) {
          if (currentFrameLength == 0) {
            free(frame);
            frame = (byte*) calloc(frameLength, sizeof (byte));
          }
          frame[currentFrameLength] = incomingByte;
        }
        currentFrameLength = currentFrameLength + 1;
        if (currentFrameLength >= frameLength){
          renderTypeZero();
          currentmode = 0;
        }
      }
    }
  }
}
void renderTypeZero() {
  int allpixels = leds.numPixels();
  if (frameLength % 3 == 0) {
    int innerLength = frameLength / 3;
    Serial.println("0rnd");
    for (int i = 0; i < (frameLength / 3); i++) {
      if (i < allpixels) {
        long color = (frame[i] << 16) | (frame[i + innerLength] << 8) | frame[i + innerLength*2];
        Serial.println("R:" + String(frame[i]) + " G:" + String(frame[i + innerLength]) + " B:" + String(frame[i + innerLength*2]));
        Serial.println(color, HEX);
        leds.setPixel(i, color);
      }
    }
    Serial.println("0rndshow");
    leds.show();
  }else{
    Serial.println("0rndfaildivby3");
  }
  currentmode = 0;
}


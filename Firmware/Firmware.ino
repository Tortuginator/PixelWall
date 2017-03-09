#include <stdlib.h> // for malloc and free
#include <OctoWS2811.h>



//Configuration
const int SerialBaudrate = 100000;
const int Vlength = 28; // The vertival amount of lED's
const int Hlength = 28; // The Horizontal amount of LED's
const int Hbegin = 1;//where the initial strip beginns: Left -> 0, Right -> 1
const int VrowsperStrip = 4; // How many rows are there per strip

//Static Configuration
const int ledsPerStrip = Hlength * VrowsperStrip; //total 28*28// 7 strips
DMAMEM int displayMemory[ledsPerStrip * 6];
int drawingMemory[ledsPerStrip * 6];
const int config = WS2811_GRB | WS2811_800kHz;
OctoWS2811 leds(ledsPerStrip, displayMemory, drawingMemory, config);


//Code
void setup() {
  Serial.begin(100000);
  leds.begin();
  leds.show();
}

//DecompressionConfiguration
byte incomingFrameSequence = 200;

//Static Configuration/Init
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
void renderTypeThree(){//RFCA compression V1.0
  char SkipSignal = 0;
  int lengthRGB[3];
  lengthRGB[0] = frame[1] * 255 + frame[2];
  lengthRGB[1] = frame[3] * 255 + frame[4];
  lengthRGB[2] = frame[5] * 255 + frame[6];

  int counter = 7;
  for (int p = 0; i < 3;p++){
    int locmax = lengthRGB[p] + counter;
    int index = 0;
    while (index <= locmax){
      if (frame[counter] == SkipSignal){
        index += frame[counter+1];
        counter +=2;
      }else{
        short pixelpos = nbrPixelbyPosition(index);
        long number = leds.getPixel(pixelpos);
        long r = number >> 16;
        long g = number >> 8 & 0xFF;
        long b = number & 0xFF;
        long color = (r << 16) | (g << 8) | b;
        leds.setPixel(pixelpos,color);
        index +=1;
        counter +=1;
      }
    }
  }
  leds.show();
}
void renderTypeZero() {
  int allpixels = leds.numPixels();
  if (frameLength % 3 == 0) {
    int innerLength = frameLength / 3;
    Serial.println("0rnd");
    for (int i = 0; i < (frameLength / 3); i++) {
      if (i < allpixels) {
<<<<<<< HEAD
        long color = (frame[i] << 16) | (frame[i + innerLength] << 8) | frame[i + innerLength*2];
        Serial.println("R:" + String(frame[i]) + " G:" + String(frame[i + innerLength]) + " B:" + String(frame[i + innerLength*2]));
        Serial.println(color, HEX);
=======
        long color = ((long)frame[i] << 16) | ((long)frame[i + innerLength] << 8) | (long)frame[i + innerLength*2];
        //Serial.println("R:" + String(frame[i]) + " G:" + String(frame[i + innerLength]) + " B:" + String(frame[i + innerLength*2]));
        //Serial.println(color, HEX);
>>>>>>> origin/master
        leds.setPixel(i, color);
        //setPixelbyPosition(i,color);
      }
    }
    Serial.println("0rndshow");
    leds.show();
  }else{
    Serial.println("0rndfaildivby3");
  }
  currentmode = 0;
}

//Various Functions
int nbrPixelbyPosition(int position){
  int iY = position / Hlength;
  int iX = position % Hlength;
  return setPixelbyCoordinate(iX,iY);
}
int nbrPixelbyCoordinate(int X,int Y){
  bool inverse = false;
  if (Y/2 == 1){//Uneven number
    if (Hbegin == 0){
      inverse = true;
    }else{
      inverse = false;
    }
  }else{
    if (Hbegin == 0){
      inverse = false;
    }else{
      inverse = true;
    }
  }
  int position = Y * Hlength;
  if (inverse == true){
    position += Hlength-X;
  }else{
    position += X;
  }

  //setcolor
  return position;
}

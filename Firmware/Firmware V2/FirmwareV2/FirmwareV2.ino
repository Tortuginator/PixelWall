#include <OctoWS2811.h>

//Configuration
const int SerialBaudrate = 1000000;
const int Vlength = 28; // The vertival amount of lED's
const int Hlength = 28; // The Horizontal amount of LED's
const int Hbegin = 0;//where the initial strip beginns: Left -> 0, Right -> 1
const int VrowsperStrip = 4; // How many rows are there per strip

const bool Debug = true;
//Static Configuration
const int ledsPerStrip = Hlength * VrowsperStrip; //total 28*28// 7 strips
DMAMEM int displayMemory[ledsPerStrip * 6];
int drawingMemory[ledsPerStrip * 6];
const int config = WS2811_GRB | WS2811_800kHz;
OctoWS2811 leds(ledsPerStrip, displayMemory, drawingMemory, config);
char buffer [Vlength * Hlength * 3 + 20];//+20 should be sufficient to over the overhead
char rfbuffer [Vlength * Hlength * 3 + 20];
unsigned int Color(byte r, byte g, byte b)
{
  return (((unsigned int)r << 16) | ((unsigned int)g << 8) | (unsigned int)b);
}
//Code
void setup() {
  Serial.begin(SerialBaudrate);
  pinMode(13, OUTPUT);
  leds.begin();
  leds.show();
}

//DecompressionConfiguration
const byte incomingSequenceFlag = 200; // or char
int breakcount = 0;
void loop() {
  short inner = 0;
  int bufferLength = 0;
  int bufferPosition = 0;
  int bufferLengthSTOR; //for the temporary calculation of the buffer length
  
  //frame configuration
  short frameType = 0;
  short currentFlag = 0;

  byte incomingByte;
  while (true) {
    breakcount += 1;
    if (breakcount > 10000 and bufferLength > 0) {
      Serial.println("RCVmissing");
      breakcount = 0;
    }
    if (Serial.available() > 0) {
      incomingByte = Serial.read();
      breakcount = 0;
    } else {
      break;
    }
    if (currentFlag == 0 and incomingSequenceFlag == incomingByte) {
      if (Debug == true) {
        Serial.println("RCVnew");
      }
      currentFlag = 1;
    } else if (currentFlag == 1) {
      bufferLengthSTOR = incomingByte;
      currentFlag = 2;

    } else if (currentFlag == 2) {
      bufferLength = (bufferLengthSTOR * 255) + incomingByte;
      if (Debug == true) {
        Serial.println("RVClen" + String(bufferLength));
      }
      bufferPosition = 0;
      currentFlag = 3;

    } else if (currentFlag == 3) {
      frameType = incomingByte;
      currentFlag = 4;
      if (Debug == true) {
        Serial.println("RCVType");
      }
    } else if (currentFlag == 4) {
      buffer[bufferPosition] = incomingByte;
      bufferPosition += 1;
      if (bufferPosition == bufferLength) {
        Serial.println("RNDcomplete");// Incase of faulty transmission, the data will be ignored and a new set will be send.
        drawFrameFromBuffer(frameType, bufferLength);
        currentFlag = 0;
      }
    }
  }
}


void renderTypeThree(int bufferLength) { //RFCA compression V1.0; ONLY RFCA V2.0
  char SkipSignal = 1;
  int lengthRGB[3];
  lengthRGB[0] = buffer[0] * 255 + buffer[1];
  lengthRGB[1] = buffer[2] * 255 + buffer[3];
  lengthRGB[2] = buffer[4] * 255 + buffer[5];

  int index, locmax, counter;
  unsigned int r, g, b, number;
  short pixelpos;

  bufferLength = bufferLength - 3;

  counter = 6;
  if (bufferLength != (lengthRGB[0] + lengthRGB[1] + lengthRGB[2] + 6)) {
    if (Debug == true) {
      Serial.println("RNDdiffLength");
    }
    return;
  }
  locmax = counter;
  for (int p = 0; p < 3; p++) {
    int pSize = Vlength * Hlength;
    index = 0;
    locmax += lengthRGB[p];
    while (counter < locmax) {
      if (buffer[counter] == SkipSignal) {
        index += buffer[counter + 1]; //the index in the pixel array, meaning the position of the pixel. Therefore since it is the RFCA v1. this is not the same as the counter index!
        counter += 2; //the index in the buffer array
      } else {
        pixelpos = nbrPixelbyPosition(index);
        rfbuffer[pSize * p + pixelpos] = buffer[counter];
        leds.setPixel(pixelpos, Color(rfbuffer[pixelpos], rfbuffer[pSize * 1 + pixelpos], rfbuffer[pSize * 2 + pixelpos]));
        index += 1;
        counter += 1;
      }
    }
  }
  leds.show();
}
void renderTypeZero(int bufferLength) {
  int allpixels = Vlength * Hlength;
  long color;
  int pixelpos;
  bufferLength = bufferLength - 3;
  int innerLength = bufferLength;//determine length of the array
  if (innerLength % 3 == 0) {
    if (Debug == true) {
      Serial.println("0RNDinit");
    }
    for (int i = 0; i <= ((innerLength / 3) - 1); i++) {
      if (i <= allpixels) {
        color = Color(buffer[i], buffer[i + (innerLength / 3)], buffer[i + ((innerLength / 3) * 2)]);
        pixelpos = nbrPixelbyPosition(i);
        leds.setPixel(pixelpos, color);
      }
    }
    leds.show();
  } else {
    if (Debug == true) {
      Serial.println("0RNDfaildivby3");
    }
  }
}

//Various Functions
int nbrPixelbyPosition(int position) {
  int iY = position / Hlength;
  int iX = position % Hlength;
  return nbrPixelbyCoordinate(iX, iY);
}
int nbrPixelbyCoordinate(int X, int Y) {
  bool inverse = false;
  if (Y % 2 == 1) { //Uneven number
    if (Hbegin == 0) {
      inverse = true;
    } else {
      inverse = false;
    }
  } else {
    if (Hbegin == 0) {
      inverse = false;
    } else {
      inverse = true;
    }
  }
  int position = Y * Hlength;
  if (inverse == true) {
    position += Hlength - (X + 1);
  } else {
    position += X;
  }
  return position;
}
short on = 0;
void rndswitch() {
  if (on == 1) {
    digitalWrite(13, HIGH);
    on = 0;
  } else {
    digitalWrite(13, LOW);
    on = 1;
  }
}

void drawFrameFromBuffer(short frameType, int bufferLength) {
  rndswitch();
  if (Debug == true) {
    Serial.println("DFFBtype" + String(frameType));
  }
  if (frameType == 0) {
    renderTypeZero(bufferLength);
  } else if (frameType == 2) {
    if (Debug == true) {
      Serial.println("DFFB2notsupp");
    }
  } else if (frameType == 100) {
    renderTypeThree(bufferLength);
  } else {
    if (Debug == true) {
      Serial.println("DFFBfrtyNotFound");
    }
  }
}

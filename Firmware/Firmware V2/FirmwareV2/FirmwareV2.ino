#include <OctoWS2811.h>

//Configuration
const int SerialBaudrate = 1000000;
const int Vlength = 28; // The vertival amount of lED's
const int Hlength = 28; // The Horizontal amount of LED's
const int Hbegin = 1;//where the initial strip beginns: Left -> 0, Right -> 1
const int VrowsperStrip = 4; // How many rows are there per strip

const bool Debug = true;
//Static Configuration
const int ledsPerStrip = Hlength * VrowsperStrip; //total 28*28// 7 strips
DMAMEM int displayMemory[ledsPerStrip * 6];
int drawingMemory[ledsPerStrip * 6];
const int config = WS2811_GRB | WS2811_800kHz;
OctoWS2811 leds(ledsPerStrip, displayMemory, drawingMemory, config);
char buffer [Vlength*Hlength*3+20];

unsigned int Color(byte r, byte g, byte b)
{
  return (((unsigned int)r << 16) | ((unsigned int)g << 8) | (unsigned int)g);
}

//Code
void setup() {
  Serial.begin(1000000);
  leds.begin();
  leds.show();
}

//DecompressionConfiguration
const byte incomingSequenceFlag = 200; // or char
void loop(){
  short inner = 0;
	int bufferLength = 0;
	int bufferPosition = 0;
	int bufferLengthSTOR; //for the temporary calculation of the buffer length
	//frame configuration
	short frameType = 0;
  short currentFlag = 0;
  
	byte incomingByte;
	while (1==1){
		if (Serial.available() > 0) {
			incomingByte = Serial.read();
		}else{
			break;//skip iteration
		}

		if (currentFlag == 0 and incomingSequenceFlag == incomingByte){
			if (Debug == true){Serial.println("rcvnew");}
			currentFlag = 1;

		}else if (currentFlag == 1){
			bufferLengthSTOR = incomingByte;
			currentFlag = 2;

		}else if(currentFlag == 2){
			bufferLength = (bufferLengthSTOR * 255) + incomingByte;
			if (Debug == true){Serial.println("rcvlen" + String(bufferLength));}
			bufferPosition = 0;
			currentFlag = 3;
      
		}else if (currentFlag == 3){
			frameType = incomingByte;
			currentFlag = 4;

		}else if (currentFlag == 4){
			buffer[bufferPosition] = incomingByte;
			bufferPosition +=1;
			if (bufferPosition == bufferLength){
				drawFrameFromBuffer(frameType,bufferLength);
				currentFlag = 0;
			}
    }
	}
}


void renderTypeThree(int bufferLength){//RFCA compression V1.0 -->THIS DOES NOT WORK FOR RFCA v2 [EXPERIMENTAL]<--
  char SkipSignal = 1;
  int lengthRGB[3];
  lengthRGB[0] = buffer[0] * 255 + buffer[1];
  lengthRGB[1] = buffer[2] * 255 + buffer[3];
  lengthRGB[2] = buffer[4] * 255 + buffer[5];

  int index,locmax,counter;
  unsigned int r,g,b,number;
  short pixelpos;

  counter = 6;
  if (bufferLength != (lengthRGB[0] + lengthRGB[1] + lengthRGB[2] + 6)){
    if (Debug == true){Serial.println("3fail");}
    return;
  }
  for (int p = 0; p < 3;p++){
    locmax = lengthRGB[p] + counter;
    index = 0;
    while (index < locmax){
      if (buffer[counter] == SkipSignal){
        index += buffer[counter+1];//the index in the pixel array, meaning the position of the pixel. Therefore since it is the RFCA v1. this is not the same as the counter index!
        counter +=2;//the index in the buffer array
      }else{
        pixelpos = nbrPixelbyPosition(index);
        number = leds.getPixel(pixelpos);
        r = number >> 16;
        g = number >> 8 & 0xFF;
        b = number & 0xFF;
        if (p == 0){r = buffer[counter];}
        if (p == 1){g = buffer[counter];}
        if (p == 2){b = buffer[counter];}
        leds.setPixel(pixelpos,Color(r,g,b));
        index +=1;
        counter +=1;
      }
    }
  }
  leds.show();
}
void renderTypeZero(int bufferLength) {
  int allpixels = leds.numPixels();
  long color;
  int pixelpos;
  int innerLength = bufferLength;//determine length of the array
  if (innerLength % 3 == 0) {
    if (Debug == true){Serial.println("0rnd");}
    for (int i = 0; i < (innerLength/3); i++) {
      if (i < allpixels) {
        color = Color(buffer[i],buffer[i + (innerLength/3)],buffer[i + (innerLength/3)*2]);
        pixelpos = nbrPixelbyPosition(i);
        leds.setPixel(pixelpos, color);
      }
    }
    if (Debug == true){Serial.println("0rndshow");}
    leds.show();
  }else{
    if (Debug == true){Serial.println("0rndfaildivby3");}
  }
}

//Various Functions
int nbrPixelbyPosition(int position){
  int iY = position / Hlength;
  int iX = position % Hlength;
  return nbrPixelbyCoordinate(iX,iY);
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

  return position;
}

void drawFrameFromBuffer(short frameType,int bufferLength){
  if (Debug == true){Serial.println("type " + frameType);}
  if (frameType == 0){
    renderTypeZero(bufferLength);
  }else if(frameType == 3){
    renderTypeThree(bufferLength);
  }else{
    if (Debug == true){Serial.println("frtyNotFound");}
  }
 }


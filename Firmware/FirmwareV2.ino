#include <stdlib.h> // for malloc and free
#include <OctoWS2811.h>



//Configuration
const int SerialBaudrate = 100000;
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


//Code
void setup() {
  Serial.begin(100000);
  leds.begin();
  leds.show();
}

//DecompressionConfiguration
byte incomingSequenceFlag = 200;

void loop(){
	byte * buffer;
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
			bufferLengthBytesSTOR = incomingByte;
			currentFlag = 2;
			
		}else if(currentFlag == 2){
			bufferLength = (bufferLengthBytesSTOR * 255) + incomingByte;
			if (Debug == true){Serial.println("rcvlen" + String(bufferLength));}
			bufferPosition = 0;
			currentFlag = 3;
			
		}else if (currentFlag == 3){
			frameType = incomingByte;
			currentFlag = 4;
			
		}else if (currentFlag == 4){
			if (bufferPosition == 0) {
				free(buffer);
				buffer = (byte*) calloc(bufferLength, sizeof (byte));
			}
			buffer[bufferPosition] = incomingByte;
			bufferPosition +=1;
			
			if (bufferPosition == bufferLength){
				drawFrameFromBuffer(buffer,frameType);
				currentFlag = 0;
			}
          }
		}
	}
}

void drawFrameFromBuffer(byte buffer[],short frameType){
	if (frameType == 0){
		renderTypeZero(buffer);
	}else if(frameType == 3){
		renderTypeThree(buffer);
	}
}


void renderTypeThree(byte buffer[]){//RFCA compression V1.0
  char SkipSignal = 0;
  int lengthRGB[3];
  lengthRGB[0] = buffer[1] * 255 + buffer[2];
  lengthRGB[1] = buffer[3] * 255 + buffer[4];
  lengthRGB[2] = buffer[5] * 255 + buffer[6];

  int counter = 7;
  for (int p = 0; i < 3;p++){
    int locmax = lengthRGB[p] + counter;
    int index = 0;
    while (index <= locmax){
      if (buffer[counter] == SkipSignal){
        index += buffer[counter+1];
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
void renderTypeZero(byte buffer[]) {
  int allpixels = leds.numPixels();
  if (frameLength % 3 == 0) {
    int innerLength = frameLength / 3;
    Serial.println("0rnd");
    for (int i = 0; i < (frameLength / 3); i++) {
      if (i < allpixels) {
        long color = ((long)frame[i] << 16) | ((long)frame[i + innerLength] << 8) | (long)frame[i + innerLength*2];
        //Serial.println("R:" + String(frame[i]) + " G:" + String(frame[i + innerLength]) + " B:" + String(frame[i + innerLength*2]));
        //Serial.println(color, HEX);
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

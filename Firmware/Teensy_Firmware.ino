#include <OctoWS2811.h>
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
char buffer [Vlength*Hlength*3+20];
char rfbuffer [Vlength*Hlength*3+20];
char rfheader[10];
//additional vars
int buffercounter = 0;
char step = 0;


void setup() {
  // put your setup code here, to run once:
  pinMode(13, OUTPUT);
  Serial.begin(100000);
  leds.begin();
  leds.show();
}
int incomingByte;
void loop() {
  // put your main code here, to run repeatedly:
  while (true){
    if (Serial.available() > 0) {
      rndswitch();
      incomingByte = Serial.read();
      Packet_collector(incomingByte);
    }
  }
}
void Packet_collector(char value){
  if(value == 200 and step == 0){
    step = 1;
  }else if(step == 1){
    step = 2;
    rfheader[0] = value;
  }else if(step == 2){
    rfheader[1] = value;
    step = 3;
  }else if(step == 3){
    rfheader[2] = value;
    if ((((int)rfheader[0])*255+rfheader[1])%71 == value){
      step = 4;
    }else{
      Serial.println("RCVinvsize");
      Packet_clean();
    }
  }else if(step == 4){
    rfheader[3] = value;
    step = 5;
  }else if(step == 5){
    rfheader[4] = value;
    step = 6;
  }else if(step == 6){
    buffer[buffercounter] = value;
    buffercounter++;
    if (buffercounter == ((int)rfheader[0])*255+rfheader[1]){
      long sum = 0;
      for (int i = 0; i < buffercounter; i++){
        if ((i % 5) == 0){
          sum = sum + buffer[i]%7;
        }else if((i%7) == 0){
          sum = sum + buffer[i]%5;
        }else if((i%11) == 0){
          sum = sum + buffer[i]%11;
        }else if((i%13) == 0){
          sum = sum + buffer[i]%13;
        }else if((i%17) == 0){
          sum = sum + buffer[i]%17;
        }else if((i%19) == 0){
          sum = sum + buffer[i]%19;
        }else if((i%3) == 0){
          sum = sum + buffer[i]%3;
        }else{
          sum = sum + buffer[i];
        }
      }
      Serial.println((sum/255));
      if ((sum/255) == (int)rfheader[4]){
        rndswitch();
        if (rfheader[3] == (char)0){
          Image_RAW();
        }else if(rfheader[3] == (char)1){
          Image_RFCA();
        }
        Packet_clean();
        Serial.println("OK");
      }else{
        Serial.println("RCVmissing");
      }
    }
  }
}
void Image_RAW() {
  long color;
  int innerLength = (((int)rfheader[0])*255+rfheader[1]);
  if (innerLength % 3 == 0) {
    for (int i = 0; i < ((innerLength/3)); i++) {
      if (i < Hlength*Vlength) {
        color = Color(buffer[i],buffer[i + (innerLength/3)],buffer[i + ((innerLength/3)*2)]);
        leds.setPixel(Image_PixelfromIndex(i), color);
      }
    }
    leds.show();
  }
}
short on = 0;
void rndswitch(){
  if (on == 1){
    digitalWrite(13, HIGH);
    on = 0;
  }else{
    digitalWrite(13, LOW);
    on = 1;
  }
}
void Image_RFCA() { //RFCA compression V1.0; ONLY RFCA V2.0
  char SkipSignal = 1;
  int lengthRGB[3];
  lengthRGB[0] = buffer[0] * 255 + buffer[1];
  lengthRGB[1] = buffer[2] * 255 + buffer[3];
  lengthRGB[2] = buffer[4] * 255 + buffer[5];

  int index, locmax, counter;
  short pixelpos;
  counter = 6;
  locmax = counter;
  int pSize = Vlength * Hlength;
  for (int p = 0; p < 3; p++) {
    index = 0;
    locmax += lengthRGB[p];
    while (counter < locmax) {
      if (buffer[counter] == SkipSignal) {
        index += buffer[counter + 1];
        counter += 2;
      } else {
        pixelpos = Image_PixelfromIndex(index);
        rfbuffer[pSize * p + pixelpos] = buffer[counter];
        leds.setPixel(pixelpos, Color(rfbuffer[pixelpos], rfbuffer[pSize * 1 + pixelpos], rfbuffer[pSize * 2 + pixelpos]));
        index += 1;
        counter += 1;
      }
    }
  }
  leds.show();
}
int Image_PixelfromIndex(long position){
  int iY = position / Hlength;
  int iX = position % Hlength;
  return Image_PixelfromCoordinate(iX,iY);
}
int Image_PixelfromCoordinate(int X,int Y){
  int position = Y * Hlength;
  if (Y%2 == 1){
    position += Hlength-(X+1);
  }else{
    position += X;
  }
  return position;
}
unsigned int Color(unsigned int r, unsigned int g, unsigned int b){
  return (((unsigned int)b & 0xFF )<<16 | ((unsigned int)r & 0xFF)<<8 | (unsigned int)g & 0xFF);
}
void Packet_clean(){
  //clean Packet header
  for (char i = 0; i < 10;i++){
    rfheader[i] = 0;
  }
  //clean buffer
  for (int i = 0; i < Vlength*Hlength*3+20; i++){
    buffer[i] = 0;
  }
  //clean internal vars
  step = 0;
  buffercounter = 0;
}



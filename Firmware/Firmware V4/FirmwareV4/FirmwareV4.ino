#include <OctoWS2811.h>
const int Vlength = 28; // The vertival amount of lED's
const int Hlength = 28; // The Horizontal amount of LED's
const int VrowsperStrip = 4;
const int ledsPerStrip = Hlength * VrowsperStrip;
DMAMEM int displayMemory[Hlength * VrowsperStrip * 6];
int drawingMemory[ledsPerStrip * 6];
const int config = WS2811_GRB | WS2811_800kHz;
const int SerialBaudrate = 1000000;
OctoWS2811 leds(ledsPerStrip, displayMemory, drawingMemory, config);

//additional vars
uint8_t buffercounter = 0;
uint8_t step = 0;
unsigned long headTimer = 0;


//local buffers 
uint8_t rfbuffer [Vlength * Hlength*3];
uint8_t buffer [Vlength*Hlength*3+20];
uint8_t header [10];
uint8_t Packet_hash(){
  uint16_t sum = 0;
  for (uint8_t i = 0; i<Packet_size(); i++){
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
  return (uint8_t)(sum/255);
}
void Packet_clean(){
  //clean Packet header
  for (uint8_t i = 0; i < 10;i++){
    header[i] = 0;
  }
  //clean buffer
  for (uint8_t i = 0; i < Vlength*Hlength*3+20; i++){
    header[i] = 0;
  }
  //clean internal vars
  step = 0;
  buffercounter = 0;
  headTimer = 0;
}
uint16_t Packet_size(){
  if (step >= 2){
    return (((long) header[1])*255+header[2]);
  }
  return 0;
}
void Image_RFCA(){
  char SkipSignal = 1;
  int pixelCount = Vlength * Hlength;
  
  int CompressedChannelSize[3];
  CompressedChannelSize[0] = buffer[0] * 255 + buffer[1];
  CompressedChannelSize[1] = buffer[2] * 255 + buffer[3];
  CompressedChannelSize[2] = buffer[4] * 255 + buffer[5];

  short pixelpos;
  int positionOffset = 6;
  for (int c = 0; c < 3;c++){
    int channelIndex = 0;
  int imageIndex = 0;
  positionOffset +=CompressedChannelSize[c];
    while (channelIndex < CompressedChannelSize[c]){
      if (buffer[positionOffset + channelIndex] == SkipSignal){
        imageIndex += buffer[positionOffset + channelIndex + 1];
        channelIndex +=2;
      }else{
        pixelpos = Image_PixelfromIndex(imageIndex);
    rfbuffer[pixelCount*c + pixelpos] = buffer[positionOffset + channelIndex];
        leds.setPixel(pixelpos,Color(rfbuffer[pixelpos],rfbuffer[(pixelCount/3)+pixelpos],rfbuffer[(pixelCount/3)*2+pixelpos]));
        imageIndex +=1;
        channelIndex +=1;
      }
    }
  }
  leds.show();
}
int Image_PixelfromIndex(uint16_t position){
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
  return(((unsigned int)b & 0xFF )<<16 | ((unsigned int)r & 0xFF)<<8 | (unsigned int)g & 0xFF);
}
void Image_RAW() {
  long color;
  uint16_t innerLength = Packet_size();
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
void Packet_collector(int value){
  if (headTimer != 0 && headTimer + 200 < millis()){
    Packet_clean();
  }
  //first byte is allways 200
  if (step == 0 && value != 200){return;}
  switch (step) {
    case 0://init byte
      headTimer = millis();
      step = 1;
      break;
      Serial.println("HI");
    case 1://Size /255
      step = 2;
      header[0] = value;
      break;
    case 2://Size %255
      step = 3;
      header[1] = value;
      break;
    case 3: //checksum size%71
      step = 4;
      header[2] = value;
      if (value != (Packet_size())%71){
        Packet_clean();
        Serial.println("RCVmissing");
      }
      headTimer = 0;
      break;
    case 4: //set Type
      header[3] = value;
      step = 5;
      break;
    case 5://get sec val for content 
      header[4] = value;
      step = 6;
      break;
    case 6: // get Data
      buffer[buffercounter] = value;
      buffercounter++;
      break;
    }
    if (step == 6 && Packet_size() == buffercounter){
      if (Packet_hash() != header[4]){
        Packet_clean();
        Serial.println("RCVmissing");
      }
      //todo:send verification
      rndswitch();
      Serial.println("RNDcomplete");
      switch (header[3]){
        case 0://RAW type
        Image_RAW();
        break;
        case 1://RFCA type
        Image_RFCA();
        break;
      }
      Packet_clean();
    }
  
}
void setup() {
  Serial.begin(SerialBaudrate);
  pinMode(13, OUTPUT);
  leds.begin();
  leds.show();
  rndswitch();
}

int incomingByte;
// the loop routine runs over and over again forever:
void loop() {
  if (Serial.available() > 0) {
    // read the oldest byte in the serial buffer:
    incomingByte = Serial.read();
    rndswitch();
    Packet_collector(incomingByte);
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

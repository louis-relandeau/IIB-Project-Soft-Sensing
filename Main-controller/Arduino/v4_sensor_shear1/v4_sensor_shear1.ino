#include <Wire.h>
#include <Adafruit_ADS1X15.h>

Adafruit_ADS1115 ads1115a; 
Adafruit_ADS1115 ads1115b;

//SDA is green and pin A4
//SCL is yellow and pin A5
//Red 5V - Black GND

char incoming_data[3];//CMD,data
char ipt;
int n = 0;

int16_t adc0, adc1, adc2, adc3, adc4, adc5, adc6, adc7;

void(* resetFunc) (void) = 0;

void setup(void)
{
  Serial.begin(115200);

  ads1115a.begin();
  ads1115a.begin(0x49);
  ads1115b.begin(0x48);
  ads1115a.setGain(GAIN_ONE);
  ads1115b.setGain(GAIN_ONE);
  ads1115a.setDataRate(RATE_ADS1115_860SPS);
  ads1115b.setDataRate(RATE_ADS1115_860SPS);
}

void loop(void)
{
  while(Serial.available()){
    ipt = char(Serial.read());
    //store ipt if not eot
    if(ipt!='\n'){
        if(n>2){
            n=0;
            continue;    
        }
        incoming_data[n]=ipt;
        n++;
    }
    else{
        n=0;    
        switch(incoming_data[0]){
            case 'R':
//                Serial.print("done\r\n");
                delay(0.1);
                resetFunc();
                break;
            case 'N':
//                Serial.print("Skin Sense\r\n");
//                Serial.print("done\r\n");
                break;
            case 'S':
                Serial.print(adc0); Serial.print("\t"); 
                Serial.print(adc1); Serial.print("\t"); 
                Serial.print(adc2); Serial.print("\t"); 
                Serial.print(adc3); Serial.print("\t"); 
                Serial.print(adc4); Serial.print("\t"); 
                Serial.print(adc5); Serial.print("\t");
                Serial.print(adc6); Serial.print("\t"); 
//                Serial.print(adc7); Serial.print("\t");     
                break;
        
            default:
//                Serial.print("INVALID CMD\r\n");
//                Serial.print("done\r\n");
                break; 
        }
    }
  }
  adc0 = ads1115a.readADC_SingleEnded(3);
  adc1 = ads1115a.readADC_SingleEnded(2);
  adc2 = ads1115a.readADC_SingleEnded(1);
  adc3 = ads1115a.readADC_SingleEnded(0);
  adc4 = ads1115b.readADC_SingleEnded(3);
  adc5 = ads1115b.readADC_SingleEnded(2);
  adc6 = ads1115b.readADC_SingleEnded(1);
//  adc7 = ads1115b.readADC_SingleEnded(0);
}

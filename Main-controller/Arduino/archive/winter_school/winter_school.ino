#include <Wire.h>
#include <Adafruit_ADS1X15.h>
#include <Servo.h>

Adafruit_ADS1115 ads1115; // Construct an ads1115 

char incoming_data[3];//CMD,data
char ipt;
int n = 0;
bool streaming = 1;

Servo flexor;

int fl_angle = 90;

void(* resetFunc) (void) = 0;

void setup(void)
{
  Serial.begin(115200);
  Serial.print("Skin Sense\r\n");

  flexor.attach(9);
  flexor.write(fl_angle);
  
  //Serial.println("Getting single-ended readings from AIN0..3");
  //Serial.println("ADC Range: +/- 6.144V (1 bit = 188uV)");
  ads1115.begin(0x49);
  ads1115.setGain(GAIN_ONE);
  ads1115.setDataRate(RATE_ADS1115_860SPS);
}

void loop(void)
{
  int16_t adc0, adc1, adc2, adc3;
  int tic;

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
    }else{
        n=0;    
        Serial.print("received\r\n");
        switch(incoming_data[0]){
            case 'R':
                Serial.print("done\r\n");
                delay(0.1);
                resetFunc();
                break;
            case 'N':
                Serial.print("Skin Sense\r\n");
                Serial.print("done\r\n");
                break;
            case 'S':
                streaming = incoming_data[1]-'0';            
                Serial.print(incoming_data[1]);
                Serial.print('\n');
                Serial.print("done\r\n");
                break;
            case 'M':
                fl_angle = int(incoming_data[1]-'0');
                fl_angle = map(fl_angle,0,78,20,165);            
                Serial.print(fl_angle);
                Serial.print('\n');
                flexor.write(fl_angle);
                Serial.print("done\r\n");
                break;
        
            default:
                Serial.print("INVALID CMD\r\n");
                Serial.print("done\r\n");
                break; 
        }
    }
  }
  if(streaming==1){ 
    tic = micros();

    adc0 = ads1115.readADC_SingleEnded(0);
    adc1 = ads1115.readADC_SingleEnded(1);
    adc2 = ads1115.readADC_SingleEnded(2);
    adc3 = ads1115.readADC_SingleEnded(3);
    //Serial.print("S\t"); Serial.print(micros()-tic); Serial.print("\t"); 
    Serial.print(adc0); Serial.print("\t"); Serial.print(adc1); Serial.print("\t"); Serial.print(adc2); Serial.print("\t"); Serial.print(adc3); Serial.print("\r\n"); 
  }
  delay(1);
}

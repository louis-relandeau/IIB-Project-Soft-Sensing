#include <Wire.h>
#include <Adafruit_ADS1X15.h>

Adafruit_ADS1115 ads1115d;

/* Mapping name to the array of pressure sensors
 * See picture in Journal
 */

//SDA is green and pin A4
//SCL is yellow and pin A5
//Red 5V - Black GND

char incoming_data[3];//CMD,data
char ipt;
int n = 0;

int16_t adc15;

void(* resetFunc) (void) = 0;

void setup(void)
{
  Serial.begin(115200);
  ads1115d.begin(0x4a);
  ads1115d.setGain(GAIN_ONE);
  ads1115d.setDataRate(RATE_ADS1115_860SPS);

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
            case 'S':
                Serial.print(adc15); Serial.print("\r\n");
                break;
        }
    }
  }
  adc15 = ads1115d.readADC_SingleEnded(3); 
}

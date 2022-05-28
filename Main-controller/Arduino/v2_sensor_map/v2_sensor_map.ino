#include <Wire.h>
#include <Adafruit_ADS1X15.h>
#include <Servo.h>

Adafruit_ADS1115 ads1115a; 
Adafruit_ADS1115 ads1115b;
Adafruit_ADS1115 ads1115c; 
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
bool streaming = 1;

Servo myservo;

int servo_open = 170;
int servo_close = 130;

int servo_state = servo_open;

void(* resetFunc) (void) = 0;

void setup(void)
{
  Serial.begin(115200);

  //ads1115a.begin();
  ads1115a.begin(0x49);
  ads1115b.begin(0x48);
  ads1115c.begin(0x4b);
  ads1115d.begin(0x4a);
  ads1115a.setGain(GAIN_ONE);
  ads1115b.setGain(GAIN_ONE);
  ads1115c.setGain(GAIN_ONE);
  ads1115d.setGain(GAIN_ONE);
  ads1115a.setDataRate(RATE_ADS1115_860SPS);
  ads1115b.setDataRate(RATE_ADS1115_860SPS);
  ads1115c.setDataRate(RATE_ADS1115_860SPS);
  ads1115d.setDataRate(RATE_ADS1115_860SPS);

  myservo.attach(9);  // attaches the servo on pin 9 to the servo object
  myservo.write(servo_state);
}

void loop(void)
{
  int16_t adc0, adc1, adc2, adc3, adc4, adc5, adc6, adc7, adc8, adc9, adc10, adc11, adc12, adc13, adc14, adc15;
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
    }
    else{
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
                streaming = incoming_data[1]-'0'; // 'S0' stopps streaming, 'S1' starts it           
                Serial.print(incoming_data[1]);
                Serial.print('\n');
                Serial.print("done\r\n");
                break;
            case 'M':     
                Serial.print('\n');
                servo_control();
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
    adc0 = ads1115a.readADC_SingleEnded(0);
    adc1 = ads1115a.readADC_SingleEnded(1);
    adc2 = ads1115a.readADC_SingleEnded(2);
    adc3 = ads1115a.readADC_SingleEnded(3);
    adc4 = ads1115b.readADC_SingleEnded(0);
    adc5 = ads1115b.readADC_SingleEnded(1);
    adc6 = ads1115b.readADC_SingleEnded(2);
    adc7 = ads1115b.readADC_SingleEnded(3);
    adc8 = ads1115c.readADC_SingleEnded(0);
    adc9 = ads1115c.readADC_SingleEnded(1);
    adc10 = ads1115c.readADC_SingleEnded(2);
    adc11 = ads1115c.readADC_SingleEnded(3);
    adc12 = ads1115d.readADC_SingleEnded(0);
    adc13 = ads1115d.readADC_SingleEnded(1);
    adc14 = ads1115d.readADC_SingleEnded(2);
    adc15 = ads1115d.readADC_SingleEnded(3);
    //Serial.print("S\t"); Serial.print(micros()-tic); Serial.print("\t"); 
    Serial.print("0:"); Serial.print(adc0/100); Serial.print("\t"); 
    Serial.print("1:"); Serial.print(adc1/100); Serial.print("\t"); 
    Serial.print("2:"); Serial.print(adc2/100); Serial.print("\t"); 
    Serial.print("3:"); Serial.print(adc3/100); Serial.print("\t"); 
    Serial.print("4:"); Serial.print(adc4/100); Serial.print("\t"); 
    Serial.print("5:"); Serial.print(adc5/100); Serial.print("\t");
    Serial.print("6:"); Serial.print(adc6/100); Serial.print("\t"); 
    Serial.print("7:"); Serial.print(adc7/100); Serial.print("\t");     
    Serial.print("8:"); Serial.print(adc8/100); Serial.print("\t"); 
    Serial.print("9:"); Serial.print(adc9/100); Serial.print("\t"); 
    Serial.print("10:"); Serial.print(adc10/100); Serial.print("\t"); 
    Serial.print("11:"); Serial.print(adc11/100); Serial.print("\t"); 
    Serial.print("12:"); Serial.print(adc12/100); Serial.print("\t"); 
    Serial.print("13:"); Serial.print(adc13/100); Serial.print("\t");
    Serial.print("14:"); Serial.print(adc14/100); Serial.print("\t"); 
    Serial.print("15:"); Serial.print(adc15/100); Serial.print("\r\n"); 
  }
  delay(1);
}


void servo_control(){
  if (servo_state == servo_open){
    myservo.write(servo_close);
    servo_state = servo_close;
  }
  else if (servo_state == servo_close){
    myservo.write(servo_open);                    
    servo_state = servo_open;
  }
}

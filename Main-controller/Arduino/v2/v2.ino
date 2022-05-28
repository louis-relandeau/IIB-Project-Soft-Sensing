#include <Wire.h>
#include <Adafruit_ADS1X15.h>
#include <Servo.h>

Adafruit_ADS1115 ads1115a; 
Adafruit_ADS1115 ads1115b;

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
  
  ads1115a.begin();
  //.begin(0x48);
  ads1115b.begin(0x49);
  ads1115a.setGain(GAIN_ONE);
  ads1115b.setGain(GAIN_ONE);
  ads1115a.setDataRate(RATE_ADS1115_860SPS);
  ads1115b.setDataRate(RATE_ADS1115_860SPS);

  myservo.attach(9);  // attaches the servo on pin 9 to the servo object
  myservo.write(servo_state);
}

void loop(void)
{
  int16_t adc0, adc1, adc2, adc3, adc4, adc5, adc6, adc7;
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
    //Serial.print("S\t"); Serial.print(micros()-tic); Serial.print("\t"); 
    Serial.print(adc0); Serial.print("\t"); Serial.print(adc1); Serial.print("\t"); Serial.print(adc2); Serial.print("\t"); Serial.print(adc3); Serial.print("\t"); 
    Serial.print(adc4); Serial.print("\t"); Serial.print(adc5); Serial.print("\t"); Serial.print(adc6); Serial.print("\r\n"); 
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

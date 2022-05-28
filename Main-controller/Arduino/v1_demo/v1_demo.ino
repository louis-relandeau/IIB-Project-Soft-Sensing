#include <Wire.h>
#include <Adafruit_ADS1X15.h>

//Adafruit_ADS1015 ads1015;    // Construct an ads1015 
Adafruit_ADS1115 ads1115a; // Construct an ads1115 
Adafruit_ADS1115 ads1115b;

//SDA is green and pin A4
//SCL is yellow and pin A5
//Red 5V - Black GND

#include <Servo.h>
Servo myservo;  // create servo object to control a servo

unsigned long tic;

int servo_open = 170;
int servo_close = 130;

int servo_state = servo_open;
int node = 0;

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
//  read_sensors();

  if (Serial.available()){
    node = Serial.readString().toInt();
    if (node == 1) {
      read_sensors();
    }
    if (node == 2) {
      servo_control();
    }
  }
  
}

void read_sensors(){
  int16_t adc0, adc1, adc2, adc3, adc4, adc5, adc6, adc7;
  adc0 = ads1115a.readADC_SingleEnded(0);
  adc1 = ads1115a.readADC_SingleEnded(1);
  adc2 = ads1115a.readADC_SingleEnded(2);
  adc3 = ads1115a.readADC_SingleEnded(3);
  adc4 = ads1115b.readADC_SingleEnded(0);
  adc5 = ads1115b.readADC_SingleEnded(1);
  adc6 = ads1115b.readADC_SingleEnded(2);
  //adc7 = ads1115b.readADC_SingleEnded(3);  weird output, leak?
  Serial.print(adc0); Serial.print("    "); Serial.print(adc1); Serial.print("    "); Serial.print(adc2); Serial.print("    "); Serial.print(adc3); Serial.print("    "); 
  Serial.print(adc4); Serial.print("    "); Serial.print(adc5); Serial.print("    "); Serial.println(adc6); //Serial.print("    "); Serial.print(adc7); Serial.println("    ");   
//  delay(1);
  Serial.flush();
}

void servo_control(){
  if (servo_state == servo_open){
    for (int pos = servo_open; pos >= servo_close; pos -= 1) { 
      myservo.write(pos);              
      delay(15);                       
    }
    servo_state = servo_close;
  }
  else if (servo_state == servo_close){
    for (int pos = servo_close; pos <= servo_open; pos += 1) { 
      myservo.write(pos);              
      delay(15);                       
    }
    servo_state = servo_open;
  }
}

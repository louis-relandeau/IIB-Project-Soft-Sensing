#include <Wire.h>
#include <Adafruit_ADS1X15.h>
#include <Servo.h>

Adafruit_ADS1115 ads1115a; 
Adafruit_ADS1115 ads1115b;

//SDA is green and pin A4
//SCL is yellow and pin A5
//Red 5V - Black GND
//
//char incoming_data[3];//CMD,data
//char ipt;
//int n = 0;

int16_t adc0, adc1, adc2, adc3, adc4, adc5, adc6, adc7;

void(* resetFunc) (void) = 0;

void setup(void)
{
  Serial.begin(115200);

  ads1115a.begin();
  ads1115a.begin(0x49);
  ads1115b.begin(0x48);
//  ads1115c.begin(0x4b);
//  ads1115d.begin(0x4a);
  ads1115a.setGain(GAIN_ONE);
  ads1115b.setGain(GAIN_ONE);
//  ads1115c.setGain(GAIN_ONE);
//  ads1115d.setGain(GAIN_ONE);
  ads1115a.setDataRate(RATE_ADS1115_860SPS);
  ads1115b.setDataRate(RATE_ADS1115_860SPS);
//  ads1115c.setDataRate(RATE_ADS1115_860SPS);
//  ads1115d.setDataRate(RATE_ADS1115_860SPS);
  Serial.println('starting program');
}


void loop(void)
{
  Serial.print(adc0); Serial.print("\t"); 
  Serial.print(adc1); Serial.print("\t"); 
  Serial.print(adc2); Serial.print("\t"); 
  Serial.print(adc3); Serial.print("\t"); 
  Serial.print(adc4); Serial.print("\t"); 
  Serial.print(adc5); Serial.print("\t");
  Serial.print(adc6); Serial.print("\t"); 
  Serial.print(adc7); Serial.println("\t");     
//  Serial.print(adc8); Serial.print("\t"); 
//  Serial.print(adc9); Serial.print("\t"); 
//  Serial.print(adc10); Serial.print("\t"); 
//  Serial.print(adc11); Serial.print("\t"); 
//  Serial.print(adc12); Serial.print("\t"); 
//  Serial.print(adc13); Serial.print("\t");
//  Serial.print(adc14); Serial.print("\t"); 
//  Serial.print(adc15); Serial.print("\r\n");

  adc0 = ads1115a.readADC_SingleEnded(3);
  adc1 = ads1115a.readADC_SingleEnded(2);
  adc2 = ads1115a.readADC_SingleEnded(1);
  adc3 = ads1115a.readADC_SingleEnded(0);
  adc4 = ads1115b.readADC_SingleEnded(3);
  adc5 = ads1115b.readADC_SingleEnded(2);
  adc6 = ads1115b.readADC_SingleEnded(1);
  adc7 = ads1115b.readADC_SingleEnded(0);
//  adc8 = ads1115c.readADC_SingleEnded(0);
//  adc9 = ads1115c.readADC_SingleEnded(1);
//  adc10 = ads1115c.readADC_SingleEnded(2);
//  adc11 = ads1115c.readADC_SingleEnded(3);
//  adc12 = ads1115d.readADC_SingleEnded(0);
//  adc13 = ads1115d.readADC_SingleEnded(1);
//  adc14 = ads1115d.readADC_SingleEnded(2);
//  adc15 = ads1115d.readADC_SingleEnded(3); 
}

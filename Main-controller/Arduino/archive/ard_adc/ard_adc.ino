#include <Wire.h>
#include <Adafruit_ADS1X15.h>

//Adafruit_ADS1015 ads1015;    // Construct an ads1015 
Adafruit_ADS1115 ads1115a; // Construct an ads1115 
Adafruit_ADS1115 ads1115b;

//SDA is green and pin A4
//SCL is yellow and pin A5

unsigned long tic;

void setup(void)
{
  Serial.begin(115200);
  Serial.println("Hello!");
  
  Serial.println("Getting single-ended readings from AIN0..3");
  Serial.println("ADC Range: +/- 6.144V (1 bit = 188uV)");
  ads1115a.begin();
  //.begin(0x48);
  ads1115b.begin(0x49);
  ads1115a.setGain(GAIN_ONE);
  ads1115b.setGain(GAIN_ONE);
  ads1115a.setDataRate(RATE_ADS1115_860SPS);
  ads1115b.setDataRate(RATE_ADS1115_860SPS);
}

void loop(void)
{
  int16_t adc0, adc1, adc2, adc3, adc4, adc5, adc6, adc7;

  tic = millis();

  adc0 = ads1115a.readADC_SingleEnded(0);
  adc1 = ads1115a.readADC_SingleEnded(1);
  adc2 = ads1115a.readADC_SingleEnded(2);
  adc3 = ads1115a.readADC_SingleEnded(3);
  adc4 = ads1115b.readADC_SingleEnded(0);
  adc5 = ads1115b.readADC_SingleEnded(1);
  adc6 = ads1115b.readADC_SingleEnded(2);
  //adc7 = ads1115b.readADC_SingleEnded(3);  weird output, leak?
  //Serial.print("AIN0: "); Serial.println(adc0);
  //Serial.print("AIN1: "); Serial.println(adc1);
  //Serial.print("AIN2: "); Serial.println(adc2);
  //Serial.print("AIN3: "); Serial.println(adc3);
  //Serial.println(adc0);
  Serial.print(adc0); Serial.print("    "); Serial.print(adc1); Serial.print("    "); Serial.print(adc2); Serial.print("    "); Serial.print(adc3); Serial.print("    "); 
  Serial.print(adc4); Serial.print("    "); Serial.print(adc5); Serial.print("    "); Serial.print(adc6); Serial.println("    "); //Serial.print(adc7); Serial.println("    "); 
  //Serial.println(" ");
  //Serial.println(millis()-tic);
  delay(1);
}

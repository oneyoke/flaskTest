#include <LiquidCrystal.h>
#include <dht.h>

LiquidCrystal lcd(27, 26, 25, 24, 23, 22);

dht DHT;

#define DHT11PIN 28

void setup() {
  lcd.begin(20, 4);
  lcd.clear();
  
}

void loop() {
   int chk = DHT.read11(DHT11PIN);
  switch (chk)
  {
    case DHTLIB_OK:  
                Serial.print("OK,\t"); 
                break;
    case DHTLIB_ERROR_CHECKSUM: 
                Serial.print("Checksum error,\t"); 
                break;
    case DHTLIB_ERROR_TIMEOUT: 
                Serial.print("Time out error,\t"); 
                break;
    case DHTLIB_ERROR_CONNECT:
        Serial.print("Connect error,\t");
        break;
    case DHTLIB_ERROR_ACK_L:
        Serial.print("Ack Low error,\t");
        break;
    case DHTLIB_ERROR_ACK_H:
        Serial.print("Ack High error,\t");
        break;
    default: 
            Serial.print("Unknown error,\t"); 
                break;
  }
lcd.setCursor(0, 0);
lcd.print("humidity ");
lcd.print(DHT.humidity);
lcd.setCursor(0, 1);
lcd.print("temperature ");
lcd.print(DHT.temperature);
delay(2000);
  }
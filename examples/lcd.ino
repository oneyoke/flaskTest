# define FIRST_LED_PIN 33
# define LAST_LED_PIN 42
void setup() {
 for (int pin=FIRST_LED_PIN; pin<=LAST_LED_PIN; pin++)
 pinMode(pin, OUTPUT);
}
void loop() {
  unsigned long int ms=millis();
  int pin=FIRST_LED_PIN+(ms/120)%10;
  digitalWrite(pin, HIGH);
  delay(10);
  digitalWrite(pin, LOW); 
}
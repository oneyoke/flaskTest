# define FIRST_LED_PIN 33
# define LAST_LED_PIN 42
void setup() {
 for (int pin=FIRST_LED_PIN; pin<=LAST_LED_PIN; pin++)
 pinMode(pin, OUTPUT);
}
void loop() {
  for (int pin=FIRST_LED_PIN; pin<=LAST_LED_PIN; pin++)
  {
    digitalWrite(pin, HIGH);
    delay(140);
    digitalWrite(pin, LOW); 
  }
}
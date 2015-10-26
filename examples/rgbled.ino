int REDpin = 29;
int GREENpin = 30;
int BLUEpin = 31;
void setup(){}
//Главный цикл
void loop(){
  for(int value = 0 ; value <= 255; value +=1) { 
    analogWrite(REDpin, value);
    analogWrite(GREENpin, 255-value);
    analogWrite(BLUEpin, 255);
    delay(30);
  }
  for(int value = 0 ; value <= 255; value +=1) { 
    analogWrite(REDpin, 255);
    analogWrite(GREENpin, value);
    analogWrite(BLUEpin, 255-value);
    delay(30);
  }


  for(int value = 0 ; value <= 255; value +=1) { 
    analogWrite(REDpin, 255-value);
    analogWrite(GREENpin, 255);
    analogWrite(BLUEpin, value);
    delay(30);
  }
}
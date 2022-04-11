#define RED_BUTTON 2
#define BLUE_LED 3
#define GREEN_LED 5
#define RED_LED 6

unsigned long startpress, endpress, firstend, secondstart, timepressed;
boolean firstpressed;

void setup()
{
  pinMode(RED_BUTTON, INPUT_PULLUP);
  pinMode(BLUE_LED, OUTPUT);
  pinMode(GREEN_LED, OUTPUT);
  pinMode(RED_LED, OUTPUT);

  firstpressed = false;
 
  Serial.begin(9600);
}

void loop()
{
  if(digitalRead(RED_BUTTON) == LOW) {
    startpress = millis();
    if (firstpressed) secondstart=startpress;
    Serial.println("Red flashes (Button pressed)");
    digitalWrite(RED_LED, HIGH);
    delay(20);
    digitalWrite(RED_LED, LOW);
    while (digitalRead(RED_BUTTON) == LOW){
      endpress = millis();
      timepressed = endpress - startpress;
      if(timepressed>=2000) {
        if(digitalRead(GREEN_LED) == LOW) {digitalWrite(GREEN_LED, HIGH); digitalWrite(RED_LED, LOW); Serial.println("Green flashes");}
        else {digitalWrite(GREEN_LED, LOW); digitalWrite(RED_LED, HIGH); Serial.println("Red flashes");}
        delay(1000);
      }
    }
    Serial.println("Green flashes (Button realeses)");
    digitalWrite(GREEN_LED, HIGH);
    delay(20);
    digitalWrite(GREEN_LED, LOW);
    endpress = millis();
    timepressed = endpress - startpress;
    if(firstpressed == false) firstend = endpress;
  }
  if (firstpressed && secondstart-firstend<300) {Serial.println("Blue flashes");digitalWrite(BLUE_LED, HIGH); delay(20); digitalWrite(BLUE_LED, LOW);firstpressed = false; timepressed=0;} 
  else if(firstpressed) firstpressed = false;
  else if (timepressed>10 && timepressed<200 && firstpressed == false) firstpressed = true;
}

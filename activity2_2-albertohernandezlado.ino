#define RED_BUTTON 2

unsigned long starttime, time;
String timepressed, formattime;
int milli, sec, min, hour;

void setup()
{
  pinMode(RED_BUTTON, INPUT_PULLUP);
 
  Serial.begin(9600);
}

void loop()
{
  starttime = millis();
  while (digitalRead(RED_BUTTON) == LOW){
  }
  time = millis() - starttime;
  if(time>30){
    timepressed = "Button pressed: " + String(time,DEC) + "ms -> ";
    Serial.print(timepressed);
    int milli = time%1000; time -= milli; time /= 1000;
    int sec = time%60; time -= sec; time /= 60;
    int min = time%60; time -= min; time /= 60;
    int hour = time%60; time -= hour; time /= 60;
    
  	formattime = String(hour,DEC) + ":" + String(min,DEC) + ":" + String(sec,DEC) + "." + String(milli,DEC);
    Serial.println(formattime);
  }
}
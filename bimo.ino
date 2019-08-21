//This arduino sketch is used to check whether serial comm works
//Sends data upon button press
unsigned long lastDebounceTime=0;
unsigned long debounceDelay=50;

int buttonState;
int lastButtonState = HIGH;

void setup()
{
  pinMode(2, INPUT_PULLUP);
  Serial.begin(9600);
}

void loop()
{
  int input = !digitalRead(2);
  if(input!=lastButtonState)
    lastDebounceTime = millis();
  if((millis()-lastDebounceTime)>debounceDelay)
  {
    if(input!=buttonState)
    {
      buttonState = input;
      if(input==1)//put value print here
      {
        //collect data here
        Serial.print(49.89); Serial.print(" ");//LBM
        Serial.print(83.42); Serial.print(" ");//LBM_percent
        Serial.print(10.94); Serial.print(" ");//dryleanmass
        Serial.print(38.95); Serial.print(" ");//totalbodywater
        Serial.print(14.41); Serial.print(" ");//extracellularwater
        Serial.print(25.54); Serial.print(" ");//intracellular
        Serial.print(11.79); Serial.print(" ");//skeletalmusclemass
        Serial.print(9.06); Serial.print(" ");//bodyfatmass
        Serial.print(20.77); Serial.print(" ");//bmi
        Serial.print(15.16); Serial.print(" ");//percentbodyfat
        Serial.print(0.37); Serial.print(" ");//ECWTBWratio
        Serial.print(1563.63); Serial.print(" ");//BMR
        Serial.print(2189.07); Serial.print("\n");//recommendedBMR
      }
    }
  }
  lastButtonState=input;
}

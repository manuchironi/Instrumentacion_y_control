
int analogPin = 3; // Fototransistor
int ledPin = 5; // LED
int steps = 100;
int input = 0;
int count = 0;
float mean = 0;
int valorDeseado = 180; // Intensidad deseada
int intensidadSalida = 150;

void setup()
{
  Serial.begin(9600);  //setup serial
}

void loop()
{
  input = analogRead(analogPin);
  mean = mean + (float)input/ (float)steps;
  count = count + 1;
  if (count == steps)
  {
    if ((mean<valorDeseado)and(intensidadSalida<255))
    {
      intensidadSalida = intensidadSalida+1;
    }
    if ((mean>valorDeseado)and(intensidadSalida>0))
    {
      intensidadSalida = intensidadSalida-1;
    }
    Serial.println(mean);
    analogWrite(ledPin,intensidadSalida);
    mean = (float)0;
    count = 0;
  }
}

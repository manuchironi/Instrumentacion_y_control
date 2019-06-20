
int analogPin = 3;     // Entrada analogica del fotodetector
int ledPin = 5;        // Salida del PWM al LeED
int steps = 100;
int input = 0;      
int count = 0;      //
float mean = 0;
float old_error = 0;
float old_old_error = 0;
int setPoint = 100;
int intensidadSalida = 0; // El PWM recibe enteros entre 0 y 255
float kp = 0.001;
float ki = 0.1;
float kd = 1000;
float error = 0;
float error_integrado = 0;
float error_derivado = 0;

void setup()
{
  Serial.begin(9600);          //  setup serial
}

void loop()
{
  input = analogRead(analogPin);    // read the input pin
  mean = mean + (float)input/ (float)steps;
  count = count + 1;
  if (count == steps)
  {
    error = setPoint - mean;
    error_integrado = error_integrado + error;
    error_derivado = error - old_old_error;
    if (error_integrado>1000){
      error_integrado = 1000;
      }
    if (error_integrado<-1000){
      error_integrado = -1000;
      }
    error_derivado = 0;
    intensidadSalida = myPID(error,error_integrado,error_derivado,kp,ki,kd);
    Serial.println(mean);  // Salida serie que vemos en el serial plotter
    analogWrite(ledPin,intensidadSalida); // Escribo con el PWM
    old_old_error = old_error;
    old_error = error;
    mean = (float)0;
    count = 0;
  }
}

int myPID(float error, float error_integrado, float error_derivado, float kp, float ki, float kd){
  float result;
  result = kp*error + ki*error_integrado + kd*error_derivado;
  if (result>254){
    result = 255;
  }
  if (result<0){
    result = 0;
  }
  return (int)result;
}

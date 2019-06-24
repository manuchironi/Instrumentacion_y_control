#include <Stepper.h>

// Valores relacionados al motor y posiciones
const int stepsPerRevolution = 2048;  // change this to fit the number of steps per revolution
const int pasos2a1 = -500;  // Pasos de motor entre la posicion 2 y la 1
const int pasos2a3 = 500;  // Pasos de motor entre la posicion 2 y la 3

// Valores de protocolo de busqueda del fotogate
const int max_pasos = 500; // Amplitud de pasos de busqueda (para un lado y para el otro)
const int steps_por_paso = 1; // Cada step de busqueda avanza N pasos

// initialize the stepper library on pins 8 through 11:
Stepper myStepper(stepsPerRevolution, 8, 9, 10, 11);

// Definicion de los numeros de pines
int LED = 13; // Uso del LED onboard del Aruino Uno
int photogate = 12; // Entrada digital, en 1 si el fotogate está activado
int posicion1 = 1;  // Indica que se desea prender y centrar el diodo en -120°
int posicion2 = 2;  // Indica que se desea prender y centrar el diodo en 0°
int posicion3 = 3;  // Indica que se desea prender y centrar el diodo en 120°

// Definiciond de las variables del programa
int posicion_actual = 0;
int posicion_deseada = 0;
int centrado = 0;
int sens = 0;
int result = 0;

// Se ejecuta una única vez al principio
void setup() {
  Serial.begin(9600);
  myStepper.setSpeed(15);
  pinMode(LED, OUTPUT);
  pinMode(photogate, INPUT);
  pinMode(posicion1, INPUT);
  pinMode(posicion2, INPUT);
  pinMode(posicion3, INPUT);
  digitalWrite(LED, LOW);
  centrado = 0;
  // Centro mi dispositivo en el Fotogate
  while (centrado==0){
    // El dispositivo se queda buscando el fotogate 
    // hasta que la busqueda sea exitosa y la función devuelva un 1
    centrado = buscoPhotogate(max_pasos,steps_por_paso);
  }
  posicion_actual = 2;
}

// Loop principal del programa
void loop() {
  digitalWrite(LED, HIGH);
}

// ----  DEFINICION DE FUNCIONES ----

//Funcion que mueve el motor hashta encontrar el Fotogate
int buscoPhotogate(int max_pasos,int steps_por_paso){
  Serial.println("ENTRE!");
  // Buscamos primero moviendonos un numero de pasos max_pasos a la derecha
  // En cada paso del for avanzamos una cantidad de steps equivalente a steps_por_paso
  for (int x = 0; x < max_pasos; x++) {
    // Chequeamos el estado del Fotogate
    sens = digitalRead(photogate);
    if (sens == HIGH) {
      // Si encontramos el Fotogate, salimos del Loop y avisamos que la bsuqueda fue exitosa
      result = 1;
      break;
    }
    else {
      // Si esta en cero, avanzamos los pasos programados con el motor
      myStepper.step(steps_por_paso);
    }
  }
  // Si salimos del loop por encontrar el fotogate la variable result evita que entremos al segundo barrido
  if (result==0){
    // Ahora giramos apra el lado contrario, y hacemos 2 veces la cantidad de pasos 
    // (una para llegar al 0 otra vez y otra para recorrer la otra parte)
    for (int x = 0; x < 2*max_pasos; x++) {
      sens = digitalRead(photogate);
      if (sens == HIGH) {
        // Si encontramos el Fotogate, salimos del Loop y avisamos que la bsuqueda fue exitosa
        result = 1;
        break;
      }
      else {
        // Si esta en cero, avanzamos los pasos programados con el motor
        myStepper.step(-steps_por_paso);
      }
    }
    if (result==0) {
      // Si no encontré nada en ninguno de los dos barridos, vuelvo a la posición original
      for (int x = 0; x < max_pasos; x++) {
        myStepper.step(steps_por_paso);
      }
    }
  }
  // Si la bsuqueda fue exitosa manda un 1, sino un 0.
  return (int)result;
}

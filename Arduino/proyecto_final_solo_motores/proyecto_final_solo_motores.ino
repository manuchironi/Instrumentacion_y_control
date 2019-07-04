#include <Stepper.h>

// Valores relacionados al motor y posiciones
const int stepsPerRevolution = 2048;  // change this to fit the number of steps per revolution
const int pasos1a2 = 300;  // Pasos de motor entre la posicion 1 y la 2
const int pasos2a3 = 300;  // Pasos de motor entre la posicion 2 y la 3

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
int temp_pos = 0;

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
  
  // Chequeamos la posición deseada
  posicion_deseada = leer_posicion_deseada(posicion_actual);
  
  // Comparamos la posición deseada con la actual, si no igual actuamos
  if (posicion_deseada != posicion_actual){
    
    // Si no estoy en la posicion 2, voy hacia ella
    if (posicion_actual != 2){
      if (posicion_actual == 1){
        mover_1a2(pasos1a2);
      }
      else if (posicion_actual == 3){
        mover_3a2(pasos2a3);
      }
    }

    // Ahora seguro estamos en la posicion 2, desde ahí vamos a la posición deseada (o no hacemos nada si la posicion 2 era la deseada)
    if (posicion_deseada == 1){
      mover_2a1(pasos1a2);
    }
    else if (posicion_deseada == 3){
      mover_2a3(pasos2a3);
    }

    // Finalmente cambio mi posición actual a la deseada
    posicion_actual = posicion_deseada;
  }
  
}


// ----  DEFINICION DE FUNCIONES ----

//Funcion que mueve el motor hashta encontrar el Fotogate
int buscoPhotogate(int max_pasos,int steps_por_paso){
  Serial.println("Buscando centro");
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


// Funcion que lee la entrada para chequear cual es la posicion deseada
int leer_posicion_deseada(int posicion_actual){
  if (posicion1==HIGH && posicion2==LOW && posicion3==LOW) {
    temp_pos = 1;
  }
  else if (posicion1==LOW && posicion2==HIGH && posicion3==LOW) {
    temp_pos = 2;
  }
  else if (posicion1==LOW && posicion2==LOW && posicion3==HIGH){
    temp_pos = 3;
  }
  else {
    // Si la posicion deseada no es clara, se mantiene en la posición actual
    temp_pos = posicion_actual;
  }
  return temp_pos;
}



//Funciones de movimiento

void mover_1a2(int pasos1a2){
  for (int x = 0; x < pasos1a2; x++) {
    myStepper.step(1);
  }
}

void mover_2a3(int pasos2a3){
  for (int x = 0; x < pasos2a3; x++) {
    myStepper.step(1);
  }
}

void mover_2a1(int pasos1a2){
  for (int x = 0; x < pasos1a2; x++) {
    myStepper.step(-1);
  }
}

void mover_3a2(int pasos2a3){
  for (int x = 0; x < pasos2a3; x++) {
    myStepper.step(-1);
  }
}

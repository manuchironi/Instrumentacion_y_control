#include <Stepper.h>

// Valores de seteo del motor
const int STEPS_PER_REVOLUTION = 2048;  // change this to fit the number of steps per revolution
const int VELOCIDAD_MOTOR = 10; // Velocidad de giro del motor
const int STEPS_POR_PASO = 1; // Cada "step" avanza N pasos de motor 
                              // (le pido al motor que avance N pasos por vez)

// Valores de distancia angular de led
// Definidos en "steps" de motor (pueden ser varios pasos)
const int PASOS1A2 = 300;  // Pasos de motor entre la posicion 1 y la 2
const int PASOS2A3 = 300;  // Pasos de motor entre la posicion 2 y la 3

// Valores de protocolo de busqueda del fotogate
const int MAX_PASOS = 500; // Amplitud de pasos de busqueda (para un lado y para el otro)
const int PHOTO_TRESH = 30; // Valor contra el cual se compara a entrada del photogate

=======
const int max_pasos = 500; // Amplitud de pasos de busqueda (para un lado y para el otro)
const int steps_por_paso = 1; // Cada step de busqueda avanza N pasos

// initialize the stepper library on pins 8 through 11:
Stepper myStepper(STEPS_PER_REVOLUTION, 8, 9, 10, 11);

// Definicion de los numeros de pines
const int LED = 13; // Uso del LED onboard del Aruino Uno
const int LASER1 = 2; // Diodo laser asociado a las posicion 1
const int LASER2 = 3; // Diodo laser asociado a las posicion 2
const int LASER3 = 4; // Diodo laser asociado a las posicion 3
const int POSICION1 = 5;  // Indica que se desea prender y centrar el diodo en -120°
const int POSICION2 = 6;  // Indica que se desea prender y centrar el diodo en 0°
const int POSICION3 = 7;  // Indica que se desea prender y centrar el diodo en 120°
const int PHOTOGATE = A3; // Entrada Analogica, proporcional a la señal detectada por el Photogate

// Definiciond de las variables del programa
int posicion_actual = 0;
int posicion_deseada = 0;
int centrado = 0;
int sens = 0;
int result = 0;
int temp_pos = 0;

int valor_posicion1 = 0;
int valor_posicion2 = 0;
int valor_posicion3 = 0;

// Se ejecuta una única vez al principio
void setup() {
  Serial.begin(9600); // Iniciamos comunicación serie
  myStepper.setSpeed(VELOCIDAD_MOTOR); // Seteamos la velocidad del motor

  // Seteamos los pines
  pinMode(LED, OUTPUT);
  pinMode(LASER1, OUTPUT);
  pinMode(LASER2, OUTPUT);
  pinMode(LASER3, OUTPUT);
  pinMode(POSICION1, INPUT);
  pinMode(POSICION2, INPUT);
  pinMode(POSICION3, INPUT);

  // Apago el led y los laseres
  digitalWrite(LED, HIGH);
  apagarLaseres();
  
  // Centro mi dispositivo en el Fotogate
  centrado = 0;
  while (centrado==0){
    // El dispositivo se queda buscando el fotogate 
    // hasta que la busqueda sea exitosa y la función devuelva un 1
    centrado = buscoPhotogate();
  }

  // Actualizo la posicion actual
  posicion_actual = 2;
  
  // Enciendo el laser de la posicion central
  encenderLaser(posicion_actual);
  digitalWrite(LED, LOW);
}

// Loop principal del programa
void loop() {

  // Chequeamos la posición deseada
  posicion_deseada = leerPosicionDeseada(posicion_actual);
  
  // Comparamos la posición deseada con la actual, si no igual actuamos
  if (posicion_deseada != posicion_actual){
    digitalWrite(LED, HIGH);
    // Antes de mover el circuito apago todos los laseres
    apagarLaseres();
    
    // Si no estoy en la posicion 2, voy hacia ella
    if (posicion_actual != 2){
      if (posicion_actual == 1){
        mover1a2();
      }
      else if (posicion_actual == 3){
        mover3a2();
      }
    }

    // Ahora seguro estamos en la posicion 2, desde ahí vamos a la posición deseada (o no hacemos nada si la posicion 2 era la deseada)
    if (posicion_deseada == 1){
      mover2a1();
    }
    else if (posicion_deseada == 3){
      mover2a3();
    }

    // Cambio mi posición actual a la deseada
    posicion_actual = posicion_deseada;

    // Prendo el laser de la posición actual
    encenderLaser(posicion_actual);
    digitalWrite(LED, LOW);
  }
  
}


// ----------------  DEFINICION DE FUNCIONES ----------------

//Funcion que mueve el motor hashta encontrar el Fotogate
int buscoPhotogate(){
  Serial.println("Buscando centro");
  // Buscamos primero moviendonos un numero de pasos MAX_PASOS a la derecha
  // En cada paso del for avanzamos una cantidad de steps equivalente a STEPS_POR_PASO
  for (int x = 0; x < MAX_PASOS; x++) {
    // Chequeamos el estado del Fotogate
    sens = analogRead(PHOTOGATE);
    if (sens > PHOTO_TRESH) {
      // Si encontramos el Fotogate, salimos del Loop y avisamos que la bsuqueda fue exitosa
      result = 1;
      break;
    }
    else {
      // Si esta en cero, avanzamos los pasos programados con el motor
      myStepper.step(STEPS_POR_PASO);
    }
  }
  // Si salimos del loop por encontrar el fotogate la variable result evita que entremos al segundo barrido
  if (result==0){
    // Ahora giramos apra el lado contrario, y hacemos 2 veces la cantidad de pasos 
    // (una para llegar al 0 otra vez y otra para recorrer la otra parte)
    for (int x = 0; x < 2*MAX_PASOS; x++) {
      sens = analogRead(PHOTOGATE);
      if (sens > PHOTO_TRESH) {
        // Si encontramos el Fotogate, salimos del Loop y avisamos que la bsuqueda fue exitosa
        result = 1;
        break;
      }
      else {
        // Si esta en cero, avanzamos los pasos programados con el motor
        myStepper.step(-STEPS_POR_PASO);
      }
    }
    if (result==0) {
      // Si no encontré nada en ninguno de los dos barridos, vuelvo a la posición original
      for (int x = 0; x < MAX_PASOS; x++) {
        myStepper.step(STEPS_POR_PASO);
      }
    }
  }
  // Si la bsuqueda fue exitosa manda un 1, sino un 0.
  return (int)result;
}


// Funcion que lee la entrada para chequear cual es la posicion deseada
int leerPosicionDeseada(int posicion_actual){
  
  valor_posicion1 = digitalRead(POSICION1);
  valor_posicion2 = digitalRead(POSICION2);
  valor_posicion3 = digitalRead(POSICION3);
  
  if (valor_posicion1==HIGH && valor_posicion2==LOW && valor_posicion3==LOW) {
    temp_pos = 1;
  }
  else if (valor_posicion1==LOW && valor_posicion2==HIGH && valor_posicion3==LOW) {
    temp_pos = 2;
  }
  else if (valor_posicion1==LOW && valor_posicion2==LOW && valor_posicion3==HIGH){
    temp_pos = 3;
  }
  else {
    // Si la posicion no es clara, se mantiene en la posición actual
    temp_pos = posicion_actual;
  }
  return temp_pos;
}


// Funcion que apaga todos los laseres
void apagarLaseres(){
  digitalWrite(LASER1, LOW);
  digitalWrite(LASER2, LOW);
  digitalWrite(LASER3, LOW);
}

// Funcion que enciende el laser deseado
void encenderLaser(int posicion_actual){
  if (posicion_actual == 1) {
    digitalWrite(LASER1, HIGH);
    digitalWrite(LASER2, LOW);
    digitalWrite(LASER3, LOW);
  }
  else if (posicion_actual == 2) {
    digitalWrite(LASER1, LOW);
    digitalWrite(LASER2, HIGH);
    digitalWrite(LASER3, LOW);
  }
  else if (posicion_actual == 3){
    digitalWrite(LASER1, LOW);
    digitalWrite(LASER2, LOW);
    digitalWrite(LASER3, HIGH);
  }
  else {
    // Si la posicion no es clara, apaga los laseres
    digitalWrite(LASER1, LOW);
    digitalWrite(LASER2, LOW);
    digitalWrite(LASER3, LOW);
  }
}

// Funciones de movimiento del motor

void mover1a2(){
  for (int x = 0; x < PASOS1A2; x++) {
    myStepper.step(1);
  }
}

void mover2a3(){
  for (int x = 0; x < PASOS2A3; x++) {
    myStepper.step(1);
  }
}

void mover2a1(){
  for (int x = 0; x < PASOS1A2; x++) {
    myStepper.step(-1);
  }
}

void mover3a2(){
  for (int x = 0; x < PASOS2A3; x++) {
    myStepper.step(-1);
  }
}

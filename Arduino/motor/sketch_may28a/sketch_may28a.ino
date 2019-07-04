// Elegir si medio paso o paso completo. Ver también SetDirection.

int respiro=4000; // elegir según el Paso, necesita un mínimo para no trabarse
// con el 28BYJ48, medio paso no necesita respiro, y simple de a dos bobinas necesita 350.
//int Paso [ 8 ][ 4 ] = //doble paso
//   {  {1, 0, 0, 0},
//      {1, 1, 0, 0},
//      {0, 1, 0, 0},
//      {0, 1, 1, 0},
//      {0, 0, 1, 0},
//      {0, 0, 1, 1},
//      {0, 0, 0, 1},
//      {1, 0, 0, 1}
//   };
int Paso [ 4 ][ 4 ] = //paso simple, pero de a dos bobinas
   {  {1, 1, 0, 0},
      {0, 1, 1, 0},
      {0, 0, 1, 1},
      {1, 0, 0, 1}
   };

#define IN1  8 // qué pines de la Arduino van a qué pines del motor
#define IN2  9
#define IN3  10
#define IN4  11

float steps_left; // variable que determina si se mueve o no
boolean Direction = true; // direccion de movimiento
int Steps = 0; // Define el paso actual de la secuencia

void setup()
   { Serial.begin(9600); // para el 28BYJ48 necesita ser 9600
     Serial.print(0); // indicador de que arranca quieto
     pinMode(IN1, OUTPUT); // elige los pines a usar
     pinMode(IN2, OUTPUT);
     pinMode(IN3, OUTPUT);
     pinMode(IN4, OUTPUT);
   }

void loop()
   { if (Serial.available()) // solo arranca si le mando info
  { float steps_left = Serial.parseFloat();
    if (steps_left>0){
      Serial.print(1); // indicador de que está moviéndose
      Direction=true;}
    if (steps_left<0){
      Serial.print(1); // indicador de que está moviéndose
      Direction=false;}
    
    
    while(steps_left>0)
        { 
           stepper() ;     // Avanza un paso
           steps_left-- ;  // Queda un paso menos
           delay (1) ;
        }
    while(steps_left<0)
        { 
           stepper() ;     // Avanza un paso
           steps_left++ ;  // Queda un paso menos
           delay (1) ;
        }
      if (steps_left==0){ // apaga todas las bobinas
      digitalWrite( IN1, 0 );
      digitalWrite( IN2, 0 );
      digitalWrite( IN3, 0 );
      digitalWrite( IN4, 0 );
      Serial.print(0); // indicador de que está detenido
      }
   }
   }

void stepper()            //Avanza un paso
   {  digitalWrite( IN1, Paso[Steps][ 0] );
   delayMicroseconds(respiro);
      digitalWrite( IN2, Paso[Steps][ 1] );
   delayMicroseconds(respiro);
      digitalWrite( IN3, Paso[Steps][ 2] );
   delayMicroseconds(respiro);   
      digitalWrite( IN4, Paso[Steps][ 3] );

      SetDirection();
   }

void SetDirection() // pone los pasos en modulo 4 o modulo 8
   {  
      if(Direction)
         Steps++;
      else
         Steps--;

      //Steps = ( Steps + 8 ) % 8 ; // quiero que Steps vaya de 0 a 7
      Steps = ( Steps + 4 ) % 4 ; // quiero que Steps vaya de 0 a 3
   }

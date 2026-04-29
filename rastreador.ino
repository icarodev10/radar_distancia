#include <Servo.h>

const int pinoTrig = 10;
const int pinoEcho = 11;
const int pinoServo = 6; // Pino PWM para o Servo

Servo motorRadar;

void setup() {
  pinMode(pinoTrig, OUTPUT);
  pinMode(pinoEcho, INPUT);
  Serial.begin(9600);
  motorRadar.write(15); // Vai pra posição inicial ANTES de ligar
  motorRadar.attach(pinoServo);
}

void loop() {
  // Varredura da direita pra esquerda
  for(int angulo = 15; angulo <= 165; angulo++){
    motorRadar.write(angulo);
    delay(30); // Tempo pro motor chegar na posição
    int distancia = medirDistancia();
    
    // Manda pro Python no formato: Angulo,Distancia
    Serial.print(angulo);
    Serial.print(",");
    Serial.println(distancia);
  }
  
  // Varredura da esquerda pra direita
  for(int angulo = 165; angulo >= 15; angulo--){
    motorRadar.write(angulo);
    delay(30);
    int distancia = medirDistancia();
    
    Serial.print(angulo);
    Serial.print(",");
    Serial.println(distancia);
  }
}

// Função isolada pra deixar o loop limpo
int medirDistancia() {
  digitalWrite(pinoTrig, LOW);
  delayMicroseconds(2);
  digitalWrite(pinoTrig, HIGH);
  delayMicroseconds(10);
  digitalWrite(pinoTrig, LOW);
  
  long duracao = pulseIn(pinoEcho, HIGH);
  int calcDist = duracao * 0.034 / 2;
  return calcDist;
}
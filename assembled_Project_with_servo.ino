// Библиотеки 
#include <GParser.h>;
#include <GyverMotor.h>;
#include <Servo.h>;
// Переменные для системы асинхронности 
static byte prevAmount = 0;
static uint32_t tmr = 0;
static uint32_t tmrStopMotors = 0;
byte amountSerial;
boolean flagSerial = false;
int speedM = 255;

// Переменные для моторов 
GMotor motors(DRIVER2WIRE, 2, 3); // 1pin - (LOW/HIGH) 2pin - PWM
Servo servos;


void setup() {
  Serial.begin(9600);// Открытие терминала
  Serial.setTimeout(5); // Задержка обработчика
  motors.setDeadtime(1);
  motors.setDirection(AUTO);
  motors.setMode(AUTO);
  servos.attach(6);
}

void loop() {
  
  amountSerial = Serial.available();

  if (amountSerial != prevAmount) { // Инициализация системного таймера 
    prevAmount = amountSerial;
    tmr = millis();
  }
  
  if ((amountSerial && millis() - tmr > 10) || amountSerial > 60) { // Запуск парсинга 
    mainFunc();
    flagSerial = true;
  }
  
  if (millis() - tmrStopMotors > 3000 && flagSerial==true){
    tmrStopMotors = millis();
    flagSerial = false;
    Serial.println("false");
  };
  if (millis() - tmrStopMotors > 3000 && flagSerial==false){
    tmrStopMotors = millis();
    stopMotors();
  };
  
}


void mainFunc() {
  static uint32_t tmrSwitchFB = 0;
  static uint32_t tmrSwitchLR = 0;
  uint32_t us = micros();// таймер микросекунд
  char str[30];
  int amount = Serial.readBytesUntil(';', str, 30);
  str [amount] = NULL;
  
  GParser data(str, ',');
  int ints[20];
  data.parseInts(ints);

// серво по середине при 93 градусах !!!!
// Вперед/ назад/ холостой/ стоп
  if (millis() - tmrSwitchFB > 2){
    tmrSwitchFB = millis();
    switch (ints[0]) {
      case 1://Вперед
        forward(speedM);
      break;
      case 2://Назад
        backward(speedM);
      break;
      case 0://Холостой
        chill();
      break;
      case 5://Стоп 
        stopMotors();
      break;
    };
  };

  if (millis() - tmrSwitchLR > 3){
    tmrSwitchLR = millis();
    switch (ints[1]){
      case 0:
        servos.writeMicroseconds(1500);
      break;
      case 1:
        servos.writeMicroseconds(1000);
      break;
      case 2:
        servos.writeMicroseconds(2000);
      break;
    };
  };
  
};


void forward(int someSpeed){
  motors.smoothTick(255);

}

void backward(int someSpeed){
  motors.smoothTick(-255);

}

void chill(){
  motors.smoothTick(STOP);

}

void stopMotors(){
  motors.smoothTick(0);

};

/*  arduino_bridge.ino
    Para el intercambio de datos mediante protocolo modbus

    Autor: Claudio Morales Díaz @cmoralesd
    Versión: 1.0 - abril de 2025

    La transacción de datos se realiza mediante protocolo Modbus-RTU sobre Serial1 (USB) o Serial2 (pines 16-17)
    Requiere la librería modbus-esp8266 by Andre Sarmento Barbosa, versión 4.1.0
    https://github.com/emelianov/modbus-esp8266
    
*/

#include <ModbusRTU.h>

// Parámetros Modbus
#define BAUD_RATE     115200
#define SLAVE_ID      1 
#define COIL1   1001
#define COIL2   1002
#define REG1    4001
#define REG2    4002

ModbusRTU modbus;


void setup() {
  // inicializa comunicación y pines
  Serial.begin(115200, SERIAL_8N1);
  pinMode(LED_BUILTIN, OUTPUT);

  // inicializa registros Modbus
  modbus.begin(&Serial);
  modbus.slave(SLAVE_ID);
  modbus.addHreg(REG1);
  modbus.addHreg(REG2);
  modbus.Hreg(REG1, 0);
  modbus.Hreg(REG2, 32767);
  modbus.addCoil(COIL1, LOW);
  modbus.addCoil(COIL2, LOW);
}


void loop() {
  // realiza transacciones Modbus
  modbus.task();
  
  // vincula el estado del LED al valor del registro COIL1
  digitalWrite(LED_BUILTIN, modbus.Coil(COIL1));

  // actualiza el valor de los registros
  modbus.Hreg(REG1, millis()/1000);
  modbus.Hreg(REG2, 32767 - millis()/1000);

  delay(10);
}
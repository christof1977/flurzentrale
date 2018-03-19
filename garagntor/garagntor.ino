#include <ESP8266WiFi.h>
#include <ESP8266WiFiMulti.h>
#include <WiFiClient.h>
#include <ArduinoJson.h>
#include "credentials.h"


ESP8266WiFiMulti wifiMulti;
WiFiServer server(SERVERPORT);

WiFiClient client;

StaticJsonBuffer<300> JsonRxBuffer;
StaticJsonBuffer<300> JsonTxBuffer;

// define GPIO pins:
const int torTaster = 4;
const int torAufMeldung = 5;


void iosetup() {
  pinMode(torTaster, OUTPUT);
  pinMode(torAufMeldung, INPUT_PULLUP);

  // set outputs to low:
  digitalWrite(torTaster, LOW);
}

void wifisetup() {
  WiFi.mode(WIFI_STA);
  wifiMulti.addAP(SSID1, PASS);
  wifiMulti.addAP(SSID2, PASS);
  WiFi.hostname(HOSTNAME);
  Serial.println("Geht los jetzt ");
  while (wifiMulti.run() != WL_CONNECTED) {
    Serial.print(".");
    delay(500);
  }
  if (wifiMulti.run() == WL_CONNECTED) {
    Serial.println();
    Serial.println("Ich bin drin!");
    Serial.println("IP Adresse: ");
    Serial.println(WiFi.localIP());
  }
}

void setup() {
  Serial.begin(74880);
  Serial.println();
  Serial.println("Garagntorsteuerung");
  Serial.println("sld 03/2018");
  iosetup();
  wifisetup();
  server.begin();
  Serial.println("TCP server laaft!");
}


void loop() {
  client = server.available();
  const char* action;
  const char* parameter;
  const char* answer;
  int value;
  int stat;
  String content;

  if (client) {
    Serial.println("Da kummt was");
    String line = client.readStringUntil('\n');
    //Serial.println(line);
    JsonObject& parsed = JsonRxBuffer.parseObject(line);
    JsonObject& root = JsonTxBuffer.createObject();

    if (!parsed.success()) {
      Serial.println("Parsing failed");
      return;
    }
    action = parsed["Aktion"];
    parameter = parsed["Parameter"];
    value = parsed["Wert"];

    if (!strcmp(action, "Abfrage")) {
      root["Aktion"] = "Antwort";
      if (!strcmp(parameter, "Torstatus")) {
        stat = digitalRead(torAufMeldung);
        if (stat) {
          root["Parameter"] = "Zu";
        }
        else {
          root["Parameter"] = "Auf";
        }
      }
    }

    else if (!strcmp(action, "Kommando")) {
      root["Aktion"] = "Antwort";
      Serial.println("Kommando:");

      if (!strcmp(parameter, "TorAufZu")) {
        Serial.println("Tor auf! Oder zu!");
        digitalWrite(torTaster, HIGH);
        delay(1000);
        digitalWrite(torTaster, LOW);
        root["Parameter"] = "OK";
      }
      else {
        root["Parameter"] = "NOK";
      }
    }

    root.printTo(client);
    root.printTo(Serial);
    Serial.println();
  }
  JsonTxBuffer.clear();
  JsonRxBuffer.clear();
}


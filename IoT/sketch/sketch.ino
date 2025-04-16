#include <WiFi.h>
#include <HTTPClient.h>
#include "DHT.h"

const char* ssid = "SSID";
const char* password = "PASSWORD";

const char* serverName = "http://192.168.48.196:8000/sensor";

#define DHTPIN 21
#define DHTTYPE DHT22
#define DIMMER_PIN 23

DHT dht(DHTPIN, DHTTYPE);

void setup_wifi() {
  delay(10);
  Serial.println();
  Serial.print("Menghubungkan ke WiFi: ");
  Serial.println(ssid);

  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("");
  Serial.println("WiFi terkoneksi!");
  Serial.print("IP Address: ");
  Serial.println(WiFi.localIP());
}

void setup() {
  Serial.begin(115200);
  dht.begin();
  pinMode(DIMMER_PIN, OUTPUT);
  setup_wifi();
}

void loop() {
  float h = dht.readHumidity();
  float t = dht.readTemperature();

  if (isnan(h) || isnan(t)) {
    Serial.println("Gagal membaca DHT!");
    return;
  }

  Serial.print("Kelembaban: ");
  Serial.print(h);
  Serial.print(" %, Suhu: ");
  Serial.print(t);
  Serial.println(" °C");

  if (WiFi.status() == WL_CONNECTED) {
    HTTPClient http;
    http.begin(serverName);
    http.addHeader("Content-Type", "application/json");

    String jsonPayload = "{\"temperature\": " + String(t, 2) + 
                         ", \"humidity\": " + String(h, 2) + "}";

    int httpResponseCode = http.POST(jsonPayload);

    Serial.print("HTTP Response code: ");
    Serial.println(httpResponseCode);
    String response = http.getString();
    Serial.println(response);

    http.end();
  } else {
    Serial.println("WiFi tidak terhubung!");
  }

  if (t > 29.50) {
    digitalWrite(DIMMER_PIN, HIGH);
  } else {
    digitalWrite(DIMMER_PIN, LOW);
  }

  delay(2500);  
}
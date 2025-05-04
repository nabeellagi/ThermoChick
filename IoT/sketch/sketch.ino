#include <TinyGPS++.h>
#include <HardwareSerial.h>
#include <WiFi.h>
#include <HTTPClient.h>
#include <ArduinoJson.h>
#include "DHT.h"

const char* ssid = "WIFI";
const char* password = "PASSWORD";

const char* serverLocation = "http://192.168.60.19:8000/location?device_id=test";
const char* serverSensor = "http://192.168.60.19:8000/sensor?device_id=test";
const char* serverFlame = "http://192.168.60.19:8000/fire-detection?device_id=test";
const char* serverTemperatureSet = "http://192.168.60.19:8000/temperature-set?device_id=test";
const char* serverLamp = "http://192.168.60.19:8000/sensor/lamp?device_id=test";

#define FLAME_SENSOR_PIN 4  
#define LED_PIN 2           
#define DHTPIN 21
#define DHTTYPE DHT22
#define DIMMER_PIN 23

static const int RXPin = 18, TXPin = 19;
static const uint32_t GPSBaud = 9600;
TinyGPSPlus gps;
HardwareSerial gpsSerial(1);

DHT dht(DHTPIN, DHTTYPE);

float temperatureSetpoint = 29.50;  // default nilai awal

void setup() {
  Serial.begin(115200);

  pinMode(FLAME_SENSOR_PIN, INPUT);
  pinMode(LED_PIN, OUTPUT);
  pinMode(DIMMER_PIN, OUTPUT);

  gpsSerial.begin(GPSBaud, SERIAL_8N1, RXPin, TXPin);

  dht.begin();

  WiFi.begin(ssid, password);
  Serial.print("Menghubungkan ke WiFi");
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\nWiFi terhubung");
  Serial.print("IP Address: ");
  Serial.println(WiFi.localIP());
}

void loop() {
  int flameState = digitalRead(FLAME_SENSOR_PIN);
  if (flameState == LOW) {
    Serial.println("Api terdeteksi!");
    digitalWrite(LED_PIN, HIGH);
  } else {
    Serial.println("Tidak ada api.");
    digitalWrite(LED_PIN, LOW);
  }

  // Kirim data api ke server lokal
  if (WiFi.status() == WL_CONNECTED) {
    HTTPClient http;
    http.begin(serverFlame);
    http.addHeader("Content-Type", "application/json");

    String jsonPayload = "{\"fire_detected\": " + String(flameState == LOW ? "true" : "false") + "}";
    int httpResponseCode = http.POST(jsonPayload);
    Serial.print("Flame server response: ");
    Serial.println(httpResponseCode);
    if (httpResponseCode > 0) {
      String response = http.getString();
      Serial.println(response);
    }
    http.end();
  }

  // GET temperature setpoint dari server
  // GET temperature setpoint dari server
if (WiFi.status() == WL_CONNECTED) {
  HTTPClient http;
  http.begin(serverTemperatureSet);
  int httpResponseCode = http.GET();
  if (httpResponseCode == 200) {
    String payload = http.getString();
    Serial.print("Temperature setpoint response: ");
    Serial.println(payload);

    // Parsing JSON
    StaticJsonDocument<512> doc;
    DeserializationError error = deserializeJson(doc, payload);
    if (!error) {
      JsonObject data = doc["data"];
      if (data.containsKey("temperature")) {
        temperatureSetpoint = data["temperature"];
        Serial.print("Updated temperature setpoint: ");
        Serial.println(temperatureSetpoint);
      } else {
        Serial.println("Field 'temperature' tidak ditemukan di JSON!");
      }
    } else {
      Serial.println("Gagal parsing JSON setpoint!");
    }
  } else {
    Serial.print("GET setpoint failed, code: ");
    Serial.println(httpResponseCode);
  }
  http.end();
}


  while (gpsSerial.available() > 0) {
    gps.encode(gpsSerial.read());
  }

  if (gps.location.isUpdated()) {
    float latitude = gps.location.lat();
    float longitude = gps.location.lng();
    float altitude = gps.altitude.meters();
    int satellites = gps.satellites.value();

    Serial.printf("Latitude: %.6f, Longitude: %.6f, Altitude: %.2f m, Satellites: %d\n",
                  latitude, longitude, altitude, satellites);

    if (WiFi.status() == WL_CONNECTED) {
      HTTPClient http;
      http.begin(serverLocation);
      http.addHeader("Content-Type", "application/json");

      String jsonPayload = "{\"latitude\":" + String(latitude, 6) +
                           ",\"longitude\":" + String(longitude, 6) +
                           ",\"altitude\":" + String(altitude, 2) +
                           ",\"satellites\":" + String(satellites) +
                           ",\"flame_detected\":" + String(flameState == LOW ? "true" : "false") + "}";

      int httpResponseCode = http.POST(jsonPayload);
      Serial.print("Location server response: ");
      Serial.println(httpResponseCode);
      if (httpResponseCode > 0) {
        String response = http.getString();
        Serial.println(response);
      }
      http.end();
    }
  }

  float h = dht.readHumidity();
  float t = dht.readTemperature();

  if (!isnan(h) && !isnan(t)) {
    Serial.print("Kelembaban: ");
    Serial.print(h);
    Serial.print(" %, Suhu: ");
    Serial.print(t);
    Serial.println(" °C");

    if (WiFi.status() == WL_CONNECTED) {
      HTTPClient http;
      http.begin(serverSensor);
      http.addHeader("Content-Type", "application/json");

      String jsonPayload = "{\"device_id\": \"test\", \"temperature\": " + String(t, 2) +
                           ", \"humidity\": " + String(h, 2) + "}";

      int httpResponseCode = http.POST(jsonPayload);
      Serial.print("Sensor server response: ");
      Serial.println(httpResponseCode);
      if (httpResponseCode > 0) {
        String response = http.getString();
        Serial.println(response);
      }
      http.end();
    }

    if (t < temperatureSetpoint) {
      digitalWrite(DIMMER_PIN, HIGH);
      Serial.println("lampu nyala");
    } else {
      digitalWrite(DIMMER_PIN, LOW);
      Serial.println("lampu mati");
    }
  } else {
    Serial.println("Gagal membaca DHT!");
  }

  // Kirim status lampu ke server
if (WiFi.status() == WL_CONNECTED) {
  HTTPClient http;
  http.begin(serverLamp);
  http.addHeader("Content-Type", "application/json");

  String jsonPayload = "{\"device_id\": \"test\", \"lamp_state\": " + String(digitalRead(DIMMER_PIN) == HIGH ? "true" : "false") + "}";

  int httpResponseCode = http.POST(jsonPayload);
  Serial.print("Lamp server response: ");
  Serial.println(httpResponseCode);
  if (httpResponseCode > 0) {
    String response = http.getString();
    Serial.println(response);
  }
  http.end();
}

  delay(5000); 
}
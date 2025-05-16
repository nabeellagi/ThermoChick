#include <TinyGPS++.h>
#include <HardwareSerial.h>
#include <WiFi.h>
#include <HTTPClient.h>
#include <ArduinoJson.h>
#include "DHT.h"
#include <LittleFS.h>
#include <ESPAsyncWebServer.h>

// Server
AsyncWebServer server(80);

// WiFi Config
String ssid = "";
String pass = "";

// Config file paths
String ssidPath = "/ssid.txt";
String passPath = "/pass.txt";

// Endpoints
const char* serverLocation = "http://192.168.42.196:8000/location?device_id=test";
const char* serverSensor = "http://192.168.42.196:8000/sensor?device_id=test";
const char* serverFlame = "http://192.168.42.196:8000/fire-detection?device_id=test";
const char* serverTemperatureSet = "http://192.168.42.196:8000/temperature-set?device_id=test";
const char* serverLamp = "http://192.168.42.196:8000/sensor/lamp?device_id=test";

// Pins
#define FLAME_SENSOR_PIN 4
#define LED_PIN 2
#define DHTPIN 21
#define DHTTYPE DHT22
#define DIMMER_PIN 23

// GPS
static const int RXPin = 18, TXPin = 19;
static const uint32_t GPSBaud = 9600;
TinyGPSPlus gps;
HardwareSerial gpsSerial(1);

// DHT
DHT dht(DHTPIN, DHTTYPE);

// Temperature setpoint
float temperatureSetpoint = 29.50;

// Form input names
const char* PARAM_INPUT_1 = "ssid";
const char* PARAM_INPUT_2 = "pass";

// File read/write functions
String readFile(fs::FS &fs, const String &path) {
  File file = fs.open(path.c_str(), "r");
  if (!file || file.isDirectory()) return "";
  String content = file.readString();
  file.close();
  return content;
}

void writeFile(fs::FS &fs, const String &path, const String &content) {
  File file = fs.open(path.c_str(), "w");
  if (!file) return;
  file.print(content);
  file.close();
}

// WiFi connection logic
bool initWiFi() {
  if (ssid == "") {
    Serial.println("WiFi SSID kosong.");
    return false;
  }

  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid.c_str(), pass.c_str());

  Serial.print("Mencoba konek ke WiFi: ");
  Serial.println(ssid);

  unsigned long startAttemptTime = millis();
  while (WiFi.status() != WL_CONNECTED && millis() - startAttemptTime < 10000) {
    Serial.print(".");
    delay(500);
  }

  if (WiFi.status() == WL_CONNECTED) {
    Serial.println("\nBerhasil konek WiFi!");
    Serial.print("Alamat IP: ");
    Serial.println(WiFi.localIP());
    return true;
  } else {
    Serial.println("\nGagal konek WiFi.");
    return false;
  }
}

void setup() {
  Serial.begin(115200);
  pinMode(FLAME_SENSOR_PIN, INPUT);
  pinMode(LED_PIN, OUTPUT);
  pinMode(DIMMER_PIN, OUTPUT);

  gpsSerial.begin(GPSBaud, SERIAL_8N1, RXPin, TXPin);

  dht.begin();

  if (!LittleFS.begin()) {
    Serial.println("Gagal mount LittleFS");
    return;
  }

  ssid = readFile(LittleFS, ssidPath);
  Serial.println("SSID: " + ssid);
  pass = readFile(LittleFS, passPath);
  Serial.println("Password: " + pass);

  if (!initWiFi()) {
    Serial.println("Gagal konek WiFi. Membuat Access Point...");
    WiFi.softAP("ThermoFarm Setel WiFi");
    IPAddress IP = WiFi.softAPIP();
    Serial.print("Alamat AP: ");
    Serial.println(IP);

    server.on("/", HTTP_GET, [](AsyncWebServerRequest *request) {
      request->send(LittleFS, "/index.html", "text/html");
    });

    server.on("/success", HTTP_GET, [](AsyncWebServerRequest *request) {
      request->send(LittleFS, "/success.html", "text/html");
    });

    server.on("/bulma.min.css", HTTP_GET, [](AsyncWebServerRequest *request) {
      request->send(LittleFS, "/bulma.min.css", "text/css");
    });

    server.on("/nerd.png", HTTP_GET, [](AsyncWebServerRequest *request){
      request->send(LittleFS, "/nerd.png", "image/png");
    });


    // Mount POST handler regardless of WiFi mode
    server.on("/", HTTP_POST, [](AsyncWebServerRequest *request) {
      int params = request->params();
      for (int i = 0; i < params; i++) {
        const AsyncWebParameter* p = request->getParam(i);
        if (p->isPost()) {
          if (p->name() == PARAM_INPUT_1) {
            ssid = p->value().c_str();
            writeFile(LittleFS, ssidPath, ssid);
          }
          if (p->name() == PARAM_INPUT_2) {
            pass = p->value().c_str();
            writeFile(LittleFS, passPath, pass);
          }
        }
      }

      // 🔁 Try connecting with new credentials
      WiFi.begin(ssid.c_str(), pass.c_str());

      unsigned long startAttemptTime = millis();
      bool wifiConnected = false;
      while (millis() - startAttemptTime < 5000) {  // wait up to 5 seconds
        if (WiFi.status() == WL_CONNECTED) {
          wifiConnected = true;
          break;
        }
        delay(500);
      }

      if (wifiConnected) {
        Serial.println("WiFi berhasil disambungkan dari POST!");
        request->send(LittleFS, "/success.html", "text/html");

        // Restart ESP to apply WiFi
        xTaskCreate(
          [](void* param) {
            delay(3000);
            ESP.restart();
          },
          "RestartTask",
          2048,
          NULL,
          1,
          NULL
        );
      } else {
        Serial.println("Gagal konek dengan kredensial baru!");
        request->send(LittleFS, "/error.html", "text/html");
      }
    });


  } else {
    Serial.println("WiFi Terkoneksi: " + WiFi.localIP().toString());
  }
  server.begin();
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
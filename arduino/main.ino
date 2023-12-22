#include <ESP8266WiFi.h>
#include <PubSubClient.h>
#include <Adafruit_NeoPixel.h>
#include "config.h"

const char* clientId = ("ESP8266-" + String(random(0xffff), HEX)).c_str();
const char* topic = "RICKASTLEY";
WiFiClient espClient;
PubSubClient client(espClient);
Adafruit_NeoPixel strip(6, D1, NEO_GRB + NEO_KHZ800);

// Song Data
String song_name = "";
String song_artist = "";
String colours[5] = {"","","",""};
float sections_start[BUFFER_SIZE_SECTIONS]  = {};
float sections_vol[BUFFER_SIZE_SECTIONS] = {};
float segments[BUFFER_SIZE_SEGMENTS] = {};
float beats[BUFFER_SIZE_BEATS] = {};
float beat_duration = 0;
int sections_iter = 0;
int segs_iter = 0;
int beats_iter = 0;

void setup() {
  Serial.begin(115200);
  delay(10);

  WiFi.begin("MYHDSB");

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
  }

  Serial.println("Connected to MYHDSB");
  Serial.print("Assigned IP address: ");
  Serial.println(WiFi.localIP());

  client.setServer(MQTT_SERVER, MQTT_PORT);
  client.setCallback(callback);

  while (!client.connected()) {
    if (client.connect(clientId, MQTT_USERNAME, MQTT_PASSWORD)) {
      Serial.println("Connected to MQTT broker");
      client.subscribe(topic);
      setStripColor(strip.Color(0,255,0));
    } else {
      delay(5000);
    }
  }
}

void loop() {
  if (!client.connected()) {
    reconnect();
  }
  client.loop();
}

void callback(char* topic, byte* payload, unsigned int length) {
  String message = "";
  for (int i = 0; i < length; i++) {
    message += (char)payload[i];
  }

  Serial.println("Message arrived [");
  Serial.print(message);
  Serial.println("] ");

  if (message == "START_PROCESSING") {
    Serial.println("New Song incoming");
  }
  else{
    // Get Switching character
    String firstLetter = message.substring(0,1);
    String payload = message.substring(2);

    // Conditional Logic for each type of message

    // Song Name
    if(firstLetter == "1"){
      // Song Name
      song_name = payload;
      Serial.println("Song Name Identified : " + payload);
    }

    // Artist Name
    else if(firstLetter == "2"){
      // Artist Name
      song_artist = payload;
      Serial.println("Song Artist Identified : " + payload);
    }

    // Colors
    else if(firstLetter == "3"){
      // Color. We need the index as well
      int colorIndex = payload.substring(0,1).toInt();
      colours[colorIndex] = payload.substring(2);
      Serial.println("Song Color Identified : " + payload.substring(2));
    }

    // Sections
    else if(firstLetter == "4"){
      // Sections.
      String switcher = payload.substring(0,1);
      if(switcher == "S"){
        // We're starting the sections
        sections_iter = 0;
        Serial.println("Starting Section Processing");
      }
      else if(switcher == "N"){
        String act = payload.substring(2);
        int switcher_2 = act.substring(0,1).toInt();
        String content = act.substring(2);
        sections_start[switcher_2] = content.toFloat();
        Serial.println("Added starting time : " + content);
      }
      else if(switcher == "M"){
        String act = payload.substring(2);
        int switcher_2 = act.substring(0,1).toInt();
        String content = act.substring(2);
        sections_vol[switcher_2] = content.toFloat();
        Serial.println("Added volume : " + content);
      }
    }
  }
}

void setStripColor(uint32_t color) {
  for (int i = 0; i < strip.numPixels(); i++) {
    strip.setPixelColor(i, color);
  }
  strip.show();
}

void reconnect() {
  while (!client.connected()) {
    if (client.connect(clientId, MQTT_USERNAME, MQTT_PASSWORD)) {
      Serial.println("Reconnected to MQTT broker");
      client.subscribe(topic);
    } else {
      delay(5000);
    }
  }
}
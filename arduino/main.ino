#include <ESP8266WiFi.h>
#include <PubSubClient.h>
#include <Adafruit_NeoPixel.h>
#include <LiquidCrystal_I2C.h>

// Define LCD properties
LiquidCrystal_I2C lcd(0x27, 16, 2);

// WIFI ID
const char* WifiID = "MYHDSB";

// Mqtt Configuration
const char* MQTT_SERVER = "awesome-fisher.cloudmqtt.com";
const int MQTT_PORT = 1883;
const char* MQTT_USERNAME = "gkvpckep";
const char* MQTT_PASSWORD = "yGbZQKc8MAma";

// Client ID
const char* clientId = ("ESP8266-" + String(random(0xffff), HEX)).c_str();

// Topic to subscribe to using MQTT
const char* topic = "RICKASTLEY";

// Wifi Client
WiFiClient espClient;

// PubSubClient for MQTT
PubSubClient client(espClient);

// Strip1 (TODO : ADD MORE STRIPS)
Adafruit_NeoPixel strip1(6, D6, NEO_GRB + NEO_KHZ800);

// Song Data
// Colors of the Song
String colours[5] = {"","","",""};

// Section Start Times
int sections_start[500];

// Beats
int beats[500];

// Lyrics (the lyrics_start are the times, the lyrics are the strings)
int lyrics_start[500];
String lyrics[500];

// Iters
int sections_iter = 0;
int beats_iter = 0;
int lyrics_iter = 0;

// Current lyric, beat, secton and Color
int curLyric = -1;
int curBeat = -1;
int curSection = -1;
String curColor = "";

// Running bool
bool running = false;

// Start period of the song
int startMS = 0;

// Setup
void setup() {
  // Start Serial Communication
  Serial.begin(115200);
  delay(10);

  // Connect to Wifi
  WiFi.begin(WifiID);

  // While we aren't connected, stop.
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
  }

  // Serial print message once we connect
  Serial.println("Connected to MYHDSB");
  Serial.print("Assigned IP address: ");
  Serial.println(WiFi.localIP());

  // Connect to MQTT
  client.setServer(MQTT_SERVER, MQTT_PORT);
  client.setCallback(callback);

  // Initialize the LCD
  lcd.init();

  // Clear the screen
  lcd.clear();
  lcd.backlight();
  lcd.print("Waiting for Song...");

  // While our client isn't connected, try to connect
  while (!client.connected()) {
    // Try to connect
    if (client.connect(clientId, MQTT_USERNAME, MQTT_PASSWORD)) {
      Serial.println("Reconnected to MQTT broker");

      // Subscribe to our topic
      client.subscribe(topic);
    } else {
      // Retry after certain duration
      delay(5000);
    }
  }
}

// Set Strip to certain color
void setStripColor(uint32_t color) {
  // Set the color each pixel by each pixel
  for (int i = 0; i < strip1.numPixels(); i++) {
    strip1.setPixelColor(i, color);
  }

  // Light up the strip
  strip1.show();
}

// Function to display text on the LCD with wrapping and trimming
void displayText(String text) {
  // Clear the LCD screen
  lcd.clear();

  // Define maximum characters per line and maximum characters for both lines
  int maxCharsPerLine = 16;
  int maxCharsTotal = 32;

  // Check if the text length exceeds the maximum allowed
  if (text.length() > maxCharsTotal) {
    // Trim the text and add '..' at the end
    text = text.substring(0, maxCharsTotal - 2) + "..";
  }

  // Display the text on the LCD
  int remainingChars = text.length();
  int currentLine = 0;

  // Loop until all characters are displayed
  while (remainingChars > 0) {
    // Calculate the number of characters to display on the current line
    int charsToDisplay = min(remainingChars, maxCharsPerLine);

    // Get the substring for the current line
    String lineText = text.substring(text.length() - remainingChars, text.length() - remainingChars + charsToDisplay);

    // Print the substring on the LCD
    lcd.setCursor(0, currentLine);
    lcd.print(lineText);

    // Update the remaining characters and move to the next line
    remainingChars -= charsToDisplay;
    currentLine++;

    // If there are remaining characters, move to the next line
    if (remainingChars > 0) {
      lcd.setCursor(0, currentLine);
    }
  }
}

// Function to convert Color Code to RGB
void convertToRGB(String text){
// TO DO : ADD CODE TO CONVERT HEX TO RGB
}

void loop() {
  // If we aren't connected, reconnect
  if (!client.connected()) {
    reconnect();
  }

  // Loop function for esp8266
  client.loop();

  // If we're running, do the millisocond calculation
  if(running == true){
    // Calculate time elapsed
    long time = millis() - startMS;
    Serial.println(time);

    // Check for events
    // If we're past a certain lyric's starting, display that
    if(lyrics_start[curLyric + 1] <= time && lyrics_start != 0){
      // Write the lyric
      displayText(lyrics[curLyric + 1]);
      curLyric += 1;
    }

    // If we're past a certain beat's starting, light our strip up
    if(beats[curBeat + 1] <= time && beats[curBeat] != 0){
      // TO DO : MAKE THE MQTT THINGS LIGHT UP WITH COLOR
      setStripColor(strip1.Color(255,255,255));
    }
    else{
      // Make it not light up
      setStripColor(strip1.Color(0,0,0));
    }

    // TO DO : WHEN SECTIONS CHANGE, CHANGE THE COLOR
    if(sections_start[curSection + 1] <= time && sections_start[curSection] != 0){
      // Change the Color
    }
  }
}

void callback(char* topic, byte* payload, unsigned int length) {
  // Receieve Message
  String message = "";
  for (int i = 0; i < length; i++) {
    message += (char)payload[i];
  }

  // Print it to the Serial
  Serial.println("Message arrived [");
  Serial.print(message);
  Serial.println("] ");

  // If our message was to start processing
  if (message == "START_PROCESSING") {
    Serial.println("New Song incoming");

    // Re-initialize all of the values
    curLyric = 0;
    curBeat = 0;
    curSection = 0;
    sections_iter = 0;
    beats_iter = 0;
    lyrics_iter = 0;
  }
  else if(message == "STOP"){
    // Start the Loop
    startMS = millis();
    running = true;
  }
  else{
    // Get Switching character
    String firstLetter = message.substring(0,1);

    // Get message payload after the first letter.
    String payload = message.substring(2);

    // Conditional Logic for each type of message
    // Colors
    if(firstLetter == "3"){
      // Color. We need the index as well, so extract that first.
      int colorIndex = payload.substring(0,1).toInt();
      colours[colorIndex] = payload.substring(2);

      // Serial
      Serial.println("Song Color Identified : " + payload.substring(2));
    }

    // Sections
    if(firstLetter == "4"){
      // Assign value
      sections_start[sections_iter] = payload.toInt();

      // increment the iters variable, i.e the 'index' of the array we need to assign the next value to.
      sections_iter += 1;
    }

    // Beats
    if(firstLetter == "5"){
      // Assign value
      beats[beats_iter] = payload.toInt();

      // increment the iters variable, i.e the 'index' of the array we need to assign the next value to.
      beats_iter += 1;
    }

    // Lyrics
    if(firstLetter == "6"){
      // Assign value
      lyrics_start[lyrics_iter] = payload.toInt();
    }
    if(firstLetter = "7"){
      // Assign value
      lyrics[lyrics_iter] = payload;

      // increment the iters variable, i.e the 'index' of the array we need to assign the next value to.
      lyrics_iter += 1;
    }
  }
}

void reconnect() {
  // While our client isn't connected, try to connect
  while (!client.connected()) {
    // Try to connect
    if (client.connect(clientId, MQTT_USERNAME, MQTT_PASSWORD)) {
      Serial.println("Reconnected to MQTT broker");

      // Subscribe to our topic
      client.subscribe(topic);
    } else {
      // Retry after certain duration
      delay(5000);
    }
  }
}
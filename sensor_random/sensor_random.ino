//Program used to emulate sensor with random number
#include <ESP8266HTTPClient.h>
#include <ESP8266WiFi.h>
#include <ArduinoJson.h>

long randNumber;
 
void setup() {
  Serial.begin(115200);                             //Serial connection
  WiFi.begin("SINGTEL-F997", "aishiweilo");         //WiFi connection

  Serial.println("Waiting for connection");
  while (WiFi.status() != WL_CONNECTED) {           //Wait for the WiFI connection completion
    delay(500);
    Serial.print(".");
  }
}   //end of void setup() ===================================================================

void loop() {
//Construct JSON data
//Pass JSON data to server with POST method
  if (WiFi.status() == WL_CONNECTED) { //Check WiFi connection status
      randNumber = random(50);
      
      StaticJsonBuffer<300> JSONbuffer;   //Declaring static JSON buffer
      JsonObject& JSONencoder = JSONbuffer.createObject(); 
      JSONencoder["sensorType"] = "Temperature";
      JsonArray& values = JSONencoder.createNestedArray("values"); //JSON array
      values.add(randNumber); //Add value to array

      char JSONmessageBuffer[300];
      JSONencoder.prettyPrintTo(JSONmessageBuffer, sizeof(JSONmessageBuffer));
      Serial.println(JSONmessageBuffer);
  
      HTTPClient http;                                    //Declare object of class HTTPClient
 
      http.begin("http://192.168.1.77:5000/postjson");    //Specify request destination
      http.addHeader("Content-Type", "application/json"); //Specify content-type header
   
      int httpCode = http.POST(JSONmessageBuffer);        //Send the request
      String payload = http.getString();                  //Get the response payload
   
      Serial.println(httpCode);                           //Print HTTP return code
      Serial.println(payload);                            //Print request response payload
   
      http.end();                                         //Close connection
  } else {
      Serial.println("Error in WiFi connection");
  }
  delay(60000);                                           //Send a request every 60 seconds

 
}  // end of void loop() ===================================================================

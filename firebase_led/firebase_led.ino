#include <ESP8266WiFi.h>
#include <WiFiClient.h>
#include <MySQL_Connection.h>

IPAddress server_addr(192,168,1,13);
char user[] = "ESP8266";
char password[] = "passwd";
char ssid[] = "Wi-Fi";
char pass[] = "120302";

WiFiClient client;
MySQL_Connection conn((Client *)&client);

void setup() {
        Serial.begin(115200);
       WiFi.begin(ssid, pass);
       
       while ( WiFi.status() != WL_CONNECTED ) {
              delay ( 500 );
              Serial.print ( "." );
       }
       
       Serial.println ( "" );
       Serial.print ( "Connected to " );
       Serial.println ( ssid );
       Serial.print ( "IP address: " );
       Serial.println ( WiFi.localIP() );
     
       Serial.println("DB - Connecting...");
     
}

void loop(){

  while (conn.connect(server_addr, 3306, user, password) != true) {
              delay(500);
              Serial.print ( "." );
              String url = String("connectDB/display_mysql.php");
              client.println(String("GET") + url +  "HTTP/1.1\r\n" +  "\r\n" +
               "Connection: close\r\n\r\n");
       }

 
  delay(1000);
 
 
  while(client.available()){
    String line = client.readStringUntil('\r');
    Serial.print(line);
  }

   
  Serial.println();
  Serial.println("connection closed");

  delay(30000);
 
}

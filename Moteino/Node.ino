// Sample RFM69 sender/node sketch, with ACK and optional encryption
// Sends periodic messages of increasing length to gateway (id=1)
// It also looks for an onboard FLASH chip, if present
// Library and code by Felix Rusu - felix@lowpowerlab.com
// Get the RFM69 and SPIFlash library at: https://github.com/LowPowerLab/

#include <RFM69.h>    //get it here: https://www.github.com/lowpowerlab/rfm69
#include <SPI.h>
#include <SPIFlash.h> //get it here: https://www.github.com/lowpowerlab/spiflash
#include <DHT.h>	  // Adafruit DHT library
#include <LowPower.h> // Low power library

#define NODEID        2    //unique for each node on same network
#define NETWORKID     100  //the same on all nodes that talk to each other
#define GATEWAYID     1
#define FREQUENCY   RF69_868MHZ
#define ENCRYPTKEY    "sampleEncryptKey" //exactly the same 16 characters/bytes on all nodes!
#define ACK_TIME      30 // max # of ms to wait for an ack
#define LED           9 // Moteinos have LEDs on D9

#define SEND_LOOPS   75 //send data this many sleep loops (15 loops of 8sec cycles = 120sec ~ 2 minutes)
//*********************************************************************************************
#define SLEEP_FASTEST SLEEP_15Ms
#define SLEEP_FAST SLEEP_250Ms
#define SLEEP_SEC SLEEP_1S
#define SLEEP_LONG SLEEP_2S
#define SLEEP_LONGER SLEEP_4S
#define SLEEP_LONGEST SLEEP_8S
period_t sleepTime = SLEEP_SEC; //period_t is an enum type defined in the LowPower library (LowPower.h)
//*********************************************************************************************

#define SERIAL_BAUD   115200

#define DHT_PIN 3
#define DHT_TYPE DHT22

// Set up the DHT sensor
DHT dht(DHT_PIN, DHT_TYPE);

int TRANSMITPERIOD = 3000; //transmit a packet to gateway so often (in ms)
char buff[20];
byte sendSize=0;
boolean requestACK = false;
RFM69 radio;
byte sendLoops=0;
char id[] = "ABC";

void setup() {
  Serial.begin(SERIAL_BAUD);
  radio.initialize(FREQUENCY,NODEID,NETWORKID);
  radio.encrypt(ENCRYPTKEY);
  char buff[50];
  sprintf(buff, "\nTransmitting at %d Mhz...", FREQUENCY==RF69_433MHZ ? 433 : FREQUENCY==RF69_868MHZ ? 868 : 915);
  Serial.println(buff);
}

void loop() {
  //check for any received packets
  if (radio.receiveDone())
  {
    Serial.print('[');Serial.print(radio.SENDERID, DEC);Serial.print("] ");
    for (byte i = 0; i < radio.DATALEN; i++)
      Serial.print((char)radio.DATA[i]);
    Serial.print("   [RX_RSSI:");Serial.print(radio.RSSI);Serial.print("]");

    if (radio.ACKRequested())
    {
      radio.sendACK();
      Serial.print(" - ACK sent");
    }
    Serial.println();
  }

  if (sendLoops--<=0)
  {
    sendLoops = SEND_LOOPS-1;
    
    delay(2000); // dht-22 appears to need this long to power up
    
    float h = dht.readHumidity();
	// Read temperature as Celsius (the default)
	float t = dht.readTemperature();
	
	  // Check if any reads failed and exit early (to try again).
	if (isnan(h) || isnan(t) ) {
	  Serial.println("Failed to read from DHT sensor!");
	  return;
	}
	
	Serial.print("H: ");
	Serial.print(h);
	Serial.print(" %\t");
	Serial.print("T: ");
	Serial.print(t);
	Serial.print("\n");
	
	// Data should be sent in json format: {"id": "ABC", "temp": 25.4}
	  
	char sendStuff[] = "{\"id\": \"ABC\", \"temp\": 25.4}";
	char floatbuffer[5];
	dtostrf(t, 3, 1, floatbuffer);
	
	sprintf(sendStuff, "{\"id\": \"%s\", \"temp\":%s}", id, floatbuffer);
	Serial.println(sendStuff);
	  
      if (radio.sendWithRetry(GATEWAYID, sendStuff, strlen(sendStuff)))
       Serial.print(" ok!");
  }
  
  radio.sleep(); //you can comment out this line if you want this node to listen for wireless programming requests
  LowPower.powerDown(SLEEP_8S, ADC_OFF, BOD_OFF);
}
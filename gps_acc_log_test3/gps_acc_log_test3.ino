#include <Wire.h> // Needed for I2C to GNSS
#include <SparkFun_u-blox_GNSS_v3.h> // http://librarymanager/All#SparkFun_u-blox_GNSS_v3

SFE_UBLOX_GNSS myGNSS;

void setup()
{
  delay(1000);

  Serial.begin(115200);
  Serial.println("SparkFun u-blox example");

  Wire.begin();

  if (myGNSS.begin(Wire) == false) // Connect to the u-blox module using Wire port
  {
    Serial.println(F("u-blox GNSS not detected at default I2C address. Please check wiring. Freezing."));
    while (1);
  }

  // 設定更新頻率為 20Hz
  if (myGNSS.setNavigationFrequency(20)) // 設定更新頻率為 20Hz
  {
    Serial.println("Successfully set navigation frequency to 20Hz.");
  }
  else
  {
    Serial.println("Failed to set navigation frequency!");
  }

  // 驗證當前更新頻率
  byte currentRate;
  if (myGNSS.getNavigationFrequency(&currentRate))
  {
    Serial.print("Current navigation frequency: ");
    Serial.print(currentRate);
    Serial.println(" Hz");
  }
  else
  {
    Serial.println("Failed to get navigation frequency!");
  }

  //  myGNSS.setI2COutput(COM_TYPE_UBX); // Set the I2C port to output UBX only
  myGNSS.setI2COutput(COM_TYPE_NMEA); // 設定 I2C 為輸出 NMEA
  myGNSS.setNavigationFrequency(5, VAL_LAYER_RAM); // Set output to 5 times a second
}

void loop()
{
  // Query module. The module only responds when a new position or time is available
  if (myGNSS.getPVT())
  {
    uint16_t year = myGNSS.getYear();
    uint8_t month = myGNSS.getMonth();
    uint8_t day = myGNSS.getDay();
    uint8_t hour = myGNSS.getHour();
    uint8_t minute = myGNSS.getMinute();
    uint8_t second = myGNSS.getSecond();
    uint16_t millisecond = myGNSS.getMillisecond();
    uint8_t numSats = myGNSS.getSIV();
    double latitude = myGNSS.getLatitude() / 1e7;  // Convert to degrees
    double longitude = myGNSS.getLongitude() / 1e7; // Convert to degrees
    uint32_t hAcc = myGNSS.getHorizontalAccuracy(); // Horizontal accuracy in mm
    uint32_t vAcc = myGNSS.getVerticalAccuracy();   // Vertical accuracy in mm
    if (numSats == 0) {
      //        flag = true;
    }
    hour = hour + 8;

    float fractionalSecond = millisecond / 1000.0;

    double t0 = millis() * 0.001;
    Serial.printf("Date: %04d-%02d-%02d, Time: %02d:%02d:%06.3f\n", year, month, day, hour, minute, second + fractionalSecond);
    Serial.printf("Satellites: %d\n", numSats);
    Serial.printf("Latitude: %.7f, Longitude: %.7f\n", latitude, longitude);
    Serial.printf("Horizontal Accuracy: %.1f m, Vertical Accuracy: %.1f m\n", hAcc / 1000.0, vAcc / 1000.0); // Convert mm to meters
    String datedata = String(t0, 3) + "," + String(hour) + ":" +  String(minute) + ":" +  String(second + fractionalSecond, 3);
    Serial.printf("time,gpstime : ");
    Serial.println(datedata);
  }
}

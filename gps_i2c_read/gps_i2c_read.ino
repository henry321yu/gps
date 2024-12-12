#include <Wire.h> // Needed for I2C to GNSS
#include <SparkFun_u-blox_GNSS_v3.h> // http://librarymanager/All#SparkFun_u-blox_GNSS_v3

SFE_UBLOX_GNSS myGNSS;

void setup()
{
  delay(1000);

  Serial.begin(115200);
  Wire.begin();

  if (myGNSS.begin(Wire) == false) // Connect to the u-blox module using Wire port
  {
    Serial.println(F("u-blox GNSS not detected at default I2C address. Please check wiring. Freezing."));
    while (1);
  }
  myGNSS.setI2COutput(COM_TYPE_NMEA); // 設定 I2C 為輸出 NMEA

  // 設定更新頻率
  setgpsrate(5);
}

void loop()
{
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
    uint8_t fixType = myGNSS.getFixType();
    if (numSats == 0) {
      //        flag = true;
    }
    hour = hour + 8;

    float fractionalSecond = millisecond / 1000.0;

    double t0 = millis() * 0.001;

    //    Serial.printf("time : %.3f,Date: %04d-%02d-%02d, Time: %02d:%02d:%06.3f ,Satellites: %d ,Latitude: %.7f, Longitude: %.7f,Horizontal Accuracy: %.1f m, Vertical Accuracy: %.1f m\n", t0, year, month, day, hour, minute, second + fractionalSecond, numSats, latitude, longitude, hAcc / 1000.0, vAcc / 1000.0);
    Serial.printf("%.3f,%04d-%02d-%02d,%02d:%02d:%06.3f,%d,%.7f,%.7f,%.1f,%.1f,%d\n", t0, year, month, day, hour, minute, second + fractionalSecond, numSats, latitude, longitude, hAcc / 1000.0, vAcc / 1000.0, fixType);

    String datedata = String(t0, 3) + "," + String(hour) + ":" +  String(minute) + ":" +  String(second + fractionalSecond, 3);
    //    Serial.println(datedata);
  }
}

void setgpsrate(int rate) {
  if (myGNSS.setNavigationFrequency(rate, VAL_LAYER_RAM)) // 設定更新頻率
  {
    Serial.printf("Successfully set navigation frequency to %d Hz.\n", rate);
  }
  else
  {
    Serial.println("Failed to set navigation frequency!");
  }

  // 驗證當前更新頻率
  byte currentRate;
  if (myGNSS.getNavigationFrequency(&currentRate))
  {
    Serial.printf("Current navigation frequency: %d Hz \n", currentRate);
  }
  else
  {
    Serial.println("Failed to get navigation frequency!");
  }
}

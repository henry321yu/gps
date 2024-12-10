#include <Wire.h>

#define ZED_I2C_ADDR 0x42  // ZED-F9P 的 I2C 位址

void setup() {
  Serial.begin(115200);
  Wire.begin();  // 初始化 I2C
  delay(1000);
  Serial.println("Starting GPS Time Reading...");
}

void loop() {
  uint8_t buffer[32];
  
  // 請求 UBX NAV-TIMEUTC 資料
  uint8_t navTimeUtc[] = {
    0xB5, 0x62,         // UBX header
    0x01, 0x21,         // NAV-TIMEUTC message class and ID
    0x00, 0x00,         // Payload length (0 for polling)
    0x22, 0x67          // Checksum (預計)
  };

  // 發送 UBX NAV-TIMEUTC Polling
  Wire.beginTransmission(ZED_I2C_ADDR);
  Wire.write(navTimeUtc, sizeof(navTimeUtc));
  Wire.endTransmission();

  delay(100); // 等待模組回應

  // 讀取返回的 UBX 資料
  Wire.requestFrom(ZED_I2C_ADDR, sizeof(buffer));
  int idx = 0;
  while (Wire.available()) {
    buffer[idx++] = Wire.read();
  }

  // 解析 NAV-TIMEUTC 回應資料
//  if (idx > 16 && buffer[2] == 0x01 && buffer[3] == 0x21) {
  if (idx > 16) {
    uint32_t iTOW = *((uint32_t*)&buffer[6]); // GPS Time of Week
    uint16_t year = *((uint16_t*)&buffer[10]);
    uint8_t month = buffer[12];
    uint8_t day = buffer[13];
    uint8_t hour = buffer[14];
    uint8_t min = buffer[15];
    uint8_t sec = buffer[16];
    uint8_t valid = buffer[17];
    uint32_t nano = *((uint32_t*)&buffer[18]); // NAV-TIMEUTC 的 nano 字段
    float fractional_sec = nano / 1e9;         // 轉換為小數秒

    if (valid & 0x04) { // Check if time is valid
      Serial.printf("UTC Time: %04d-%02d-%02d %02d:%02d:%02d.%03d\n",
              year, month, day, hour, min, sec, nano / 1000000);
    } else {
      Serial.println("UTC Time is not valid.");
    }
  } else {
    Serial.println("Failed to get NAV-TIMEUTC response.");
  }

//  delay(1000);
}

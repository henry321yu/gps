#include <Arduino.h>
#include <TimeLib.h>
#include <SoftwareSerial.h>
#include <SparkFun_u-blox_GNSS_v3.h> // http://librarymanager/All#SparkFun_u-blox_GNSS_v3
#include <Wire.h>
#include <SD.h>

SoftwareSerial HC12(7, 8);
SFE_UBLOX_GNSS myGNSS;

// small board change:sd,led,beeper,hall,mpu6050 set&read tcaselect(2)
const int mag_I2c = 0x0c; //
const int MPU_addr = 0x68;
const int SD_CS = 10; // teensy builtin
const int beeper = 4;
const int mRD = 21;
int ID, delayy = 2000, setF = 100;
long values[20], t[12];
double x[3], y[3], z[3], gx[3], gy[3], gz[3], xm[7], ym[7], zm[7], t0, timee = 0, f = 100, f2, tm[7], ta[3], tg, temp[5]; //, x1, y1, z1
String logFileName, accdata, gyrdata, magdata, logdata, mag2data, tmdata, halldata, datedata, datadate, gpsdata, gpstime;            // Rotordata;
unsigned long i = 0, t1, beepert;
int maxsize = 52428000;//104857600 =100mb 52428000 =50mb 31457280=30mb 209715200=200mb 262144000=250mb = 250*2^20; 50mb for power_sensor_90393、yan_gps
File logFile;
String fileName;
int Addr;
int wireread = A3;
int a = 0, lasta = 0;
int thb1, b1, lastb1, thb2, b2, lastb2, thb3, b3, lastb3;
double tt[10];
long ii = 500; long iii = 1000;
int setpin = 9;
String mon, dayy;
bool flag = true, setT = true;
int gyear, gmonth, gday, ghour, gminute, numSats, fixType;
double gsecond, secondn, latitude, longitude, altitude, hAcc, vAcc;
bool readgg = true;
byte readggt;
double gpsms;

void setup()
{
  Serial.begin(115200); // Initialize serial output via USB
  delay(100);
  Serial.println(F("Serial.begin"));
  Serial.println(F("SPI.begin"));
  SPI.begin();
  delay(100);

  Serial.println(F("Wire.begin"));
  Wire.begin();
  Wire.setClock(400000); // 設定 I2C 頻率

  Serial.println(F("HC12.begin"));
  HC12.begin(115200);
  pinMode(setpin, OUTPUT);
  digitalWrite(setpin, LOW);
  delay(100);
  HC12.print("AT+B115200");
  delay(100);
  HC12.print("AT+C117"); //117 mag sensor
  delay(100);
  HC12.print("AT+P8");
  delay(100);
  digitalWrite(setpin, HIGH);

  Serial.println(F("HC12.set"));
  while (HC12.available()) {
    Serial.write(HC12.read());
  }

  //f9p setup
  Serial.println(F("f9p.set"));
  if (myGNSS.begin(Wire) == false) // Connect to the u-blox module using Wire port
  {
    Serial.println(F("u-blox GNSS not detected at default I2C address. Please check wiring. Freezing."));
    //    while (1);
  }
  myGNSS.setI2COutput(COM_TYPE_NMEA); // 設定 I2C 為輸出 NMEA
  // 設定更新頻率
  //  setgpsrate(5);

  Serial.println(F("SD.begin"));
  if (!SD.begin(SD_CS)) {
    Serial.println(F("Card failed, or not present"));
  }

  while (!SD.begin(SD_CS)) {
    Serial.println(F("Card failed, or not present"));
    digitalWrite(beeper, HIGH);
    delay(500);
    digitalWrite(beeper, LOW);
    delay(500);
  }
  
  while (!Serial && millis() < 4000 );
  Serial.println("\n" __FILE__ " " __DATE__ " " __TIME__);
  setSyncProvider(getTeensy3Time);
  
  Serial.println(F("file.set"));
  mon = String(month());
  dayy = String(day());
  if (mon.length() < 2) {
    mon = "0" + mon;
  }
  if (dayy.length() < 2) {
    dayy = "0" + dayy;
  }
  datadate = mon + dayy;
  logFileName = nextLogFile_date();
  Serial.println(logFileName);
  logFile = SD.open(logFileName, FILE_WRITE);
  if (logFile) {
    //Serial.println(F("writing"));
  }
  // if the file didn't open, print an error:
  else {
    Serial.println(F("error opening file"));
    while (1);
  }

}

void loop()
{
  readgps();
  timee = millis() * 0.001;

  gpstime = String(ghour) + ":" +  String(gminute) + ":" +  String(gsecond);
  gpsdata = String(latitude, 8) + "," + String(longitude, 8) + "," + String(altitude, 4) + "," + String(numSats) + "," + String(fixType) + "," + String(hAcc) + "," + String(vAcc);
  logdata = String(timee, 3) + "," + gpstime + "," + gpsdata;

  Serial.println(logdata);

  //  delayy = 1000;
  delayMicroseconds(delayy);
  savesd(logdata);
}

void readgps() {
  digitalWrite(beeper, HIGH);
  if (myGNSS.getPVT())
  {
    gyear = myGNSS.getYear();
    gmonth = myGNSS.getMonth();
    gday = myGNSS.getDay();
    ghour = myGNSS.getHour();
    gminute = myGNSS.getMinute();
    gsecond = myGNSS.getSecond();
    uint16_t millisecond = myGNSS.getMillisecond();
    numSats = myGNSS.getSIV();
    latitude = myGNSS.getLatitude() / 1e7;  // Convert to degrees
    longitude = myGNSS.getLongitude() / 1e7; // Convert to degrees
    altitude = myGNSS.getAltitude();
    hAcc = myGNSS.getHorizontalAccuracy(); // Horizontal accuracy in mm
    vAcc = myGNSS.getVerticalAccuracy();   // Vertical accuracy in mm
    fixType = myGNSS.getFixType();

    gpsms = millisecond / 1000.0;
    gsecond = gsecond + gpsms;
    ghour = ghour + 8;
    altitude = altitude / 1000; // Convert to m
    hAcc = hAcc / 1000;
    vAcc = vAcc / 1000;
    if (ghour > 24)
      ghour -= 24;

    if (setT == true) {
      gsecond = round(gsecond); //使四捨五入小數點
      // 假設 RTC 時間是以 UTC 時間為基準
      time_t settime = makeTime({
        gsecond, gminute, ghour, gday, gmonth - 1, gyear - 1970 // makeTime 接收的 month 範圍為 0-11，year 要減去 1970
      });
      // 設定 RTC 時間
      setTime(settime);
      setT = false;
    }
    if (readggt >= 5) {
      readggt = 0;
      //      digitalWrite(beeper, LOW);
      //      readgg = false;
    }
    else {
      readggt += 1;
    }
  }
}

String nextLogFile_date(void) {
  String filename;
  int logn = 0;
  for (int i = 0; i < 999; i++) {
    filename = datadate + "_" + String(logn) + "p" + String(".csv");
    if (!SD.exists(filename))    {
      return filename;
    }
    logn++;
  }
  return "";
}

time_t getTeensy3Time() {
  return Teensy3Clock.get();
}

void savesd(String savedata) {
  if (!logFile) {
    logFile = SD.open(logFileName, FILE_WRITE);
  }

  if (logFile) {
    logFile.println(savedata);    
    logFile.close(); // close the file
  }
  else {
    Serial.println("error opening test.txt");
  }
}

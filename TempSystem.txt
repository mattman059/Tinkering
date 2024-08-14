1. Arduino Setup
The Arduino will read the temperature sensor's analog data and send it over serial communication to the Raspberry Pi.

Arduino Code:
cpp
[code]
const int sensorPin = A0;  // Analog input pin for the temperature sensor

void setup() {
  Serial.begin(9600);  // Start serial communication at 9600 baud
}

void loop() {
  int analogValue = analogRead(sensorPin);  // Read the analog value from the sensor

  // Convert the analog value to a voltage (assuming 5V reference)
  float voltage = analogValue * (5.0 / 1023.0);

  // Convert the voltage to temperature (for LM35: 10mV per degree Celsius)
  float temperatureC = voltage * 100.0;

  // Send the temperature value over Serial to the Raspberry Pi
  Serial.println(temperatureC);

  delay(1000);  // Wait 1 second before the next reading
}
[/code]
2. Raspberry Pi Setup
a. Read Data from the Arduino
The Raspberry Pi will read the data sent by the Arduino over the serial port and log it to a file.

Python Script to Read and Log Data:
python
[code]
import serial
import time

# Configure serial port
ser = serial.Serial('/dev/ttyUSB0', 9600)  # Adjust to the correct port if different
log_file = '/home/pi/temperature_log.txt'

def log_temperature():
    with open(log_file, 'a') as f:
        while True:
            try:
                if ser.in_waiting > 0:
                    temperature = ser.readline().decode('utf-8').strip()
                    timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
                    f.write(f"{timestamp}, {temperature}\n")
                    f.flush()
                    print(f"Logged: {temperature}°C at {timestamp}")
                time.sleep(5)  # Log every 5 seconds
            except KeyboardInterrupt:
                print("Logging stopped.")
                break

if __name__ == "__main__":
    log_temperature()

[/code]
Serial Communication: Ensure the correct serial port is specified (/dev/ttyUSB0 is common, but it might differ on your setup).
b. Hosting a Web Server
Use Flask to create a simple web server that reads the most recent temperature from the log file and displays it.

Python Flask Web Server:
python

[code]
from flask import Flask
import time

app = Flask(__name__)
log_file = '/home/pi/temperature_log.txt'

def get_latest_temperature():
    try:
        with open(log_file, 'r') as f:
            lines = f.readlines()
            if lines:
                return lines[-1].strip().split(', ')[-1]
            else:
                return "No data available"
    except FileNotFoundError:
        return "Log file not found"

@app.route('/')
def index():
    temp = get_latest_temperature()
    return f"<h1>Current Temperature: {temp}°C</h1>"

if __name__ == '__main__':
    app.run(host='10.0.0.10', port=9999)
[/code]
Explanation:
get_latest_temperature(): Reads the last line from the log file to get the most recent temperature reading.
Flask Web Server: Hosts the server on 10.0.0.10:9999.
c. Running the Flask Server
To run the Flask server:

Install Flask if it's not already installed:
bash
Copy code
pip install flask
Run the Flask app:
bash
Copy code
python3 your_flask_script.py
3. System Integration
Connection: Connect the Arduino to the Raspberry Pi via a USB cable.
Data Logging: The Raspberry Pi will continuously read data from the Arduino and log it to a file.
Web Access: Access the temperature readings on the Raspberry Pi's IP at http://10.0.0.10:9999/.
Summary
Arduino: Reads analog data and sends it via serial.
Raspberry Pi: Logs data and serves it on a web interface every 5 seconds.

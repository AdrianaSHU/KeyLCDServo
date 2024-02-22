# Import necessary modules
from myservo import Servo
from keypad import KeyPad
from machine import Pin, I2C
from I2C_LCD import I2CLcd
import time

# Define the I2C interface with specified pin assignments
i2c = I2C(1, sda=Pin(14), scl=Pin(15), freq=400000)

# Define the pins for LEDs and buzzer
redLed = Pin(17, Pin.OUT)
greenLed = Pin(16, Pin.OUT)
activeBuzzer = Pin(28, Pin.OUT)

# Define the servo motor with Pin 18
servo = Servo(18)
servo.ServoAngle(0)  # Ensure servo is initially closed

# Define the password
password = "1234"
keyIn = ""
wrong_attempts = 0

# Initialize keypad and LCD once
keyPad = KeyPad(13, 12, 11, 10, 9, 8, 7, 6)
devices = i2c.scan()
if devices:
    lcd = I2CLcd(i2c, devices[0], 2, 16)
    lcd.move_to(0, 0)
    lcd.putstr("Enter password:")
    lcd.move_to(0, 1)
    lcd.putstr("")
else:
    print("No address found")

# Define a function to read keypad input and produce a beep sound
def read_keypad():
    keyvalue = keyPad.scan()
    if keyvalue is not None:
        activeBuzzer.on()
        time.sleep_ms(100)
        activeBuzzer.off()
        return keyvalue

# Main loop
try:
    while True:
        redLed.on()  # Turn on the red LED
        time.sleep(0.3)
        redLed.off()  # Turn off the red LED
        time.sleep(0.3)
        keydata = read_keypad()
        if keydata is not None:
            keyIn += keydata 
            lcd.putstr(keydata)  # Display the entered number on LCD
            if len(keyIn) == 4:
                if keyIn == password:
                    lcd.move_to(0, 1)
                    lcd.putstr("" * 16)  # Clear previous message
                    lcd.move_to(0, 1)
                    lcd.putstr("Correct Password")
                    greenLed.on()
                    servo.ServoAngle(180)  # Move servo to open position
                    time.sleep_ms(1000)
                    time.sleep(2)
                    servo.ServoAngle(0)  # Move servo to closed position
                    greenLed.off()
                    time.sleep(1)  # Wait for 1 second
                    lcd.clear() # Reset the LCD display
                    lcd.move_to(0, 0)
                    lcd.putstr("Enter password: ")
                    keyIn = ""  # Reset keyIn for the next input
                    wrong_attempts = 0  # Reset wrong attempts counter
                else:
                    if wrong_attempts == 0:  # First wrong attempt
                        lcd.clear()  # Clear LCD
                        lcd.move_to(0, 0)  # Move cursor to first line
                        lcd.putstr("Second attempt: ")  # Display "Second attempt" message
                        lcd.move_to(0, 1)  # Move cursor to second line
                        lcd.putstr("")
                    else:
                        lcd.move_to(0, 1)
                        lcd.putstr("" * 16)  # Clear previous message
                        lcd.move_to(0, 1)
                        lcd.putstr("")
                    redLed.on()  # Turn on the red LED
                    activeBuzzer.on()  # Activate the buzzer
                    time.sleep(1)
                    redLed.off()
                    activeBuzzer.off()
                    keyIn = ""  # Reset keyIn for the next input
                    wrong_attempts += 1
                    if wrong_attempts == 2:  # Check if two wrong attempts have occurred
                        lcd.clear()
                        lcd.move_to(0, 0)
                        lcd.putstr("2 WRONG ATTEMPTS")
                        lcd.move_to(0, 1)
                        lcd.putstr("Wait for: ")
                        count = 20
                        while count >= 0:
                            lcd.move_to(10, 1)
                            lcd.putstr("%2d" % count)
                            time.sleep(1)
                            count -= 1
                        lcd.clear()  # Clear the LCD after countdown
                        lcd.move_to(0, 0)
                        lcd.putstr("Enter password: ")
                        wrong_attempts = 0  # Reset wrong attempts counter
                        activeBuzzer.on()  # Activate the buzzer briefly
                        time.sleep(0.5)  # Wait for a short duration
                        activeBuzzer.off()  # Deactivate the buzzer

except KeyboardInterrupt:
    pass
except Exception as e:
    print("An error occurred:", e)
finally:
    # Release resources
    redLed.off()
    greenLed.off()
    activeBuzzer.off()


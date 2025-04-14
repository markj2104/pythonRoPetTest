import RPi.GPIO as GPIO
import time
import random
import pygame

# GPIO pin setup
TOUCH_PIN = 17
SERVO_TAIL = 18
SERVO_HEAD = 13

GPIO.setmode(GPIO.BCM)
GPIO.setup(TOUCH_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(SERVO_TAIL, GPIO.OUT)
GPIO.setup(SERVO_HEAD, GPIO.OUT)

# Set up PWM for servos
tail_servo = GPIO.PWM(SERVO_TAIL, 50)
head_servo = GPIO.PWM(SERVO_HEAD, 50)
tail_servo.start(0)
head_servo.start(0)

# Initialize pygame for sound
pygame.mixer.init()
pygame.mixer.music.set_volume(1.0)

# List of sound files
sound_files = [
    "0001.wav", "0002.wav", "0003.wav",
    "0004.wav", "0007.wav", "0009.wav", "0010.wav"
]

def play_random_sound():
    sound_file = random.choice(sound_files)
    print(f"Playing: {sound_file}")
    sound = pygame.mixer.Sound(sound_file)
    sound.play()
    while pygame.mixer.get_busy():
        time.sleep(0.1)

def move_tail():
    print("Wagging tail...")
    tail_servo.ChangeDutyCycle(7.5)  # Center
    time.sleep(0.3)
    tail_servo.ChangeDutyCycle(5.5)  # Left
    time.sleep(0.4)
    tail_servo.ChangeDutyCycle(9.5)  # Right
    time.sleep(0.4)
    tail_servo.ChangeDutyCycle(7.5)  # Back to center
    time.sleep(0.3)
    tail_servo.ChangeDutyCycle(0)    # Stop signal

def move_head():
    print("Turning head...")
    head_servo.ChangeDutyCycle(6.5)
    time.sleep(0.4)
    head_servo.ChangeDutyCycle(8.5)
    time.sleep(0.4)
    head_servo.ChangeDutyCycle(7.5)
    time.sleep(0.3)
    head_servo.ChangeDutyCycle(0)

def cat_interaction():
    print("Cat interaction triggered!")
    play_random_sound()
    move_head()
    move_tail()

print("Robotic Cat Ready. Waiting for touch...")

try:
    while True:
        if GPIO.input(TOUCH_PIN) == GPIO.LOW:
            cat_interaction()
            # Wait for touch to be released before reactivating
            while GPIO.input(TOUCH_PIN) == GPIO.LOW:
                time.sleep(0.05)
        time.sleep(0.1)
except KeyboardInterrupt:
    print("Shutting down...")
finally:
    tail_servo.stop()
    head_servo.stop()
    GPIO.cleanup()

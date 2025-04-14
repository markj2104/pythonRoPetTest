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
    "0004.wav", "0007.wav", "0009.wav"
]

# Default head movement
def move_head_default():
    print("Turning head (default)...")
    head_servo.ChangeDutyCycle(6.5)
    time.sleep(0.4)
    head_servo.ChangeDutyCycle(8.5)
    time.sleep(0.4)
    head_servo.ChangeDutyCycle(7.5)
    time.sleep(0.3)
    head_servo.ChangeDutyCycle(0)

# Default tail movement
def move_tail_default():
    print("Wagging tail (default)...")
    tail_servo.ChangeDutyCycle(7.5)
    time.sleep(0.3)
    tail_servo.ChangeDutyCycle(5.5)
    time.sleep(0.4)
    tail_servo.ChangeDutyCycle(9.5)
    time.sleep(0.4)
    tail_servo.ChangeDutyCycle(7.5)
    time.sleep(0.3)
    tail_servo.ChangeDutyCycle(0)

# Alternate movement patterns for variety
def move_head_nod():
    print("Head nodding...")
    for _ in range(2):
        head_servo.ChangeDutyCycle(6.5)
        time.sleep(0.2)
        head_servo.ChangeDutyCycle(8.5)
        time.sleep(0.2)
    head_servo.ChangeDutyCycle(7.5)
    time.sleep(0.2)
    head_servo.ChangeDutyCycle(0)

def move_tail_quick():
    print("Tail quick flick...")
    tail_servo.ChangeDutyCycle(5.5)
    time.sleep(0.2)
    tail_servo.ChangeDutyCycle(9.5)
    time.sleep(0.2)
    tail_servo.ChangeDutyCycle(7.5)
    time.sleep(0.2)
    tail_servo.ChangeDutyCycle(0)

def move_tail_slow():
    print("Tail slow sweep...")
    tail_servo.ChangeDutyCycle(6.0)
    time.sleep(0.6)
    tail_servo.ChangeDutyCycle(9.0)
    time.sleep(0.6)
    tail_servo.ChangeDutyCycle(7.5)
    time.sleep(0.4)
    tail_servo.ChangeDutyCycle(0)

def move_head_slow_turn():
    print("Slow head turn...")
    head_servo.ChangeDutyCycle(8.5)
    time.sleep(0.6)
    head_servo.ChangeDutyCycle(6.5)
    time.sleep(0.6)
    head_servo.ChangeDutyCycle(7.5)
    time.sleep(0.4)
    head_servo.ChangeDutyCycle(0)

# Mapping sounds to movement patterns
def get_movement_pattern(sound_file):
    return {
        "0001.wav": (move_head_default, move_tail_quick),
        "0002.wav": (move_head_nod, move_tail_default),
        "0003.wav": (move_head_slow_turn, move_tail_slow),
        "0004.wav": (move_head_nod, move_tail_quick),
        "0007.wav": (move_head_default, move_tail_default),
        "0009.wav": (move_head_slow_turn, move_tail_quick)
    }.get(sound_file, (move_head_default, move_tail_default))

def play_random_sound():
    sound_file = random.choice(sound_files)
    print(f"Playing: {sound_file}")
    sound = pygame.mixer.Sound(sound_file)
    sound.play()
    return sound_file

def cat_interaction():
    print("Cat interaction triggered!")
    sound_file = play_random_sound()
    head_move, tail_move = get_movement_pattern(sound_file)
    head_move()
    tail_move()
    while pygame.mixer.get_busy():
        time.sleep(0.1)

print("Robotic Cat Ready. Waiting for touch...")

try:
    while True:
        if GPIO.input(TOUCH_PIN) == GPIO.LOW:
            cat_interaction()
            while GPIO.input(TOUCH_PIN) == GPIO.LOW:
                time.sleep(0.05)
        time.sleep(0.1)
except KeyboardInterrupt:
    print("Shutting down...")
finally:
    tail_servo.stop()
    head_servo.stop()
    GPIO.cleanup()

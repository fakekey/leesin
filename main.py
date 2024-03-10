from pynput import keyboard
from os import system
from pystyle import Colors
from time import sleep
from threading import Thread

keyboard_controller = keyboard.Controller()
is_auto_ward_w = False
is_auto_ward_flash_w = False
is_comboing = False


def combo_thread(func):
    def wrapper():
        func()
    thread = Thread(target=wrapper)
    thread.start()


def combo_ward_w():
    global is_comboing
    is_comboing = True
    sleep(0.02)
    for i in range(20):
        keyboard_controller.press('w')
        sleep(0.01)
        keyboard_controller.release('w')
    is_comboing = False


def combo_ward_flash_w():
    global is_comboing
    is_comboing = True
    sleep(0.02)
    keyboard_controller.press('f')
    keyboard_controller.release('f')
    for i in range(20):
        keyboard_controller.press('w')
        sleep(0.01)
        keyboard_controller.release('w')
    is_comboing = False


def on_press(key):
    global is_auto_ward_w, is_auto_ward_flash_w, is_comboing
    if key == keyboard.Key.left and not is_auto_ward_w:
        is_auto_ward_w = True
        is_auto_ward_flash_w = False
        print(Colors.yellow, "Auto Ward W on")
    elif key == keyboard.Key.right and not is_auto_ward_flash_w:
        is_auto_ward_flash_w = True
        is_auto_ward_w = False
        print(Colors.yellow, "Auto Ward Flash W on")
    elif key == keyboard.Key.down and (is_auto_ward_w or is_auto_ward_flash_w):
        is_auto_ward_w = is_auto_ward_flash_w = False
        print(Colors.red, "Stopped all")
    elif isinstance(key, keyboard.KeyCode) and key.char in ('2', '4'):
        if is_comboing:
            return
        if is_auto_ward_w:
            combo_thread(combo_ward_w)
        elif is_auto_ward_flash_w:
            combo_thread(combo_ward_flash_w)


def main():
    system("title Nghị Hack")
    with keyboard.Listener(on_press=on_press) as listener:
        print(Colors.yellow, "Please place wards in 2 and 4")
        print(Colors.green, "Press ← (Left Arrow) to Auto Ward W")
        print(Colors.green, "Press → (Right Arrow) to Auto Ward Flash W")
        print(Colors.red, "Press ↓ (Down Arrow) to Stop all")
        listener.join()


if __name__ == "__main__":
    main()

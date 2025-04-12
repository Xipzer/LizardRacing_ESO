import cv2
import numpy as np
import pyautogui
import time
import random
import win32gui

# Load template images
e_talk_template = cv2.imread('images/e_talk.png', 0)  # For "E Talk" Prompt
goodbye_template = cv2.imread('images/goodbye.png', 0)  # For "Goodbye" Dialogue
whats_lizard_racing_template = cv2.imread('images/whats_lizard_racing.png', 0)  # For "What's Lizard Racing" Dialogue
thanks_template = cv2.imread('images/thanks.png', 0)  # For "Thanks" Dialogue
try_again_template = cv2.imread('images/try_again.png', 0)  # For "Try Again" Dialogue
lizard_racing_template = cv2.imread('images/lizard_racing_quest.png', 0)  # For "Lizard Racing" Quest Name In Your Journal

# Define screen regions (adjust these based on your game window)
e_talk_region = (1062, 611, 93, 37)  # (x, y, width, height) For "E Talk" Prompt
goodbye_region = (1074, 555, 96, 32)  # (x, y, width, height) For "Goodbye" Dialogue
whats_lizard_racing_region = (1078, 560, 201, 24)  # (x, y, width, height) For "What's Lizard Racing" Dialogue
thanks_region = (1072, 552, 84, 37)  # (x, y, width, height) For "Thanks" Dialogue
try_again_region = (1073, 555, 151, 34)  # (x, y, width, height) For "Try Again" Dialogue
journal_region = (1029, 462, 125, 30)  # (x, y, width, height) For "Lizard Racing" Quest Name In Your Journal

# Image matching threshold
MATCH_THRESHOLD = 0.65

def press_key(key, times=1):
    """Press a key a specified number of times with random delays."""
    for _ in range(times):
        pyautogui.press(key)
        time.sleep(random.uniform(0.075, 0.15))

def hold_key(key, duration):
    """Hold a key for a specified duration."""
    pyautogui.keyDown(key)
    time.sleep(duration)
    pyautogui.keyUp(key)

def move_character():
    """Perform a random movement to simulate player activity."""
    movements = [
        ('s', 'd'),  # Down and right
        ('d', 's'),  # Right and down
    ]
    move_pair = random.choice(movements)  # Randomly pick a movement pair
    duration = random.uniform(0.01, 0.02)   # Random duration between 0.01 and 0.02 seconds

    print(f"Moving {move_pair[0]} for {duration:.2f}s, then {move_pair[1]} for {duration * 0.65:.2f}s")
    hold_key(move_pair[0], duration)  # Move in one direction
    time.sleep(random.uniform(0.01, 0.02))  # Brief pause
    hold_key(move_pair[1], duration * 0.65)  # Return to original position

def wait_with_movement(wait_time):
    """Wait for a specified time with a random movement during the period."""
    move_time = random.uniform(2, wait_time - 2)  # Random time to move (leaving buffer)
    time.sleep(move_time)  # Wait until movement
    move_character()       # Perform the movement
    time.sleep(wait_time - move_time)  # Wait the remaining time

def detect_template(screen, template):
    """Detect if a template is present in the screen region."""
    screen_gray = cv2.cvtColor(np.array(screen), cv2.COLOR_RGB2GRAY)
    result = cv2.matchTemplate(screen_gray, template, cv2.TM_CCOEFF_NORMED)
    return np.max(result) >= MATCH_THRESHOLD

def interact_with_npc():
    """Interact with the NPC by pressing 'E'."""
    print("Interacting with NPC...")
    press_key('e')
    time.sleep(1)  # Wait for dialogue to appear

def analyze_dialogue():
    """Analyze the dialogue to determine quest state."""
    if detect_template(pyautogui.screenshot(region=whats_lizard_racing_region), whats_lizard_racing_template):
        print("Detected 'What's Lizard Racing?' - Starting quest.")
        return "start"
    elif detect_template(pyautogui.screenshot(region=thanks_region), thanks_template):
        print("Detected 'Thanks.' - Quest succeeded.")
        return "success"
    elif detect_template(pyautogui.screenshot(region=try_again_region), try_again_template):
        print("Detected 'Can I try again?' - Quest failed.")
        return "failure"
    elif detect_template(pyautogui.screenshot(region=goodbye_region), goodbye_template):
        print("Detected 'Goodbye.' - Quest in progress.")
        return "goodbye"
    else:
        print("Unknown dialogue detected.")
        return "unknown"

def start_quest():
    """Start the 'Lizard Racing' quest by navigating dialogue."""
    print("Starting 'Lizard Racing' quest...")
    press_key('e', 5)  # Navigate through initial dialogue to start the race

def retry_quest():
    """Retry the 'Lizard Racing' quest after failure."""
    print("Retrying 'Lizard Racing' quest...")
    press_key('e', 5)  # Select 'Can I try again?' and start again

def turn_in_quest():
    """Turn in the 'Lizard Racing' quest after success."""
    print("Turning in and restarting 'Lizard Racing' quest...")
    press_key('e', 7)  # Select 'Thanks.' to complete

def abandon_quest():
    """Abandon the 'Lizard Racing' quest."""
    print("Quest stuck. Abandoning 'Lizard Racing'...")
    press_key('j')  # Open journal
    time.sleep(random.uniform(0.075, 0.15))

    # Cycle through quests to find "Lizard Racing"
    max_attempts = 25
    for _ in range(max_attempts):
        journal_screen = pyautogui.screenshot(region=journal_region)
        if detect_template(journal_screen, lizard_racing_template):
            break
        press_key('t')  # Cycle quests
        time.sleep(random.uniform(0.075, 0.15))
    else:
        print("Error: 'Lizard Racing' not found in journal.")
        press_key('alt')  # Close journal
        return False

    # Abandon and confirm
    press_key('x')  # Abandon quest
    time.sleep(random.uniform(0.075, 0.15))
    press_key('e')  # Confirm
    time.sleep(random.uniform(0.075, 0.15))
    press_key('alt')  # Close journal
    print("Quest abandoned successfully.")
    return True

def get_game_window_hwnd():
    """Find the window handle (hwnd) of the Elder Scrolls Online window."""
    def callback(hwnd, hwnds):
        if win32gui.IsWindowVisible(hwnd) and "Elder Scrolls Online" in win32gui.GetWindowText(hwnd):
            hwnds.append(hwnd)
        return True

    hwnds = []
    win32gui.EnumWindows(callback, hwnds)
    return hwnds[0] if hwnds else None

def is_game_focused(game_hwnd):
    """Check if the game window is currently focused."""
    return win32gui.GetForegroundWindow() == game_hwnd

# Main loop
quest_fail = 0
quest_success = 0
print("Lizard Racing bot started. Press Ctrl+C to stop.")

try:
    while True:
        # Wait for the game window to appear
        print("Waiting for the Elder Scrolls Online window to appear...")
        while True:
            game_hwnd = get_game_window_hwnd()
            if game_hwnd:
                break
            time.sleep(5)

        # Wait for the user to focus the game window
        print("Game window found. Please focus the game window to start the bot.")
        start_time = time.time()
        while not is_game_focused(game_hwnd):
            if time.time() - start_time > 60:
                print("Timeout: Game window not focused within 60 seconds.")
                exit()
            time.sleep(1)

        print("Game window is focused. Starting bot functionality.")
        print("Please ensure the game window remains focused during bot operation.")

        # Wait for "E Talk" prompt
        print("Waiting for 'E Talk' prompt...")
        while True:
            screen = pyautogui.screenshot(region=e_talk_region)
            if detect_template(screen, e_talk_template):
                break
            time.sleep(1)

        # Initiate interaction with NPC
        interact_with_npc()
        quest_start_time = time.time()
        state = analyze_dialogue()

        if state == "start" or state == "failure":
            start_quest()
            print("Quest in progress...")
            wait_with_movement(13)  # Wait for race to complete with movement
            while True:
                interact_with_npc()
                state = analyze_dialogue()
                if state == "success":
                    quest_success += 1
                    print("Successful Quests:", quest_success)
                    turn_in_quest()
                    quest_start_time = time.time()
                    wait_with_movement(13)  # Wait for next cycle with movement
                elif state == "failure":
                    quest_fail += 1
                    print("Failed Quests:", quest_fail)
                    retry_quest()
                    quest_start_time = time.time()
                    wait_with_movement(13)  # Wait for retry with movement
                elif state == "goodbye" and time.time() - quest_start_time > 30:
                    print("Quest stuck after 30 seconds with 'Goodbye.'")
                    abandon_quest()
                    break
                elif state == "unknown" and time.time() - quest_start_time > 30:
                    print("Quest stuck after 30 seconds with unknown dialogue.")
                    abandon_quest()
                    break
                time.sleep(2)
        elif state == "goodbye":
            print("NPC reset detected. Waiting for next cycle...")
        else:
            print("Unexpected state. Waiting for next cycle...")

        # Delay before next cycle
        time.sleep(random.uniform(2, 5))

except KeyboardInterrupt:
    print("\nPrinting results...")
    print("Successful Quests:", quest_success)
    print("Failed Quests:", quest_fail)
    print("\nBot stopped by user.")
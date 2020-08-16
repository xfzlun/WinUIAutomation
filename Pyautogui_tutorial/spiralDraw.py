# In OS X system, I use paint Expert for testing
import pyautogui, time
time.sleep(5)  # 5secs for 
pyautogui.click()  # we need click mouse left button on target window to switch activated window
distance = 200
while distance > 0:
    pyautogui.dragRel(distance, 0, duration = 1, button = 'left')  # move right
    distance = distance - 5
    pyautogui.dragRel(0, distance, duration = 1, button= 'left')  # move down
    distance = distance - 5
    pyautogui.dragRel(-distance, 0, duration = 1, button = 'left')  # move left 
    distance = distance - 5
    pyautogui.dragRel(0, -distance, duration = 1, button = 'left')  # move up



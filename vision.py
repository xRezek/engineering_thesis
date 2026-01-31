import cv2 as cv
import mediapipe as mp
from datetime import datetime
from collections import deque
import pymysql

session_start = datetime.now()
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7, max_num_hands=2)
mp_draw = mp.solutions.drawing_utils
db = pymysql.connect(host='localhost', user='root', password='', database='engineering_thesis')
cursor = db.cursor()

CORRECT_SEQUENCE = [1, 2, 3]

zones = {
    1: {'coords': (100, 150, 300, 350), 'color': (0, 255, 0), 'name': 'STREFA 1'},
    2: {'coords': (500, 150, 700, 350), 'color': (255, 255, 0), 'name': 'STREFA 2'},
    3: {'coords': (900, 150, 1100, 350), 'color': (0, 0, 255), 'name': 'STREFA 3'}
}

history = deque(maxlen=10)
current_zone = None
last_zone = None
last_log_time = None
zone_time = None

stats = {'entries': 0, 'errors': 0, 'sequences': 0, 'visits': {1: 0, 2: 0, 3: 0}}

cap = cv.VideoCapture(0)
cap.set(cv.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv.CAP_PROP_FRAME_HEIGHT, 720)

print("="*60)
print("SYSTEM DETEKCJI - STREFY")
print(f"Prawidlowa sekwencja: {' -> '.join(map(str, CORRECT_SEQUENCE))}")
print("="*60)
print("q - wyjscie, r - reset")
print("="*60)

while True:
    ret, frame = cap.read()
    if not ret:
        break
    
    frame = cv.rotate(frame, cv.ROTATE_180)
    frame_rgb = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
    
    current_zone = None
    
    results = hands.process(frame_rgb)
    h, w = frame.shape[:2]
    
    if results.multi_hand_landmarks:
        for hand_lm in results.multi_hand_landmarks:
            
            for conn in mp_hands.HAND_CONNECTIONS:
                s = hand_lm.landmark[conn[0]]
                e = hand_lm.landmark[conn[1]]
                sx, sy = int(s.x*w), int(s.y*h)
                ex, ey = int(e.x*w), int(e.y*h)
                cv.line(frame, (sx, sy), (ex, ey), (0, 255, 0), 2)
            
            for lm in hand_lm.landmark:
                x, y = int(lm.x*w), int(lm.y*h)
                cv.circle(frame, (x, y), 3, (255, 255, 0), -1)
            
            idx = hand_lm.landmark[8]
            fx, fy = int(idx.x*w), int(idx.y*h)
            cv.circle(frame, (fx, fy), 12, (255, 0, 255), -1)
            
            for zid, zdata in zones.items():
                x1, y1, x2, y2 = zdata['coords']
                if x1 <= fx <= x2 and y1 <= fy <= y2:
                    now = datetime.now()
                    
                    if current_zone != zid:
                        if last_log_time:
                            diff = (now - last_log_time).total_seconds()
                            if diff < 1.0:
                                break
                        
                        expected_next = None
                        if len(history) < len(CORRECT_SEQUENCE):
                            expected_next = CORRECT_SEQUENCE[len(history)]
                        
                        if expected_next and zid != expected_next:
                            stats['errors'] += 1
                            print(f"[{now.strftime('%H:%M:%S')}] [ERROR] Zla strefa! Oczekiwano {expected_next}, otrzymano {zid}")
                            print(f"[{now.strftime('%H:%M:%S')}] [ERROR] Prawidlowa kolejnosc: {' -> '.join(map(str, CORRECT_SEQUENCE))}")
                            cursor.execute("INSERT INTO errors (id, message, created_at) VALUES (NULL, %s, CURRENT_TIMESTAMP())",(f"Zla strefa! Oczekiwano {expected_next}, otrzymano {zid}",))
                            db.commit()
                        
                        history.append(zid)
                        stats['entries'] += 1
                        stats['visits'][zid] += 1
                        last_zone = zid
                        zone_time = now
                        last_log_time = now
                        current_zone = zid
                        
                        if expected_next and zid == expected_next:
                            print(f"[{now.strftime('%H:%M:%S')}] [OK] Prawidlowe wejscie do strefy {zid}")
                        else:
                            print(f"[{now.strftime('%H:%M:%S')}] [INFO] Wejscie do strefy {zid}")
                        
                        if len(history) >= len(CORRECT_SEQUENCE):
                            last_seq = list(history)[-len(CORRECT_SEQUENCE):]
                            if last_seq == CORRECT_SEQUENCE:
                                stats['sequences'] += 1
                                print(f"[{now.strftime('%H:%M:%S')}] [SUCCESS] Prawidlowa sekwencja: {' -> '.join(map(str, CORRECT_SEQUENCE))}!")
                                history.clear()
                                last_zone = None
                    break
    
    for zid, zdata in zones.items():
        x1, y1, x2, y2 = zdata['coords']
        col = zdata['color']
        thick = 4 if zid == current_zone else 2
        cv.rectangle(frame, (x1, y1), (x2, y2), col, thick)
        lbl = f"{zdata['name']} ({stats['visits'][zid]})"
        cv.putText(frame, lbl, (x1, y1-10), cv.FONT_HERSHEY_SIMPLEX, 0.7, col, 2)
    
    y = 420
    info = [
        "=== STATYSTYKI ===",
        f"Sekwencja: {' -> '.join(map(str, CORRECT_SEQUENCE))}",
        f"Wejscia: {stats['entries']}",
        f"Prawidlowe sekwencje: {stats['sequences']}",
        f"Bledy: {stats['errors']}",
        f"Historia: {' -> '.join(map(str, list(history)[-8:]))}"
    ]
    for i, txt in enumerate(info):
        cv.putText(frame, txt, (10, y+i*28), cv.FONT_HERSHEY_SIMPLEX, 0.55, (0,0,0), 2)
    
    cv.imshow('Hand Zones', frame)
    
    key = cv.waitKey(1) & 0xFF
    if key == ord('q'):
        cursor.execute("INSERT INTO session_summaries (id, entries, errors, correct_sequences, start, end) " \
        "VALUES (NULL, %s, %s, %s, %s, CURRENT_TIMESTAMP())",
        (int(stats['entries']),int(stats['errors']), int(stats['sequences']), session_start.strftime('%Y-%m-%d %H:%M:%S')))
        db.commit()
        cursor.close()
        db.close()
        break
    elif key == ord('r'):
        cursor.execute("INSERT INTO session_summaries (id, entries, errors, correct_sequences, start, end) " \
        "VALUES (NULL, %s, %s, %s, %s, CURRENT_TIMESTAMP())",
        (int(stats['entries']), int(stats['errors']), int(stats['sequences']), session_start.strftime('%Y-%m-%d %H:%M:%S')))
        db.commit()
        session_start = datetime.now()
        history.clear()
        current_zone = None
        last_zone = None
        last_log_time = None
        stats = {'entries': 0, 'errors': 0, 'sequences': 0, 'visits': {1: 0, 2: 0, 3: 0}}
        print("\n"+"="*60)
        print("RESET STATYSTYK")
        print("="*60+"\n")

print("\n"+"="*60)
print("PODSUMOWANIE SESJI")
print("="*60)
print(f"Laczne wejscia: {stats['entries']}")
print(f"Prawidlowe sekwencje: {stats['sequences']}")
print(f"Bledy: {stats['errors']}")
print(f"Strefa 1: {stats['visits'][1]} razy")
print(f"Strefa 2: {stats['visits'][2]} razy")
print(f"Strefa 3: {stats['visits'][3]} razy")
print("="*60)

cap.release()
cv.destroyAllWindows()
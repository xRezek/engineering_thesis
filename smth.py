import cv2 as cv
import mediapipe as mp
import numpy as np
from datetime import datetime
from collections import deque

class HandZoneDetector:
    def __init__(self):
        # Inicjalizacja MediaPipe dla obu rąk
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            min_detection_confidence=0.7,
            min_tracking_confidence=0.7,
            max_num_hands=2  # Wykrywanie obu rąk
        )
        self.mp_draw = mp.solutions.drawing_utils
        
        # Definicja stref (x1, y1, x2, y2) - wyżej i z większymi odstępami
        self.zones = {
            1: {'coords': (100, 150, 300, 350), 'color': (0, 255, 0), 'name': 'STREFA 1'},
            2: {'coords': (400, 150, 600, 350), 'color': (255, 255, 0), 'name': 'STREFA 2'},
            3: {'coords': (700, 150, 900, 350), 'color': (0, 0, 255), 'name': 'STREFA 3'}
        }
        
        # Historia wejść dla każdej ręki osobno
        self.left_hand_history = deque(maxlen=10)
        self.right_hand_history = deque(maxlen=10)
        
        self.left_current_zone = None
        self.right_current_zone = None
        
        self.left_last_zone = None
        self.right_last_zone = None
        
        self.left_zone_entry_time = None
        self.right_zone_entry_time = None
        
        self.left_last_log_time = None
        self.right_last_log_time = None
        
        self.min_time_in_zone = 0.3
        self.log_cooldown = 1.0
        
        # Statystyki dla każdej ręki
        self.stats = {
            'left': {
                'total_entries': 0,
                'errors': [],
                'correct_sequence': 0,
                'zone_visits': {1: 0, 2: 0, 3: 0}
            },
            'right': {
                'total_entries': 0,
                'errors': [],
                'correct_sequence': 0,
                'zone_visits': {1: 0, 2: 0, 3: 0}
            }
        }
        
    def is_hand_in_zone(self, hand_x, hand_y, zone_coords):
        """Sprawdza czy punkt jest w strefie"""
        x1, y1, x2, y2 = zone_coords
        return x1 <= hand_x <= x2 and y1 <= hand_y <= y2
    
    def log_event(self, message, event_type="INFO", hand_type=""):
        """Logowanie zdarzeń"""
        timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]
        hand_label = f"[{hand_type.upper()}] " if hand_type else ""
        log_msg = f"[{timestamp}] [{event_type}] {hand_label}{message}"
        print(log_msg)
        
        if event_type == "ERROR":
            if hand_type == "left":
                self.stats['left']['errors'].append(log_msg)
            elif hand_type == "right":
                self.stats['right']['errors'].append(log_msg)
    
    def validate_sequence(self, new_zone, last_zone, history, hand_type):
        """Walidacja sekwencji przejść między strefami"""
        if last_zone is None:
            return True
        
        # Sprawdź czy nie pominięto strefy
        if abs(new_zone - last_zone) > 1:
            self.log_event(
                f"BŁĄD: Pominięto strefę! Skok z STREFY {last_zone} do STREFY {new_zone}",
                "ERROR", hand_type
            )
            return False
        
        # Sprawdź czy nie wrócono do tej samej strefy zbyt szybko
        if len(history) >= 2:
            if history[-1] == new_zone and history[-2] == new_zone:
                self.log_event(
                    f"BŁĄD: Podwójne wejście do STREFY {new_zone}",
                    "ERROR", hand_type
                )
                return False
        
        return True
    
    def process_zone_entry(self, zone_id, hand_type):
        """Przetwarzanie wejścia do strefy"""
        current_time = datetime.now()
        
        # Wybierz odpowiednie dane dla ręki
        if hand_type == "left":
            last_log_time = self.left_last_log_time
            zone_entry_time = self.left_zone_entry_time
            last_zone = self.left_last_zone
            history = self.left_hand_history
            stats = self.stats['left']
        else:
            last_log_time = self.right_last_log_time
            zone_entry_time = self.right_zone_entry_time
            last_zone = self.right_last_zone
            history = self.right_hand_history
            stats = self.stats['right']
        
        # Sprawdź cooldown dla logowania
        if last_log_time is not None:
            time_since_last_log = (current_time - last_log_time).total_seconds()
            if time_since_last_log < self.log_cooldown:
                return False
        
        # Sprawdź czy wystarczająco długo w poprzedniej strefie
        if zone_entry_time is not None:
            time_diff = (current_time - zone_entry_time).total_seconds()
            if time_diff < self.min_time_in_zone and last_zone is not None:
                self.log_event(
                    f"UWAGA: Zbyt krótki pobyt w STREFIE {last_zone} ({time_diff:.2f}s)",
                    "WARNING", hand_type
                )
        
        # Walidacja sekwencji
        if not self.validate_sequence(zone_id, last_zone, history, hand_type):
            if hand_type == "left":
                self.left_last_log_time = current_time
            else:
                self.right_last_log_time = current_time
            return False
        
        # Zapisz wejście
        history.append(zone_id)
        stats['total_entries'] += 1
        stats['zone_visits'][zone_id] += 1
        
        if hand_type == "left":
            self.left_last_zone = zone_id
            self.left_zone_entry_time = current_time
            self.left_last_log_time = current_time
        else:
            self.right_last_zone = zone_id
            self.right_zone_entry_time = current_time
            self.right_last_log_time = current_time
        
        self.log_event(f"✓ Wejście do STREFY {zone_id}", "SUCCESS", hand_type)
        
        # Sprawdź czy wykonano poprawną sekwencję 1->2->3
        if len(history) >= 3:
            last_three = list(history)[-3:]
            if last_three == [1, 2, 3]:
                stats['correct_sequence'] += 1
                self.log_event("★ PRAWIDŁOWA SEKWENCJA 1→2→3 ★", "SUCCESS", hand_type)
        
        return True
    
    def draw_zones(self, frame):
        """Rysowanie stref na obrazie"""
        for zone_id, zone_data in self.zones.items():
            x1, y1, x2, y2 = zone_data['coords']
            color = zone_data['color']
            
            # Pogrubienie dla aktywnej strefy
            thickness = 3 if (zone_id == self.left_current_zone or zone_id == self.right_current_zone) else 2
            
            # Rysuj prostokąt strefy
            cv.rectangle(frame, (x1, y1), (x2, y2), color, thickness)
            
            # Etykieta strefy z oddzielnymi licznikami
            left_count = self.stats['left']['zone_visits'][zone_id]
            right_count = self.stats['right']['zone_visits'][zone_id]
            label = f"{zone_data['name']} (L:{left_count} R:{right_count})"
            cv.putText(frame, label, (x1, y1-10), 
                      cv.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)
    
    def draw_stats(self, frame):
        """Wyświetlanie statystyk"""
        y_offset = 420
        
        # Statystyki lewej ręki
        left_stats = [
            "=== LEWA REKA ===",
            f"Wejscia: {self.stats['left']['total_entries']}",
            f"Sekwencje: {self.stats['left']['correct_sequence']}",
            f"Bledy: {len(self.stats['left']['errors'])}",
            f"Historia: {' -> '.join(map(str, list(self.left_hand_history)[-5:]))}"
        ]
        
        for i, text in enumerate(left_stats):
            cv.putText(frame, text, (10, y_offset + i*25),
                      cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 2)
        
        # Statystyki prawej ręki
        right_stats = [
            "=== PRAWA REKA ===",
            f"Wejscia: {self.stats['right']['total_entries']}",
            f"Sekwencje: {self.stats['right']['correct_sequence']}",
            f"Bledy: {len(self.stats['right']['errors'])}",
            f"Historia: {' -> '.join(map(str, list(self.right_hand_history)[-5:]))}"
        ]
        
        x_offset = 500
        for i, text in enumerate(right_stats):
            cv.putText(frame, text, (x_offset, y_offset + i*25),
                      cv.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 255), 2)
    
    def run(self):
        """Główna pętla programu"""
        cap = cv.VideoCapture(0)
        
        # Ustaw rozdzielczość
        cap.set(cv.CAP_PROP_FRAME_WIDTH, 1280)
        cap.set(cv.CAP_PROP_FRAME_HEIGHT, 720)
        
        print("=" * 60)
        print("SYSTEM DETEKCJI OBU RĄK Z STREFAMI")
        print("=" * 60)
        print("Instrukcja:")
        print("- Każda ręka jest śledzona niezależnie")
        print("- Przesuwaj ręce przez strefy w kolejności 1 -> 2 -> 3")
        print("- System wykryje błędy dla każdej ręki osobno")
        print("- Naciśnij 'q' aby zakończyć")
        print("- Naciśnij 'r' aby zresetować statystyki")
        print("=" * 60)
        
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            # Obróć obraz o 180 stopni
            frame = cv.rotate(frame, cv.ROTATE_180)
            
            frame_rgb = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
            
            # Resetuj obecne strefy
            self.left_current_zone = None
            self.right_current_zone = None
            
            # Detekcja rąk
            results = self.hands.process(frame_rgb)
            
            height, width = frame.shape[:2]
            
            if results.multi_hand_landmarks and results.multi_handedness:
                for hand_landmarks, handedness in zip(results.multi_hand_landmarks, results.multi_handedness):
                    # Określ czy to lewa czy prawa ręka
                    hand_label = handedness.classification[0].label  # "Left" lub "Right"
                    hand_type = "left" if hand_label == "Left" else "right"
                    
                    # Kolor dla ręki
                    hand_color = (0, 255, 255) if hand_type == "left" else (255, 0, 255)
                    
                    # Rysuj szkielet dłoni
                    for connection in self.mp_hands.HAND_CONNECTIONS:
                        start_idx = connection[0]
                        end_idx = connection[1]
                        
                        start_point = hand_landmarks.landmark[start_idx]
                        end_point = hand_landmarks.landmark[end_idx]
                        
                        start_x = int(start_point.x * width)
                        start_y = int(start_point.y * height)
                        end_x = int(end_point.x * width)
                        end_y = int(end_point.y * height)
                        
                        cv.line(frame, (start_x, start_y), (end_x, end_y), hand_color, 2)
                    
                    # Rysuj punkty landmarków
                    for landmark in hand_landmarks.landmark:
                        x = int(landmark.x * width)
                        y = int(landmark.y * height)
                        cv.circle(frame, (x, y), 3, hand_color, -1)
                    
                    # Pobierz pozycję wskazującego palca (landmark 8)
                    index_finger = hand_landmarks.landmark[8]
                    finger_x = int(index_finger.x * width)
                    finger_y = int(index_finger.y * height)
                    
                    # Rysuj punkt wskazującego palca
                    cv.circle(frame, (finger_x, finger_y), 10, hand_color, -1)
                    
                    # Dodaj etykietę ręki
                    label_text = "LEWA" if hand_type == "left" else "PRAWA"
                    cv.putText(frame, label_text, (finger_x + 15, finger_y - 15),
                              cv.FONT_HERSHEY_SIMPLEX, 0.6, hand_color, 2)
                    
                    # Sprawdź w której strefie jest palec
                    for zone_id, zone_data in self.zones.items():
                        if self.is_hand_in_zone(finger_x, finger_y, zone_data['coords']):
                            # Jeśli to nowa strefa, zapisz wejście
                            if hand_type == "left" and self.left_current_zone != zone_id:
                                self.left_current_zone = zone_id
                                self.process_zone_entry(zone_id, "left")
                            elif hand_type == "right" and self.right_current_zone != zone_id:
                                self.right_current_zone = zone_id
                                self.process_zone_entry(zone_id, "right")
                            break
            
            # Rysuj strefy i statystyki
            self.draw_zones(frame)
            self.draw_stats(frame)
            
            # Wyświetl obraz
            cv.imshow('Hand Zone Detection - Both Hands', frame)
            
            # Obsługa klawiszy
            key = cv.waitKey(1) & 0xFF
            if key == ord('q'):
                break
            elif key == ord('r'):
                self.__init__()
                print("\n" + "=" * 60)
                print("STATYSTYKI ZRESETOWANE")
                print("=" * 60 + "\n")
        
        # Podsumowanie
        print("\n" + "=" * 60)
        print("PODSUMOWANIE SESJI")
        print("=" * 60)
        print("\n--- LEWA RĘKA ---")
        print(f"Łączne wejścia: {self.stats['left']['total_entries']}")
        print(f"Prawidłowe sekwencje (1→2→3): {self.stats['left']['correct_sequence']}")
        print(f"Liczba błędów: {len(self.stats['left']['errors'])}")
        
        print("\n--- PRAWA RĘKA ---")
        print(f"Łączne wejścia: {self.stats['right']['total_entries']}")
        print(f"Prawidłowe sekwencje (1→2→3): {self.stats['right']['correct_sequence']}")
        print(f"Liczba błędów: {len(self.stats['right']['errors'])}")
        print("=" * 60)
        
        cap.release()
        cv.destroyAllWindows()

if __name__ == "__main__":
    detector = HandZoneDetector()
    detector.run()
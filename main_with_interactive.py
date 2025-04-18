import cv2
import numpy as np
import tkinter as tk
import pickle
import subprocess
from PIL import Image, ImageTk
from interactive_map import InteractiveMapInterface

WIDTH, HEIGHT = 107, 48
POS_FILES = {
    1: 'CarParkPos',
    2: 'CarParkPos1',
    3: 'CarParkPos2',
}
VIDEO_FILES = {
    1: 'carPark.mp4',
    2: 'carPark2.mp4',
    3: 'carPark3.mp4',
}
IMG_WIDTH, IMG_HEIGHT = 864, 513

AREA_PARAMS = {
    1: {'thresh': 1200, 'w': WIDTH, 'h': HEIGHT},
    2: {'thresh': 900, 'w_land': 105, 'h_land': 45, 'w_port': 45, 'h_port': 95},
    3: {'thresh': 100, 'w_land': 27, 'h_land': 13, 'w_port': 13, 'h_port': 27},
}

class ParkingDetectionSystem:
    def __init__(self):
        self.map_interface = InteractiveMapInterface()

        self.root = tk.Tk()
        self.root.title('Parking Space Detection')
        self.setup_gui()

        self.root.bind('q', lambda e: self.quit_app())

    def setup_gui(self):
        tk.Label(self.root, text='Your Latitude:').pack()
        self.lat_entry = tk.Entry(self.root)
        self.lat_entry.insert(0, '12.9716')
        self.lat_entry.pack()

        tk.Label(self.root, text='Your Longitude:').pack()
        self.lon_entry = tk.Entry(self.root)
        self.lon_entry.insert(0, '77.5946')
        self.lon_entry.pack()

        tk.Button(self.root, text='Update Map', command=self.update_map).pack(pady=10)

        for area_id, area in self.map_interface.parking_areas.items():
            btn = tk.Button(
                self.root,
                text=f'View Video: {area.name}',
                command=lambda aid=area_id: self.view_video(aid)
            )
            btn.pack(fill='x', padx=20, pady=2)

    def load_positions(self, area_id):
        fname = POS_FILES.get(area_id)
        with open(fname, 'rb') as f:
            return pickle.load(f)

    def view_video(self, area_id):
        if area_id in (2, 3):
            script = f'main{area_id}.py'
            subprocess.Popen(['python', script])
            return

        cap = cv2.VideoCapture(VIDEO_FILES[1])
        posList = self.load_positions(1)

        window = tk.Toplevel(self.root)
        window.title("Live Feed – Area 1")
        label = tk.Label(window)
        label.pack()
        window.bind('q', lambda e: on_close())

        def update_frame():
            ret, frame = cap.read()
            if not ret:
                cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
                ret, frame = cap.read()

            free = self._process_frame(frame, posList, label)
            window.after(30, update_frame)

        def on_close():
            cap.release()
            window.destroy()
            self.update_map()

        window.protocol('WM_DELETE_WINDOW', on_close)
        update_frame()

    def _process_frame(self, frame, posList, label):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (3, 3), 1)
        thresh = cv2.adaptiveThreshold(blur, 255, cv2.ADAPTIVE_THRESH_MEAN_C,
                                       cv2.THRESH_BINARY_INV, 25, 16)
        med = cv2.medianBlur(thresh, 5)
        dilate = cv2.dilate(med, np.ones((3, 3), np.uint8), iterations=1)

        free = 0
        for x, y, *rest in posList:
            cnt = cv2.countNonZero(dilate[y:y + HEIGHT, x:x + WIDTH])
            color = (0, 255, 0) if cnt < AREA_PARAMS[1]['thresh'] else (0, 0, 255)
            thickness = 5 if cnt < AREA_PARAMS[1]['thresh'] else 2
            if cnt < AREA_PARAMS[1]['thresh']:
                free += 1
            cv2.rectangle(frame, (x, y), (x + WIDTH, y + HEIGHT), color, thickness)
            cv2.putText(frame, str(cnt), (x, y + HEIGHT - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1)

        cv2.putText(frame, f'Free: {free}/{len(posList)}', (10, 30),
                    cv2.FONT_HERSHEY_DUPLEX, 1, (0, 200, 0), 2)

        img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        pil = Image.fromarray(img_rgb)
        imgtk = ImageTk.PhotoImage(pil)
        label.imgtk = imgtk
        label.config(image=imgtk)
        return free

    def update_map(self):
        try:
            user_lat = float(self.lat_entry.get())
            user_lon = float(self.lon_entry.get())
        except ValueError:
            print('Invalid coordinates')
            return

        for area_id, vid in VIDEO_FILES.items():
            cap = cv2.VideoCapture(vid)
            success, frame = cap.read()
            cap.release()
            if not success:
                continue

            if area_id in (2, 3):
                frame = cv2.resize(frame, (IMG_WIDTH, IMG_HEIGHT))

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            blur = cv2.GaussianBlur(gray, (3, 3), 1)
            thresh = cv2.adaptiveThreshold(blur, 255, cv2.ADAPTIVE_THRESH_MEAN_C,
                                           cv2.THRESH_BINARY_INV, 25, 16)
            med = cv2.medianBlur(thresh, 5)
            dilate = cv2.dilate(med, np.ones((3, 3), np.uint8), iterations=1)

            posList = self.load_positions(area_id)
            free = 0
            params = AREA_PARAMS[area_id]

            for pos in posList:
                if area_id == 1:
                    x, y, *_ = pos
                    w, h = params['w'], params['h']
                    thresh_val = params['thresh']
                else:
                    if len(pos) == 2:
                        x, y = pos
                        ptype = 'landscape'
                    else:
                        x, y, ptype = pos
                    w = params['w_land'] if ptype == 'landscape' else params['w_port']
                    h = params['h_land'] if ptype == 'landscape' else params['h_port']
                    thresh_val = params['thresh']

                cnt = cv2.countNonZero(dilate[y:y + h, x:x + w])
                if cnt < thresh_val:
                    free += 1

            self.map_interface.update_area_availability(area_id, free, len(posList))

        self.map_interface.show_map(user_lat, user_lon)

    def quit_app(self):
        self.root.destroy()

    def run(self):
        self.root.mainloop()

if __name__ == '__main__':
    ParkingDetectionSystem().run()
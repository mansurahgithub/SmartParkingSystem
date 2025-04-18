import cv2
import pickle

# Load the image
image_path = 'carImg3.jpg'
img = cv2.imread(image_path)
img = cv2.resize(img, (864, 513))  # Resize as needed

# Default rectangle sizes
width_landscape, height_landscape = 27, 13
width_portrait, height_portrait = 13, 27

# Start in landscape mode
current_mode = 'landscape'

# Load saved positions or initialize an empty list
try:
    with open('CarParkPos2', 'rb') as f:
        posList = pickle.load(f)
        for i in range(len(posList)):
            if len(posList[i]) == 2:
                posList[i] = (posList[i][0], posList[i][1], 'landscape')
except:
    posList = []

# Mouse click event handler
def mouseClick(events, x, y, flags, params):
    global posList
    if events == cv2.EVENT_LBUTTONDOWN:
        posList.append((x, y, current_mode))
    elif events == cv2.EVENT_RBUTTONDOWN:
        for i, pos in enumerate(posList):
            px, py, ptype = pos
            w = width_landscape if ptype == 'landscape' else width_portrait
            h = height_landscape if ptype == 'landscape' else height_portrait
            if px < x < px + w and py < y < py + h:
                posList.pop(i)
                break

# Set mouse callback
cv2.namedWindow("Image")
cv2.setMouseCallback("Image", mouseClick)

# Main loop
while True:
    img_copy = img.copy()

    # Show current mode
    cv2.putText(img_copy, f'Mode: {current_mode}', (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 200, 0), 2)

    # Draw rectangles only (no numbering)
    for pos in posList:
        x, y, ptype = pos
        w = width_landscape if ptype == 'landscape' else width_portrait
        h = height_landscape if ptype == 'landscape' else height_portrait
        cv2.rectangle(img_copy, (x, y), (x + w, y + h), (255, 0, 255), 2)

    # Show image
    cv2.imshow("Image", img_copy)
    key = cv2.waitKey(1)

    if key == ord('r'):
        current_mode = 'portrait' if current_mode == 'landscape' else 'landscape'
    elif key == ord('s'):
        with open('CarParkPos2', 'wb') as f:
            pickle.dump(posList, f)
    elif key == ord('q'):
        break

cv2.destroyAllWindows()
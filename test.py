import cv2
import numpy as np

# Загрузка изображения
image = cv2.imread('res.jpg')

# Преобразование изображения в оттенки серого
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Обнаружение границ с помощью оператора Кэнни
edges = cv2.Canny(gray, 50, 150)

# Применение Хафовского преобразования для обнаружения прямых линий
lines = cv2.HoughLines(edges, 1, np.pi/180, threshold=100)

# Фильтрация и выбор горизонтальных линий
horizontal_lines = []
for line in lines:
    rho, theta = line[0]
    angle = theta * 180 / np.pi
    if angle > 85 and angle < 95:  # Фильтрация по углу (горизонтальные линии примерно 90 градусов)
        horizontal_lines.append((rho, theta))

# Определение угла каждой горизонтальной линии
for line in horizontal_lines:
    rho, theta = line
    angle = theta * 180 / np.pi
    print("Угол горизонтальной линии: ", angle)

# Визуализация горизонтальных линий на изображении
for line in horizontal_lines:
    rho, theta = line
    a = np.cos(theta)
    b = np.sin(theta)
    x0 = a * rho
    y0 = b * rho
    x1 = int(x0 + 1000 * (-b))
    y1 = int(y0 + 1000 * (a))
    x2 = int(x0 - 1000 * (-b))
    y2 = int(y0 - 1000 * (a))
    cv2.line(image, (x1, y1), (x2, y2), (0, 0, 255), 2)

# Вывод изображения с обнаруженными горизонтальными линиями
cv2.imshow("Detected Lines", image)
cv2.waitKey(0)
cv2.destroyAllWindows()
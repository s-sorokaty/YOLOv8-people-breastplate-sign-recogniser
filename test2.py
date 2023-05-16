import cv2
import numpy as np

# Загрузка изображения
image = cv2.imread('res.jpg')

# Преобразование изображения в оттенки серого
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
# Обнаружение границ с помощью оператора Кэнни
edges = cv2.Canny(gray, 50, 150)
cv2.imwrite('edges.jpg', edges)

# Применение Хафовского преобразования для обнаружения прямых линий
lines = cv2.HoughLines(edges, 3, np.pi/180, threshold=100)

# Фильтрация и выбор параллельных линий
parallel_lines = []
average_angle = 0
count = 0
for line1 in lines:
    rho1, theta1 = line1[0]
    angle1 = theta1 * 180 / np.pi
    for line2 in lines:
        rho2, theta2 = line2[0]
        angle2 = theta2 * 180 / np.pi
        if abs(angle1 - angle2) < 5:  # Фильтрация по углу (параллельные линии с малым отклонением)
            parallel_lines.append((rho1, theta1))
            parallel_lines.append((rho2, theta2))
            average_angle += angle1
            count += 1

# Нахождение усредненного угла параллельных линий
if count > 0:
    average_angle /= count 
    average_angle = -( 90 - average_angle)
    print("Усредненный угол параллельных линий: ", average_angle)

    # Визуализация параллельных линий на изображении
    #for line in parallel_lines:
    #    rho, theta = line
    #    angle = theta * 180 / np.pi
    #    a = np.cos(theta)
    #    b = np.sin(theta)
    #    x0 = a * rho
    #    y0 = b * rho
    #    x1 = int(x0 + 1000 * (-b))
    #    y1 = int(y0 + 1000 * (a))
    #    x2 = int(x0 - 1000 * (-b))
    #    y2 = int(y0 - 1000 * (a))
    #    cv2.line(image, (x1, y1), (x2, y2), (0, 0, 255), 2)

    # Поворот изображения на усредненный угол
    center = (image.shape[1] // 2, image.shape[0] // 2)
    rotation_matrix = cv2.getRotationMatrix2D(center, average_angle, 1.0)
    rotated_image = cv2.warpAffine(image, rotation_matrix, (image.shape[1], image.shape[0]))

    # Вывод изображения с обнаруженными параллельными линиями и поворотом
    cv2.imwrite('result_haaf.jpg', rotated_image)
    cv2.imshow("Detected Lines", rotated_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
else:
    print("Не найдено параллельных линий.")

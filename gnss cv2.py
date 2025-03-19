import cv2
import numpy as np

# 讀取影像
image = cv2.imread('wtf1.jpg', cv2.IMREAD_GRAYSCALE)

# 使用 Otsu's Thresholding 進行二值化
_, binary_image = cv2.threshold(image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

# 顯示結果
cv2.imshow('Binary Image', binary_image)
cv2.waitKey(0)
cv2.destroyAllWindows()

# # 設定極座標變換尺寸 //魚眼?
# height, width = binary_image.shape
# polar_image = cv2.linearPolar(binary_image, (width//2, height//2), width//2, cv2.WARP_FILL_OUTLIERS)

# # 顯示結果
# cv2.imshow("Polar Image", polar_image)
# cv2.waitKey(0)
# cv2.destroyAllWindows()

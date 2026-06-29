import cv2
import numpy as np

def distance(p1, p2):
	x1, y1 = p1
	x2, y2 = p2
	return np.sqrt((y2-y1)**2+(x2-x1)**2)

def cart2pol(x, y):
    theta = np.arctan2(y, x)
    rho = np.hypot(x, y)
    return theta, rho

def pol2cart(theta, rho):
    x = rho * np.cos(theta)
    y = rho * np.sin(theta)
    return x, y

def rotate_contour(cnt, angle):
    M = cv2.moments(cnt)
    cx = int(M['m10']/M['m00'])
    cy = int(M['m01']/M['m00'])

    cnt_norm = cnt - [cx, cy]
    
    coordinates = cnt_norm[:, 0, :]
    xs, ys = coordinates[:, 0], coordinates[:, 1]
    thetas, rhos = cart2pol(xs, ys)
    
    thetas = np.rad2deg(thetas)
    thetas = (thetas + angle) % 360
    thetas = np.deg2rad(thetas)
    
    xs, ys = pol2cart(thetas, rhos)
    
    cnt_norm[:, 0, 0] = xs
    cnt_norm[:, 0, 1] = ys

    cnt_rotated = cnt_norm + [cx, cy]
    cnt_rotated = cnt_rotated.astype(np.int32)

    return cnt_rotated

def centroid(contour):
	M = cv2.moments(contour)
	cx = int(M['m10']/M['m00'])
	cy = int(M['m01']/M['m00'])

	return cx, cy

def compactness(contour, area):
	center, radius = cv2.minEnclosingCircle(contour)
	compactness = area / (np.pi * radius * radius)
	return compactness

def axis(contour):
	rect = cv2.minAreaRect(contour)
	boxes = cv2.boxPoints(rect)
	boxes = np.int0(boxes)
	lengths = []
	for b in boxes[1:]:
		lengths.append(distance(boxes[0], b))
	minAxis, maxAxis, diagonal = sorted(lengths)
	return minAxis, maxAxis

def diameter(area):
	diameter = np.sqrt(4*area/np.pi)
	return diameter

def perimeter(contour):
	perimeter = cv2.arcLength(contour,True)
	return perimeter

def feret(contour, area):
	minFeret = area
	maxFeret = 0
	for angle in range(90):
		rcnt = rotate_contour(contour, angle)
		_, _, w, h = cv2.boundingRect(rcnt)
		if w > maxFeret:
			maxFeret = w
		if h > maxFeret:
			maxFeret = h
		if w < minFeret:
			minFeret = w
		if h < minFeret:
			minFeret = h
	return minFeret, maxFeret

def eccenticity(contour):
	ellipse = cv2.fitEllipse(contour)
	boxes = cv2.boxPoints(ellipse)
	boxes = np.int0(boxes)
	lengths = []
	for b in boxes[1:]:
		lengths.append(distance(boxes[0], b))
	b, a, d = sorted(lengths)
	eccenticity = np.sqrt(1-b**2/a**2)
	return eccenticity

def extent(contour, area):
	_, _, w, h = cv2.boundingRect(contour)
	extent = area/(w*h)
	return extent

def extent2(area, minAxis, maxAxis):
	extent = area/(minAxis*maxAxis)
	return extent

def solidity(contour, area):
	hull = cv2.convexHull(contour)
	hull_area = cv2.contourArea(hull)
	solidity = float(area)/hull_area
	return solidity

def intensity(image, mask):
	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	intensity = np.sum(gray[mask==255])
	return intensity

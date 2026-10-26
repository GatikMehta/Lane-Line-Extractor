# Lane-Line-Extractor

Week 2 of CEAM Task Phase. This is a Python script that uses OpenCV to find the lane lines in a photo of a road.

Where can we use lane line extractor?

In a self-driving car: before it can steer, it has to know where the lane is.

How it works

The script goes through 5 steps, one after the other.

Original Image I took from Google (random).

<img width="618" height="349" alt="image" src="https://github.com/user-attachments/assets/9d88ded5-881e-454d-857e-1024163ff534" />

1. Load the image

I used cv2.imread() to load the picture. I learned that an image is really just a big grid of numbers (one number per pixel), and that OpenCV stores colours as BGR instead of the usual RGB.

2. HSV colour filtering

Lane lines are usually white or yellow, so I convert the image from BGR to HSV and keep only those colours using cv2.inRange().

Why HSV and not BGR? In HSV, the colour (Hue) is separate from the brightness (Value), so "yellow" is easier to pick out even if it's a bit shadowy.

HSV mask

The white parts are the pixels that matched white or yellow.

<img width="618" height="349" alt="road1_1_hsv_mask" src="https://github.com/user-attachments/assets/bf8798ec-4222-4975-9e6f-dbd66f852cba" />


3. Gaussian blur

cv2.GaussianBlur() smooths the image a little by averaging each pixel with its neighbours. This gets rid of tiny noise so that it doesn't get mistaken for edges in the next step.

<img width="618" height="349" alt="road1_2_blurred" src="https://github.com/user-attachments/assets/11a6bf1c-6c6c-4afd-bac3-6f3a54046b11" />


4. Canny edge detection

cv2.Canny() finds the places where brightness changes a lot, which are the edges of objects. It uses two thresholds (I used 50 and 150): anything above the high one is definitely an edge, and anything below the low one is thrown away.

<img width="618" height="349" alt="road1_3_canny" src="https://github.com/user-attachments/assets/2db5e437-f87e-484d-8068-dc02a2854ac2" />


5. Region of Interest (ROI) mask

Lane lines are only on the road, so I draw a trapezoid shape over the road area and delete everything outside of it. I did this by making a black image, filling the trapezoid with white (cv2.fillPoly()), and combining it with the edges using cv2.bitwise_and().

<img width="618" height="349" alt="road1_4_roi_edges" src="https://github.com/user-attachments/assets/2726e886-0e78-4854-9243-b29b05e06c0b" />

Final Result

<img width="618" height="349" alt="road1_5_result" src="https://github.com/user-attachments/assets/07b9a790-95ec-482c-b347-3c6750cca8bd" />


How to run it

Install Python and then the libraries:

1) pip install -r requirements.txt
   
2) Put your road images in the images folder.

3) Run the script with the image path:

4) python lane_extractor.py images/sample_road.jpg
   
5) Check the output folder. It saves one image for each step, and _5_result.jpg is the final one.

Limitations

1) This is "classical" computer vision, which means it uses fixed rules that I set by hand, so it isn't perfect:

2) The HSV ranges and the ROI trapezoid are tuned by hand, so different lighting or camera angles need different numbers.

3) Shadows, worn paint, rain or night driving would probably break it.

4) It only finds lane edge pixels. It doesn't draw clean lines or work out where the lane is.

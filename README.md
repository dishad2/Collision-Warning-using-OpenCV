# Simple ADAS Car Safety Dashboard & Data Logger

This project is a car safety simulation that helps drivers maintain a safe distance from the vehicle ahead. It generates a virtual driving scene from scratch and uses smart rules to display warnings if you get too close to the car in front.

---

## Working

1. **Creates a Road Screen**: The program draws a moving highway with lane lines and a vehicle in front using computer code.
2. **Tracks the Car**: It watches the car ahead and calculates exactly how many meters away it is.
3. **Shows Live Alerts**: It changes the dashboard color and messages based on distance:
   * **Far Away**: Shows a **Green** box and says `"SYSTEM OK: KEEP DISTANCE"`.
   * **Getting Closer**: Turns **Amber** and says `"WARNING: CLOSING DISTANCE"`.
   * **Too Close**: Flashes **Red** and warns `"FCW CRITICAL: BRAKE NOW!"`.
4. **Saves a Table (Data Log)**: It automatically writes down the distance, speed, and safety message for every single moment into a spreadsheet file (`adas_telemetry_log.csv`).

---

## Topics Covered

This project uses standard Python libraries (**OpenCV**, **NumPy**, and **Pandas**) to practice these exact skills from the course:

*   **NumPy & OpenCV Basics**: Creating a clean background image canvas from scratch using number arrays and saving the finished video file smoothly.
*   **Drawing & Effects**: Using code to draw geometric shapes (rectangles, lines, and circles) to build the road, lanes, and cars. It also uses color mapping to switch the UI colors from green to red based on smart threshold rules.
*   **Object Detection & Tracking**: Simulating how a forward camera follows a target vehicle frame by frame as it moves closer and further away.
*   **Data Logging Integration**: Exporting live structural tracking data directly into a spreadsheet table so engineers can look back at the safety logs.

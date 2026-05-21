import cv2
import numpy as np
import pandas as pd

def generate_adas_with_logs(output_filename="adas_slow_simulation.webm", num_frames=150):
    print("Generating simulation and logging data with Pandas... Please wait.")
    
    width, height = 800, 600
    
    # 1. SLOW DOWN SPEED: We change the FPS from 30 to 10. 
    # This makes the video play 3 times slower so you can read the text!
    fps = 10 
    
    fourcc = cv2.VideoWriter_fourcc(*'VP80')  
    out = cv2.VideoWriter(output_filename, fourcc, fps, (width, height))
    
    car_w, car_h = 100, 80
    
    # Create an empty list to hold our data rows for Pandas
    telemetry_data = []
    
    for i in range(num_frames):
        # --- GENERATE ENVIRONMENT ---
        frame = np.zeros((height, width, 3), dtype="uint8") + 35
        cv2.rectangle(frame, (0, 0), (width, 250), (100, 60, 40), -1) 
        
        offset = (i * 15) % 100
        for y_pos in range(250, height, 80):
            current_y = y_pos + offset
            if current_y < height:
                cv2.line(frame, (int(current_y * 0.4), current_y), (int(current_y * 0.4) + 20, current_y), (255, 255, 255), 4)
                cv2.line(frame, (width - int(current_y * 0.4), current_y), (width - int(current_y * 0.4) - 20, current_y), (255, 255, 255), 4)

        # Simulate vehicle ahead distance
        distance_factor = 1.0 + 0.5 * np.sin(i * 0.08) 
        current_w = int(car_w * distance_factor)
        current_h = int(car_h * distance_factor)
        
        cx, cy = 400, 250 + int(70 / distance_factor)
        x1, y1 = cx - (current_w // 2), cy - (current_h // 2)
        x2, y2 = cx + (current_w // 2), cy + (current_h // 2)
        
        cv2.rectangle(frame, (x1, y1), (x2, y2), (70, 70, 70), -1)      
        cv2.rectangle(frame, (x1 + 10, y1 + 10), (x2 - 10, y1 + 35), (20, 20, 20), -1) 
        cv2.circle(frame, (x1 + 15, y2 - 15), 12, (0, 0, 255), -1)     
        cv2.circle(frame, (x2 - 15, y2 - 15), 12, (0, 0, 255), -1)     

        # --- CALCULATE METRICS AND SAFETY MESSAGES ---
        simulated_distance = round(45.0 / distance_factor, 1)
        simulated_speed = int(80 + (distance_factor * 12))
        
        # Threshold Logic
        if simulated_distance < 35.0:
            status_text = "FCW CRITICAL: BRAKE NOW!"
            ui_color = (0, 0, 255)       # Red
            line_thickness = 3
        elif simulated_distance < 42.0:
            status_text = "WARNING: CLOSING DISTANCE"
            ui_color = (0, 255, 255)     # Amber
            line_thickness = 2
        else:
            status_text = "SYSTEM OK: KEEP DISTANCE"
            ui_color = (0, 255, 0)       # Green
            line_thickness = 1

        # --- COLLECT DATA FOR PANDAS ---
        # We append a dictionary for every single frame
        telemetry_data.append({
            "Frame_ID": i + 1,
            "Distance_Meters": simulated_distance,
            "Host_Speed_KMH": simulated_speed,
            "System_Message": status_text
        })

        # --- DRAW UI OVERLAYS ---
        cv2.rectangle(frame, (x1 - 5, y1 - 5), (x2 + 5, y2 + 5), ui_color, line_thickness)
        cv2.rectangle(frame, (0, 0), (width, 65), (20, 20, 20), -1)
        cv2.line(frame, (0, 65), (width, 65), (150, 150, 150), 2)
        
        cv2.putText(frame, f"TARGET DISTANCE: {simulated_distance} m", (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        cv2.putText(frame, status_text, (420, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.6, ui_color, 2)
        cv2.putText(frame, f"HOST SPEED: {simulated_speed} KM/H", (20, 560), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

        out.write(frame)
        
    out.release()
    print("Video output saved.")
    
    # --- PHASE 4: PANDAS DATA EXTRACTION ---
    # Convert our list of data into a structured Pandas DataFrame table
    df = pd.DataFrame(telemetry_data)
    
    # Save the table to a CSV spreadsheet file
    df.to_csv("adas_telemetry_log.csv", index=False)
    print("Pandas table saved to disk as 'adas_telemetry_log.csv'!")
    
    # Print the first few rows of the table in the terminal to see it immediately
    print("\n--- SAMPLE LOG TABLE (First 15 Frames) ---")
    print(df.head(15).to_string())

if __name__ == "__main__":
    generate_adas_with_logs()

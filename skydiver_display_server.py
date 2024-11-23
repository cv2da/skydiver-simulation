#!/usr/bin/python3
import sys 
import socket
import math
from tkinter import *


# ----------------------------------------------------------------------
# 1.0 Process the command line arguments, to get the port number.
if ( len(sys.argv) == 2) :
    trick_varserver_port = int(sys.argv[1])
else :
    print( "Usage: vsclient <port_number>")
    sys.exit()
# ----------------------------------------------------------------------
# 2.0 Set client Parameters.
HEIGHT, WIDTH = 500, 500   # Square canvas, 500x500 pixels
MARGIN = 80                # Margin for axis labels
SCALE = 0.1                # Adjusted scale factor for 500px height (4000m -> 400px)
skydiverSize = 15         # Size of skydiver representation

# Add axis parameters
AXIS_TICK_LENGTH = 5       # Length of axis tick marks in pixels
HEIGHT_INTERVAL = 500      # Height interval between tick marks in meters
MAX_HEIGHT = 4000         # Maximum height to show on axis

# ----------------------------------------------------------------------
# 3.0 Create constants for clarity.
MODE_FREEZE = 1 
MODE_RUN = 5 

# ----------------------------------------------------------------------
# 4.0 Create a variable to start the jump sequence.
jumpCommand = False
def startJump():
    global jumpCommand
    jumpCommand = True

# ----------------------------------------------------------------------
# 5.0 Create the GUI

# 5.1 Create a Canvas to draw on.
tk = Tk()
canvas = Canvas(tk, width=WIDTH, height=HEIGHT)
tk.title("Skydiver Display")
canvas.pack()

# 5.2  Add a jump button, whose callback sets the jumpCommand variable.
buttonFrame = Frame()
buttonFrame.pack(side=BOTTOM)
jumpButton = Button(buttonFrame, text="Jump", command=startJump)
jumpButton.pack(side=LEFT)

# 5.3 Add an Initial height Scale.
heightScale = Scale(buttonFrame, from_=1000, to=4000, 
                   label="Initial Height (m)", 
                   orient=HORIZONTAL,
                   length=200)  # Add fixed length
heightScale.pack(side=LEFT, padx=10)  # Add padding
heightScale.set(3000)

# 5.4 Add a mass Scale.
massScale = Scale(buttonFrame, from_=50, to=100, 
                 label="Skydiver Mass (kg)", 
                 orient=HORIZONTAL,
                 length=200)  # Add fixed length
massScale.pack(side=LEFT, padx=10)  # Add padding
massScale.set(75)
# 5.5 Create coordinate axes on the canvas.
xAxis = canvas.create_line(MARGIN,HEIGHT-MARGIN,WIDTH,HEIGHT-MARGIN)
yAxis = canvas.create_line(MARGIN,HEIGHT-MARGIN,MARGIN,0)

# Add tick marks and labels for y-axis
for height in range(0, MAX_HEIGHT + HEIGHT_INTERVAL, HEIGHT_INTERVAL):
    # Calculate y position for tick mark
    y_pos = HEIGHT - MARGIN - (height * SCALE)
    
    # Draw tick mark
    canvas.create_line(MARGIN - AXIS_TICK_LENGTH, y_pos, 
                      MARGIN + AXIS_TICK_LENGTH, y_pos)
    
    # Add label
    canvas.create_text(MARGIN - 20, y_pos, 
                      text=str(height), 
                      anchor=E)

# 5.6 Create an square object to represent the skydiver.
skydiver = canvas.create_rectangle(0, 0, skydiverSize, skydiverSize, fill="red")

# 5.7 Create a text field on the canvas for the simulation mode display.
modeText = canvas.create_text(WIDTH/2, 20, text="--unknown-mode--")

# 5.8 Create text fields on the canvas for time and position of impact display.
impactTimeText = canvas.create_text(WIDTH/2, 40, text="")
impactPosText =  canvas.create_text(WIDTH/2, 60, text="")

# Add text display for drag force
dragForceText = canvas.create_text(WIDTH-100, 20, text="Drag: 0 N", anchor=E)
heightText = canvas.create_text(WIDTH-100, 40, text="Height: 0 m", anchor=E)
velocityText = canvas.create_text(WIDTH-100, 60, text="Velocity: 0 m/s", anchor=E)

# ----------------------------------------------------------------------
# 6.0 Connect to the variable server.
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect( ("localhost", trick_varserver_port) )
insock = client_socket.makefile("r")

# ----------------------------------------------------------------------
# 7.0 Request the skydiver position, velocity, drag force, and simulation mode.
client_socket.send( b"trick.var_set_client_tag(\"myvsclient\") \n")
client_socket.send( b"trick.var_debug(0)\n" ) #Set to 3 to print debug messages, and 0 for no debug messages**
client_socket.send( b"trick.var_pause()\n" )
client_socket.send( b"trick.var_ascii()\n" )
client_socket.send( b"trick.var_add(\"dyn.skydiver.pos\") \n" +    # Height
                   b"trick.var_add(\"dyn.skydiver.Fd\") \n" +      # Drag force
                   b"trick.var_add(\"dyn.skydiver.vel\") \n" +     # Velocity
                   b"trick.var_add(\"trick_sys.sched.mode\") \n" )
client_socket.send( b"trick.var_unpause()\n" )

# ----------------------------------------------------------------------
# 8.0 Repeatedly read and process the responses from the variable server.
while(True):
    # 8.1 Read the response line from the variable server.
    line = insock.readline()
    if line == '':
        break

    # 8.2 Split the line into an array of value fields.
    field = line.split("\t")

    if len(field) >= 4:  # We now expect height, Fd, velocity, and mode
        try:
            height = float(field[1])
            drag_force = float(field[2])
            velocity = float(field[3])
            simMode = int(field[4])
            
            # Update skydiver position
            cx = WIDTH/2
            cy = HEIGHT - MARGIN - (height * SCALE)  # Scale adjusted for 500px height
            canvas.coords(skydiver, 
                        cx-skydiverSize/2, cy-skydiverSize/2,
                        cx+skydiverSize/2, cy+skydiverSize/2)
            
            # Update text displays
            canvas.itemconfig(dragForceText, text=f"Drag: {drag_force:.1f} N")
            canvas.itemconfig(heightText, text=f"Height: {height:.1f} m")
            canvas.itemconfig(velocityText, text=f"Velocity: {velocity:.1f} m/s")
            
            # Update mode display
            if simMode == MODE_FREEZE:
                canvas.itemconfig(modeText, text="FREEZE", fill="blue")
                jumpButton.config(state=NORMAL)
            else:
                canvas.itemconfig(modeText, text="RUN", fill="red")
                jumpButton.config(state=DISABLED)
                
            # Handle jump command
            if simMode == MODE_FREEZE:
                if jumpCommand:
                    jumpCommand = False
                    jumpButton.config(state=DISABLED)
                    # 8.6.1 Command the sim to assign the slider values to init_speed, and init_angle.
                    client_socket.send( b"dyn.skydiver.pos0 = " + bytes(str(heightScale.get()), 'UTF-8') + b" \n")
                    client_socket.send( b"dyn.skydiver.m = " + bytes(str(massScale.get()), 'UTF-8') + b" \n")
                    # 8.6.2 Command the sim to re-run the skydiver_init() job.
                    client_socket.send( b"trick.skydiver_init( dyn.skydiver )\n")
                    # 8.6.3 Command the sim to run.
                    client_socket.send( b"trick.exec_run()\n")
            
        except (ValueError, IndexError) as e:
            print(f"Error parsing data: {field} - {e}")
            continue
    
    # 8.7 Update the Tk graphics.
    tk.update()

# ----------------------------------------------------------------------
# 9.0 Keep the window open, when the data stops.
tk.mainloop()
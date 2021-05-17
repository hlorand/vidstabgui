from tkinter import *
from tkinter import filedialog as Filedialog
from tkinter import messagebox as Messagebox
import subprocess
import time

tk = Tk()
tk.title("VidStab GUI")
tk.widgetcount = 1

"""
Base class for every GUI element.

Stores the name and description. First it creates a frame and a label for the element, then
places the element into the grid.

Every GUI element has a numeric value that is used when generating the ffmpeg command. This
value is stored in a variable called "valueHolder". You can get this value as is with getValue()
or you can get the command line attribute in "valuename=value" format with getAttribute().
"""
class GuiThing:
    valueHolder = None
    
    def __init__(self, name, description):
        self.name = name

        self.frame = LabelFrame(tk, text=name.capitalize(), padx=10, pady=0)
        tk.widgetcount += 1
        self.frame.grid( row=int(tk.widgetcount/2), column=tk.widgetcount%2, sticky=NSEW )
        
        self.label = Label(self.frame, text=description, wraplength=500)
        self.label.pack(anchor=NW)
    
    def getValue(self):
        return self.valueHolder.get()

    def getArgument(self):
        return self.name + "=" + str(self.valueHolder.get())


"""
GUI element responsible for opening files

A single button that calls the browse() method, with which you can browse for video files.
"""
class GuiFiles(GuiThing):
    def browse(self):
        types = [ ('MP4 files', '*.mp4'),
                  ('MOV files', '*.mov'),
                  ('AVI files', '*.avi'),
                  ('MPG files', '*.mpg'),
                  ('MPEG files','*.mpeg'),
                  ('M4V files', '*.m4v') ]
        self.files = list( Filedialog.askopenfilename(multiple=True, filetypes=types ) )

        if len(self.files) == 1:
            self.label.configure(fg="green", text=f"{self.files[0].split('/').pop()} selected" )
        else:
            self.label.configure(fg="green", text=f"{len(self.files)} file(s) selected" )
    
    def __init__(self, name, description):
        super().__init__(name, description)

        self.files = []

        self.button = Button(self.frame,text = "Browse video files...", padx="10", command=self.browse)
        self.button.pack(anchor=NW)


"""
Slider GUI element

A simple slider. You can set the slider start and end value and step size.
"""
class GuiSlider(GuiThing):
    def __init__(self, name, description,  start, end, default, stepsize=1):
        super().__init__(name, description)

        self.valueHolder = Scale(self.frame, from_=start, to=end, length=600, resolution=stepsize, orient=HORIZONTAL)
        self.valueHolder.pack(anchor=NW)
        self.valueHolder.set(default)


"""
Radio button group GUI element which

You can set the options (value-description pairs) in the options list
"""
class GuiRadio(GuiThing):
    def __init__(self, name, description, options):
        super().__init__(name, description)

        self.options = options

        # Add every option as a radio button
        self.value = IntVar()
        for i in range(len(options)):
            radio = Radiobutton(self.frame, text=f"{options[i][0]} ({options[i][1]})", variable=self.value, value=i)
            radio.pack(anchor=NW)

        self.valueHolder = self

    # Define a get() attribute to get the selected radio button value from the options list (and not as a single int)
    def get(self):
        return self.options[ self.value.get() ][0]


"""
A function that calls ffmpeg with the selected settings
"""
def stabilize():
    # Check if files selected
    if len(files.files) == 0:
        Messagebox.showerror(title="Error", message="No files selected")
        return

    # Check if ffmpeg.exe is present
    if not os.path.isfile("./ffmpeg.exe"):
        Messagebox.showerror(title="Error", message="Can't find ffmpeg.exe. Please download it from https://www.gyan.dev/ffmpeg/builds/ and place it next to vidstabgui.exe")
        return
    
    for file in files.files:
        # Generate output filename. ( inputfilename.stabilized.time.mp4 )
        output = ".".join( file.split(".")[0:-1] + ["stabilized",str(int(time.time())), "mp4"] )

        # Show notification that the analysis has started
        info.configure(fg="purple", text="Analysing: " + file.split("/").pop() )
        tk.update()

        # Analyze motion
        command  = f"ffmpeg.exe -i \"{file}\""
        command += f" -vf vidstabdetect={shakiness.getArgument()}"
        command += f" -f null -"
        print(command)
        subprocess.call(command, shell=True)

        # Show notification that the stabilization process has started
        info.configure(fg="blue", text="Stabilizing: " + file.split("/").pop() )
        tk.update()

        # Stabilize video
        command  = f"ffmpeg.exe -i \"{file}\""
        command += f" -crf {crf.getValue()}"
        command += f" -preset medium"
        command += f" -vf unsharp=5:5:{sharpening.getValue()}:3:3:{sharpening.getValue()/2},"
        command += f"vidstabtransform="
        command += f"{smoothing.getArgument()}"
        command += f":{crop.getArgument()}"
        command += f":{optalgo.getArgument()}"
        command += f":{optzoom.getArgument()}"
        command += f":{zoom.getArgument()}"
        command += f":{zoomspeed.getArgument()}"
        command += f":{interpol.getArgument()}"
        command += f":{maxshift.getArgument()}"
        command += f":maxangle={-1 if maxangle.getValue() < 0 else maxangle.getValue()*3.1415/180}"
        command += f":input='transforms.trf'"
        command += f" \"{output}\" -y"
        print(command)
        subprocess.call(command, shell=True)

    # Show notification that the job done
    info.configure(fg="green", text="Done." )

    # Open output folder in the file manager
    outputfolder = "/".join( file.split("/")[0:-1] )
    print(outputfolder)
    subprocess.call(f"start \"\" \"{outputfolder}\" ", shell=True)


#########################################################################
# Build GUI
files      = GuiFiles("input files", "Open mp4, mov, avi... videos here")

shakiness  = GuiSlider("shakiness", "On a scale of 1 to 10 how quick is the camera shake in your opinion?", 1, 10, 6)
smoothing  = GuiSlider("smoothing", "Number of frames used in stabilization process. Bigger frame count = smoother motion. (A number of 10 means that 21 frames are used: 10 in the past and 10 in the future.) ", 1, 300, 60)
optalgo    = GuiRadio("optalgo", "Set the camera path optimization algorithm.", [ ["gauss","Gaussian kernel low-pass filter on camera motion"],["avg"," Averaging on transformations"] ])

optzoom    = GuiRadio("optzoom", "Set optimal zooming to avoid blank-borders. ", [ ["0","Disabled"],["1","Optimal static zoom value is determined, only very strong movements will lead to visible borders"], ["2", "Optimal adaptive zoom value is determined"] ])
zoom       = GuiSlider("zoom", "Zoom in or out (percentage).", -100, 100, 0)
zoomspeed  = GuiSlider("zoomspeed", "Set percent to zoom maximally each frame (enabled when optzoom is set to 2).", 0, 5, 0.25, 0.05)

crop       = GuiRadio("crop", "How to deal with empty frame borders", [ ["black","Fill the border-areas black."],["keep","Keep image information from previous frame"] ])
interpol   = GuiRadio("interpol", "Specify type of interpolation", [ ["bilinear","Linear in both directions"],["bicubic","Cubic in both directions - slow"],["linear","Linear only horizontal"],["no","No interpolation"] ])

maxshift   = GuiSlider("maxshift", "Set maximal number of pixels to translate frames. (-1 = no limit)", -1, 640, -1)
maxangle   = GuiSlider("maxangle", "Set maximal angle in degrees to rotate frames. (-1 = no limit)", -1, 360, -1)

sharpening = GuiSlider("sharpening", "A little bit of sharpening is recommended after stabilization.", 0, 1.5, 0.8, 0.05)
crf        = GuiSlider("crf", "Output video compression rate factor. Smaller crf: Better quality, greater file size. Bigger crf: Better compression, smaller file size.", 0, 51, 21)


# A frame that holds the Stabilize button
stabilizeFrame = LabelFrame(tk, text="Stabilize", padx=0, pady=0)
tk.widgetcount += 1
stabilizeFrame.grid( row=int(tk.widgetcount/2), column=tk.widgetcount%2, sticky=NSEW )

info = Label(stabilizeFrame, text="")
info.pack(anchor=NW)

stabilizeButton = Button(stabilizeFrame, text="Stabilize", padx=20, pady=10, bg="white", command=stabilize )
stabilizeButton.pack(pady=10)

tk.mainloop()

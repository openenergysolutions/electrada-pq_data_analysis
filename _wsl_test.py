import matplotlib
# Setting needed by WSL (Windows Subsystem for Linux), WSL doesn't have a display server by default to render graphical windows
# Need to run "sudo apt install python3-tk", then set TkAgg as the backend
matplotlib.use("TkAgg")

# Test if the plot window works
import matplotlib.pyplot as plt
plt.plot([1, 2, 3], [1, 4, 9])
plt.show()

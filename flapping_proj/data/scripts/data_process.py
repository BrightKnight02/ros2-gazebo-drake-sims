import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.animation import FuncAnimation
import matplotlib.ticker as ticker
import shutil
import numpy as np
import sys
import os
import math
# Convert quaternion to Euler angles
def quaternion_to_euler(x, y, z, w,length=.02):
    t0 = +2.0 * (w * x + y * z)
    t1 = +1.0 - 2.0 * (x * x + y * y)
    roll_x = math.atan2(t0, t1)

    t2 = +2.0 * (w * y - z * x)
    t2 = +1.0 if t2 > +1.0 else t2
    t2 = -1.0 if t2 < -1.0 else t2
    pitch_y = math.asin(t2)

    t3 = +2.0 * (w * z + x * y)
    t4 = +1.0 - 2.0 * (y * y + z * z)
    yaw_z = math.atan2(t3, t4)

    return roll_x * length, pitch_y * length, yaw_z * length

def quiver_data_to_segments(X, Y, Z, u, v, w, length=1):
    segments = (X, Y, Z, X+v*length, Y+u*length, Z+w*length)
    segments = np.array(segments).reshape(6,-1)
    return [[[x, y, z], [u, v, w]] for x, y, z, u, v, w in zip(*list(segments))]

# Update function for animation
def update(frame):
    ax.cla()  # Clear the current axes

    # Plot the trajectory
    ax.plot(position_x[:frame+1], position_y[:frame+1], position_z[:frame+1], marker='o', markersize=1, linestyle='dashed')

    # Set labels and title
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.set_title('Object Trajectory')
    ax.set_xlim3d(np.min(position_x)-3, np.max(position_x)+3)
    ax.set_ylim3d(np.min(position_y)-3, np.max(position_y)+3)
    ax.set_zlim3d(np.min(position_z)-10, np.max(position_z)+10)

    roll, pitch, yaw = quaternion_to_euler(quaternion_x[frame], quaternion_y[frame], quaternion_z[frame], quaternion_w[frame])
    quivers = ax.quiver(position_x[frame], position_y[frame], position_z[frame], roll, pitch, yaw, color='r', label='Model',linestyle='--', alpha=0.5, length=.2, normalize=True,)
    return quivers

#another one without without max and min, copy pasted
def update_dynamic(frame):
    ax.cla()  # Clear the current axes

    # Plot the trajectory
    ax.plot(position_x[:frame+1], position_y[:frame+1], position_z[:frame+1], marker='o', markersize=1, linestyle='dashed')

    # Set labels and title
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.set_title('Object Trajectory')

    roll, pitch, yaw = quaternion_to_euler(quaternion_x[frame], quaternion_y[frame], quaternion_z[frame], quaternion_w[frame])
    quivers = ax.quiver(position_x[frame], position_y[frame], position_z[frame], roll, pitch, yaw, color='r', label='Model',linestyle='--', alpha=0.5, length=.2, normalize=True,)
    return quivers

# script entry point
# Read the data from the CSV file
csv_name = sys.argv[2] if len(sys.argv) == 3 else 'data.csv'
data = pd.read_csv(csv_name)

if len(sys.argv) < 2:
    print("Usage: python3 data_process.py <folder_name> <optional:csv_name>")
    print("No folder path provided, data will be saved in current directory")
    folder_name = ''
else:
    folder_name = sys.argv[1]
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

#script dir to get abs path
script_dir = os.path.dirname(os.path.abspath(__file__))
csv_source = os.path.join(script_dir, csv_name)
csv_dest = os.path.join(script_dir, folder_name, 'data', csv_name)

dest_folder = os.path.dirname(csv_dest)
if not os.path.exists(dest_folder):
    os.makedirs(dest_folder)

shutil.copy2(csv_source, csv_dest)

folder_name = os.path.join(folder_name, 'data_plots')
if not os.path.exists(folder_name):
    os.makedirs(folder_name)
# Extract the required columns
time = data['time'].to_numpy()
position_x = data['position_x'].to_numpy()
position_y = data['position_y'].to_numpy()
position_z = data['position_z'].to_numpy()
quaternion_x = data['quaternion_x'].to_numpy()
quaternion_y = data['quaternion_y'].to_numpy()
quaternion_z = data['quaternion_z'].to_numpy()
quaternion_w = data['quaternion_w'].to_numpy()
joint_LW_J_Pitch = data['joint_LW_J_Pitch'].to_numpy()
joint_RW_J_Pitch = data['joint_RW_J_Pitch'].to_numpy()
joint_LW_J_Flap = data['joint_LW_J_Flap'].to_numpy()
joint_RW_J_Flap = data['joint_RW_J_Flap'].to_numpy()

# Convert angles to degrees
joint_LW_J_Pitch_deg = np.degrees(joint_LW_J_Pitch)
joint_RW_J_Pitch_deg = np.degrees(joint_RW_J_Pitch)
joint_LW_J_Flap_deg = np.degrees(joint_LW_J_Flap)
joint_RW_J_Flap_deg = np.degrees(joint_RW_J_Flap)

# Create synchronized plots for joint angles
fig2, ax2 = plt.subplots(2, 2)

plt.subplots_adjust(left=0.12,
                    bottom=0.1,
                    right=0.98,
                    top=0.9,
                    wspace=0.4,
                    hspace=0.4)

major_locator = ticker.MultipleLocator(base=1)
minor_locator = ticker.MultipleLocator(base=0.25)
ax2[0, 0].plot(time, joint_LW_J_Pitch_deg, label='LW_J_Pitch')
ax2[0, 0].set_xlabel('Time (s)')
ax2[0, 0].set_ylabel('Angle (degrees)')
ax2[0, 0].legend()
ax2[0, 0].xaxis.set_major_locator(major_locator)
ax2[0, 0].xaxis.set_minor_locator(minor_locator)
# ax2[0, 0].yaxis.set_major_locator(ticker.MultipleLocator(base=3.14/2))
ax2[0, 0].grid(True)

ax2[0, 1].plot(time, joint_RW_J_Pitch_deg, label='RW_J_Pitch')
ax2[0, 1].set_xlabel('Time (s)')
ax2[0, 1].set_ylabel('Angle (degrees)')
ax2[0, 1].legend()
ax2[0, 1].xaxis.set_major_locator(major_locator)
ax2[0, 1].xaxis.set_minor_locator(minor_locator)
# ax2[0, 1].yaxis.set_major_locator(ticker.MultipleLocator(base=3.14/2))
ax2[0, 1].grid(True)

ax2[1, 0].plot(time, joint_LW_J_Flap_deg, label='LW_J_Flap')
ax2[1, 0].set_xlabel('Time (s)')
ax2[1, 0].set_ylabel('Angle (degrees)')
ax2[1, 0].legend()
ax2[1, 0].xaxis.set_major_locator(major_locator)
ax2[1, 0].xaxis.set_minor_locator(minor_locator)
# ax2[1, 0].yaxis.set_major_locator(ticker.MultipleLocator(base=3.14/2))
ax2[1, 0].grid(True)

ax2[1, 1].plot(time, joint_RW_J_Flap_deg, label='RW_J_Flap')
ax2[1, 1].set_xlabel('Time (s)')
ax2[1, 1].set_ylabel('Angle (degrees)')
ax2[1, 1].legend()
ax2[1, 1].xaxis.set_major_locator(major_locator)
ax2[1, 1].xaxis.set_minor_locator(minor_locator)
# ax2[1, 1].yaxis.set_major_locator(ticker.MultipleLocator(base=3.14/2))
ax2[1, 1].grid(True)
for ax in ax2.flat:
    ax.grid(which='minor', linestyle=':', alpha=0.75)
    # for i, label in enumerate(ax.get_xticklabels()):
    #     if i % 4 != 0:
    #         label.set_visible(False)

# Save the synchronized plots as an image file
# plt.grid(which='minor', linestyle=':', alpha=0.75)
fig2.savefig(folder_name + '/joint_angles.png')


#big plot
major_locator = ticker.MultipleLocator(base=.1)
minor_locator = ticker.MultipleLocator(base=0.05)
start_time = 2
end_time = 2.3
start_idx = np.argmax(time >= start_time)
end_idx = np.argmax(time >= end_time)
time_slice = time[start_idx:end_idx]
angle_slice = joint_LW_J_Pitch_deg[start_idx:end_idx]
fig = plt.figure()
plt.plot(time_slice, angle_slice, label='Angle Data (3s to 3.3s)')
plt.gca().xaxis.set_major_locator(major_locator)
plt.gca().xaxis.set_minor_locator(minor_locator)
plt.xlabel('Time (s)')
plt.ylabel('Angle (deg)')
plt.legend()
fig.savefig(folder_name + '/joint_angles_zoom.png')
plt.show()

# Create the 3D figure (initialization)
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
roll, pitch, yaw = quaternion_to_euler(quaternion_x[0], quaternion_y[0], quaternion_z[0], quaternion_w[0])
ax.plot(position_x, position_y, position_z, marker='o', markersize=2)
fig.savefig(folder_name + '/static_traj.png')
quivers = ax.quiver(position_x[0], position_y[0], position_z[0], roll, pitch, yaw, color='r', label='Model', alpha=0.5)
ax.plot(position_x[0], position_y[0], position_z[0], marker='o')

# Create animation
print("Creating limited animation...")
animation = FuncAnimation(fig, update, frames=len(time), interval=100, blit=False)
`animation.save(folder_name + '/animation.gif', writer='pillow')
`
# print("Creating dynamic animation...")
animation = FuncAnimation(fig, update_dynamic, frames=len(time), interval=100, blit=False)
animation.save(folder_name + '/animation_dynamic.gif', writer='pillow')

# Show the plots
# plt.show()
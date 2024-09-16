import cv2
import numpy as np
import matplotlib.pyplot as plt
from SLAM import SLAM
from OpenDJI import OpenDJI
from VCS import VideoCapture

class SLAMSystem:
    def __init__(self):
        """
        Initialize the SLAM System for creating, navigating, and plotting a 3D map.
        """
        self.fig, self.ax = plt.subplots()
        
    def create_3d_map(self, cam, output_file: str):
        """
        Run the SLAM to create a 3D map while plotting the current location and heading.

        Args:
            video_source (str): Path to the video file or camera input (e.g., 0 for default camera).
            output_file (str): File path to save the map data when user quits (by pressing 'q').
        """
        plt.ion()  # Interactive mode for real-time plotting
        
        # Initialize SLAM object
        slam = SLAM(intrinsic_matrix=np.eye(3))  # Replace with actual intrinsic matrix
        
        while cv2.waitKey(10) != ord('q'):
            _, _ = cam.read()
            _, _ = cam.read()
            _, _ = cam.read()
            _, _ = cam.read()
            ret, frame = cam.read()
            if not ret:
                continue
            
            # Process frame with SLAM
            R, t = slam.process_frame(frame)
            if R is None:
                continue
            
            print(t.round(2))
            # Plot current position and heading on 2D map
            self._plot_position_heading(R, t)
            
            # Plot known and new features on the frame
            frame_with_features = self._plot_frame_features(frame, slam)
            cv2.imshow('SLAM Frame', frame_with_features)
            
            # Update 2D plot
            plt.draw()
            plt.pause(0.01)
        
        cv2.destroyAllWindows()
        
        # Save map data to file
        slam.export_state(output_file)
        print(f"Map data saved to {output_file}")

    def navigate(self, cam, map_file: str, save_new_points : bool = False):
        """
        Run the SLAM with navigation using an existing 3D map.

        Args:
            video_source (str): Path to the video file or camera input (e.g., 0 for default camera).
            map_file (str): Path to the saved map file to load for navigation.
        """
        # Load the saved map data
        slam = SLAM(intrinsic_matrix=np.eye(3), save_new_points=save_new_points)
        slam.import_state(map_file)
        
        plt.ion()  # Interactive mode for real-time plotting
        
        while True:
            ret, frame = cam.read()
            ret, frame = cam.read()
            ret, frame = cam.read()
            ret, frame = cam.read()
            ret, frame = cam.read()
            if not ret:
                break

            # Process frame with SLAM
            R, t = slam.process_frame(frame)
            
            # Plot current position and heading on 2D map
            self._plot_position_heading(R, t)
            
            # Update 2D plot
            plt.draw()
            plt.pause(0.01)
            
            # Quit navigation if 'q' is pressed
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        
        cv2.destroyAllWindows()

    def plot_map(self, map_file: str):
        """
        Load a SLAM 3D map from a file and plot the 3D points along with the 2D map.

        Args:
            map_file (str): File path to the saved map data.
        """
        self._3d_fig = plt.figure()
        self.ax_3d = self._3d_fig.add_subplot(111, projection='3d')

        # Load the saved map data
        slam = SLAM(intrinsic_matrix=np.eye(3))
        slam.import_state(map_file)
        
        # Extract 3D points and plot them
        world_points = slam.get_world_points()
        self.ax_3d.clear()
        self.ax_3d.scatter(world_points[:, 0], world_points[:, 1], world_points[:, 2], c='red', marker='o')
        self.ax_3d.set_title("3D Map - Global Points")
        plt.show()

    def _plot_frame_features(self, frame: np.ndarray, slam: SLAM) -> np.ndarray:
        """
        Draw the feature points on the frame. Known 3D points are drawn in black, and new points in red.

        Args:
            frame (np.ndarray): Current video frame.
            slam (SLAM): SLAM object used to get feature points and matches.

        Returns:
            np.ndarray: The frame with drawn feature points.
        """
        kps, _ = slam.get_previous_keypoints_descriptors()
        
        if kps is None:
            return frame
        
        kps = np.array(kps, dtype=object)
        
        unmatched_idxes = slam.get_unmatched()
        matched_idxes = slam.get_matched()
        
        for kp in kps[matched_idxes]:
            cv2.circle(frame, (int(kp.pt[0]), int(kp.pt[1])), 3, (255, 255, 0), -1)
        for kp in kps[unmatched_idxes]:
            cv2.circle(frame, (int(kp.pt[0]), int(kp.pt[1])), 3, (0, 0, 255), -1)
        
        return frame

    def _plot_position_heading(self, R: np.ndarray, t: np.ndarray):
        """
        Plot the current position and heading on the 2D map.

        Args:
            R (np.ndarray): Rotation matrix (3x3).
            t (np.ndarray): Translation vector (3x1).
        """
        # Clear the previous plot
        # self.ax.clear()
        self.ax.grid(True)
        
        # Plot the current position
        # t.round(1)
        self.ax.scatter(t[0], t[2], color='blue', label='Current Position')
        
        # # FIX:
        # # Plot the heading using the rotation matrix
        # heading_x = t[0] + R[0, 0]
        # heading_y = t[2] + R[2, 0]
        # self.ax.arrow(t[0], t[2], heading_x - t[0], heading_y - t[2], 
        #             head_width=0.1, color='green', label='Heading')
        
        # Set plot title and labels
        self.ax.set_title("2D Map - Current Position")
        self.ax.set_xlabel("X")
        self.ax.set_ylabel("Z")
        
class DroneCam:
    def __init__(self, address) -> None:
        self.drone = OpenDJI(address)
    def read(self):
        frame = self.drone.getFrame()
        if frame is None:
            return False, None
        frame = cv2.resize(frame, dsize = None,
                    fx = 0.25,
                    fy = 0.25)
        return True, frame
    
    def release(self):
        pass
        
sys = SLAMSystem()

cam = DroneCam("10.0.0.4")
# cam = cv2.VideoCapture(0)
# cam = cv2.VideoCapture("video1.mp4")

vcs = VideoCapture(cam)

sys.create_3d_map(vcs, "myMap1")
# sys.navigate(vcs, "myMap1")
# sys.plot_map("myMap1")

cam.release()

"""
********************************************
*                                          *
*           Author: Bahadur Singh Thakur
*           E-mail: bahadur.th7@gmail.com  *
*           Date: 12-Dec-2024              *
*                                          *
********************************************
"""
import logging
import time
from stream.GstRtsp import GstRtsp
from camera.load_camera import LoadCamera
from inference.load_inference_engines import LoadInferenceEngines
from camera.Camera import Camera
import threading

class StartPipeline:
    def __init__(self, cameras: list):
        self.cameras = cameras
        self.logger = logging.getLogger(self.__class__.__name__)
        self.threads = []

    def start_gst_threads(self):
        """
        Starts GStreamer capture threads for each camera.
        """
        for camera in self.cameras:
            self.logger.info(f"Initializing GStreamer thread for camera: {camera.camera_id} with RTSP URL: {camera.rtsp_url}")
            thread = GstRtsp(camera)
            thread.daemon = True  # Ensure the threads exit when the main program exits
            thread.start()
            self.threads.append(thread)

    def monitor_threads(self):
        """
        Monitors the threads and restarts any that have stopped unexpectedly.
        """
        try:
            while True:
                for thread in self.threads:
                    # Check if thread is alive and if it's running
                    if not thread.is_alive():
                        self.logger.warning(f"GStreamer thread for camera {thread.camera.camera_id} has stopped unexpectedly. Restarting...")
                        new_thread = GstRtsp(thread.camera)
                        new_thread.daemon = True  # Make new thread daemon as well
                        new_thread.start()
                        # Update the threads list by replacing the old thread
                        self.threads.remove(thread)
                        self.threads.append(new_thread)
                time.sleep(10)  # Interval to check thread status
        except KeyboardInterrupt:
            self.logger.info("Stopping GStreamer RTSP capture...")
            for thread in self.threads:
                try:
                    # Gracefully stop each thread (assuming stop_capture is implemented)
                    thread.stop_capture()
                    thread.join()  # Wait for threads to finish before exiting
                except Exception as e:
                    self.logger.error(f"Error stopping thread for camera {thread.camera.camera_id}: {e}")

    def run(self):
        """
        Starts the GStreamer threads and begins monitoring them.
        """
        self.start_gst_threads()
        self.monitor_threads()

'''import logging
import time
from stream.GstRtsp import GstRtsp
from camera.load_camera import LoadCamera
from inference.load_inference_engines import LoadInferenceEngines
from camera.Camera import Camera

class StartPipeline:
    def __init__(self, cameras: list):
        self.cameras = cameras
        self.logger = logging.getLogger(self.__class__.__name__)
        self.threads = []

    def start_gst_threads(self):
        for camera in self.cameras:
            self.logger.info(f"Initializing GStreamer thread for camera: {camera.camera_id} with RTSP URL: {camera.rtsp_url}")
            thread = GstRtsp(camera)
            thread.start()
            self.threads.append(thread)

    def monitor_threads(self):
        try:
            while True:
                for thread in self.threads:
                    if not thread.is_alive() and thread.is_running:
                        self.logger.warning(f"GStreamer thread for camera {thread.camera.camera_id} has stopped unexpectedly. Restarting...")
                        new_thread = GstRtsp(thread.camera)
                        new_thread.start()
                        self.threads.remove(thread)
                        self.threads.append(new_thread)
                time.sleep(10)  # Adjust the interval as needed for checking
        except KeyboardInterrupt:
            self.logger.info("Stopping GStreamer RTSP capture...")
            for thread in self.threads:
                thread.stop_capture()
                thread.join()

    def run(self):
        self.start_gst_threads()
        self.monitor_threads()
'''
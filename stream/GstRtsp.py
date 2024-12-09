"""
********************************************
*                                          *
*           Author: Bahadur Singh Thakur
*           E-mail: bahadur.th7@gmail.com  *
*           Date: 12-Dec-2024              *
*                                          *
********************************************
"""
import os
import time
import threading
import logging
from PIL import Image
import numpy as np
import psutil
import gi
gi.require_version('Gst', '1.0')
from gi.repository import GLib, Gst
import cv2
from concurrent.futures import ThreadPoolExecutor
from rules.RuleExecutor import RuleExecutor
import gc

# Initialize GStreamer
Gst.init(None)

# Set up logging
logger = logging.getLogger('GstRtspLogger')
logger.setLevel(logging.INFO)
file_handler = logging.FileHandler('gstreamer_rtsp.log')
file_handler.setLevel(logging.INFO)
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)
logger.addHandler(file_handler)
logger.addHandler(console_handler)

class RtspAppSinkListener:
    def __init__(self, camera, inference, gst_rtsp_instance):
        self.camera = camera
        self.detection_map = {}
        self.camera_id = camera.getCameraId()
        self.frame_count = 0
        self.last_processed_time = 0  # To track the time of the last processed frame
        self.FPS = camera.get_fps()  # Desired FPS
        self.frame_interval = 1 / self.FPS  # Time interval in seconds between frames
        self.inferences_receiving = False
        self.lock = threading.Lock()
        self.inference = inference
        self.rule_executor = RuleExecutor()
        self.executor = ThreadPoolExecutor(max_workers=2)
        self.gst_rtsp_instance = gst_rtsp_instance

    def __call__(self, sink):
        sample = sink.emit("pull-sample")
        if sample:
            buffer = sample.get_buffer()
            caps = sample.get_caps()

            structure = caps.get_structure(0)
            width = structure.get_value("width")
            height = structure.get_value("height")
            format_ = structure.get_value("format")
            success, map_info = buffer.map(Gst.MapFlags.READ)

            if success:
                data = map_info.data
                try:
                    self.executor.submit(self.process_frame, data, width, height, format_)
                except RuntimeError as e:
                    logger.error(f"Failed to submit frame processing task: {e}")
                buffer.unmap(map_info)
        return Gst.FlowReturn.OK

    def process_frame(self, data, width, height, format_):
        current_time = time.time()
        if current_time - self.last_processed_time >= self.frame_interval:
            self.last_processed_time = current_time
        else:
            # Skip processing this frame if the interval hasn't passed
            del data
            return

        try:
            arr = np.frombuffer(data, dtype=np.uint8)

            #logger.info(f"Array shape: {arr.shape}, expected size: {height * width * 3}")

            if arr.size != height * width * 3:
                raise ValueError("Invalid image data: size does not match expected dimensions")

            # Process frame for supported format (RGB)
            if format_ == "RGB":
                cv_image = arr.reshape((height, width, 3))
            else:
                logger.error(f"Unsupported format: {format_}")
                return

            self.camera.set_rgb_image(cv_image)

            # Perform inference on the frame
            for detection_model, network_inference in self.camera.get_inferenceMap().items():
                network_inference.process_image(cv_image, detection_model, self.camera)
                self.detection_map[detection_model] = self.camera.get_detections()

            self.rule_executor.execute_rules(self.camera, self.detection_map)
            self.detection_map.clear()

            # Explicitly delete the variables after processing
            del arr
            del cv_image

        except ValueError as ve:
            logger.error(f"ValueError: {ve}")
        except Exception as e:
            logger.error(f"Error processing frame: {e}")

    def isInferencesReceiving(self):
        return self.inferences_receiving

class GstRtsp(threading.Thread):
    def __init__(self, camera, memory_limit_mb=2400):
        threading.Thread.__init__(self)
        self.camera = camera
        self.is_running = True
        self.bEOS = False
        self.frame_count = 0
        self.videoAppSinkListener = None
        self.pipeline = None
        self.loop = None
        self.lock = threading.Lock()
        self.memory_limit_mb = memory_limit_mb
        self.timeout_id = None

    def run(self):
        logger.info(f"Starting GStreamer Camera Capture for {self.camera.getCameraId()}...")
        rtsp_url = self.camera.getRtspUrl()
        logger.info(f"Start GStreamer streaming: {self.camera.getCameraId()}, URL: {rtsp_url}")

        self.create_pipeline(rtsp_url)
        self.pipeline.set_state(Gst.State.PLAYING)

        self.loop = GLib.MainLoop()
        try:
            self.loop.run()
        except Exception as e:
            logger.error(f"Error running main loop for {self.camera.getCameraId()}: {e}")

    def create_pipeline(self, rtsp_url):
        pipeline_name = f"pipe_{self.camera.getCameraId()}"
        gst_command = self.get_gpu_pipeline(rtsp_url) if self.camera.isUseGpuDecoder() else self.get_cpu_pipeline(rtsp_url)

        if self.pipeline:
            self.pipeline.set_state(Gst.State.NULL)
            self.pipeline = None

        self.pipeline = Gst.parse_launch(gst_command)
        if not self.pipeline:
            logger.error(f"Failed to create the GStreamer pipeline for {self.camera.getCameraId()}.")
            return

        self.pipeline.set_name(pipeline_name)
        video_app_sink = self.pipeline.get_by_name("videoAppSink")

        if not video_app_sink:
            logger.error(f"Failed to get video app Sink for {self.camera.getCameraId()}.")
            self.pipeline.set_state(Gst.State.NULL)
            return

        video_app_sink.set_property("emit-signals", True)
        video_app_sink.set_property('sync', False)
        video_app_sink.set_property('max-buffers', 1)
        video_app_sink.set_property('drop', True)

        inference = self.camera.get_inference()
        self.videoAppSinkListener = RtspAppSinkListener(self.camera, inference, self)
        video_app_sink.connect("new-sample", self.videoAppSinkListener)

        bus = self.pipeline.get_bus()
        bus.add_signal_watch()
        bus.connect("message::eos", self.on_eos)
        bus.connect("message::error", self.on_error)
        bus.connect("message::warning", self.on_warning)

    def on_eos(self, bus, message):
        logger.info(f"End of stream (EOS) received for {self.camera.getCameraId()}")
        self.bEOS = True
        self.pipeline.set_state(Gst.State.NULL)
        if self.loop:
            self.loop.quit()

    def on_error(self, bus, message):
        error, debug_info = message.parse_error()
        logger.error(f"Error from element {message.src.get_name()} for {self.camera.getCameraId()}: {error.message}, Debugging information: {debug_info}")
        self.bEOS = True
        self.pipeline.set_state(Gst.State.NULL)
        if self.loop:
            self.loop.quit()

    def on_warning(self, bus, message):
        warning, debug_info = message.parse_warning()
        logger.warning(f"Warning from element {message.src.get_name()} for {self.camera.getCameraId()}: {warning.message}, Debugging information: {debug_info}")

    def get_cpu_pipeline(self, rtsp_url):
        return (
            f"rtspsrc location=\"{rtsp_url}\" ! rtp{self.camera.get_encode_mode()}depay ! {self.camera.get_encode_mode()}parse ! avdec_{self.camera.get_encode_mode()} ! videoconvert ! video/x-raw,format={self.camera.get_formats()} ! appsink name=videoAppSink"
        )

    def get_gpu_pipeline(self, rtsp_url):
        return (
            f"rtspsrc protocols=GST_RTSP_LOWER_TRANS_TCP name={self.camera.getCameraId()} location={rtsp_url} ! "
            f"rtp{self.camera.get_encode_mode()}depay ! {self.camera.get_encode_mode()}parse ! nvv4l2decoder ! "
            f"nvvideoconvert ! video/x-raw,width={self.camera.get_width()},height={self.camera.get_height()},format={self.camera.get_formats()} ! "
            f"videoscale ! videoconvert ! video/x-raw,width={self.camera.get_width()},height={self.camera.get_height()} ! "
            "appsink name=videoAppSink"
        )

'''import os
import time
import threading
import logging
from PIL import Image
import numpy as np
import psutil
import gi
gi.require_version('Gst', '1.0')
from gi.repository import GLib, Gst
import cv2
from concurrent.futures import ThreadPoolExecutor
from rules.RuleExecutor import RuleExecutor
import gc

# Initialize GStreamer
Gst.init(None)

# Set up logging
logger = logging.getLogger('GstRtspLogger')
logger.setLevel(logging.INFO)
file_handler = logging.FileHandler('gstreamer_rtsp.log')
file_handler.setLevel(logging.INFO)
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)
logger.addHandler(file_handler)
logger.addHandler(console_handler)

class RtspAppSinkListener:
    def __init__(self, camera, inference, gst_rtsp_instance):
        self.camera = camera
        self.detection_map = {}
        self.camera_id = camera.getCameraId()
        self.frame_count = 0
        self.last_processed_time = 0  # To track the time of the last processed frame
        self.FPS = camera.get_fps()  # Desired FPS
        self.frame_interval = 1 / self.FPS  # Time interval in seconds between frames
        self.inferences_receiving = False
        self.lock = threading.Lock()
        self.inference = inference
        self.rule_executor = RuleExecutor()
        self.executor = ThreadPoolExecutor(max_workers=2)
        self.gst_rtsp_instance = gst_rtsp_instance

    def __call__(self, sink):
        sample = sink.emit("pull-sample")
        if sample:
            buffer = sample.get_buffer()
            caps = sample.get_caps()

            structure = caps.get_structure(0)
            width = structure.get_value("width")
            height = structure.get_value("height")
            format_ = structure.get_value("format")
            success, map_info = buffer.map(Gst.MapFlags.READ)

            if success:
                data = map_info.data
                try:
                    self.executor.submit(self.process_frame, data, width, height, format_)
                except RuntimeError as e:
                    logger.error(f"Failed to submit frame processing task: {e}")
                buffer.unmap(map_info)
        return Gst.FlowReturn.OK

    def process_frame(self, data, width, height, format_):
        current_time = time.time()
        if current_time - self.last_processed_time >= self.frame_interval:
            self.last_processed_time = current_time
        else:
            #print("----------------------------------------------------------------------------------------------------------------->",current_time - self.last_processed_time)
            del data
            return
        # if current_time - self.last_processed_time < 1:  # For 1 FPS
        #     return  # Skip processing this frame
        try:
            

            arr = np.frombuffer(data, dtype=np.uint8)

            logger.info(f"Array shape: {arr.shape}, expected size: {height * width * 3}")

            if arr.size != height * width * 3:
                raise ValueError("Invalid image data: size does not match expected dimensions")

            # Process frame for supported format (RGB)
            if format_ == "RGB":
                cv_image = arr.reshape((height, width, 3))
            else:
                logger.error(f"Unsupported format: {format_}")
                return

            self.camera.set_rgb_image(cv_image)

            # Perform inference on the frame
            for detection_model, network_inference in self.camera.get_inferenceMap().items():
                network_inference.process_image(cv_image, detection_model, self.camera)
                self.detection_map[detection_model] = self.camera.get_detections()

            self.rule_executor.execute_rules(self.camera, self.detection_map)
            self.detection_map.clear()

            del arr
            del cv_image
            #gc.collect()  # Explicitly trigger garbage collection

        except ValueError as ve:
            logger.error(f"ValueError: {ve}")
        except Exception as e:
            logger.error(f"Error processing frame: {e}")

    def isInferencesReceiving(self):
        return self.inferences_receiving

class GstRtsp(threading.Thread):
    def __init__(self, camera, memory_limit_mb=2400):
        threading.Thread.__init__(self)
        self.camera = camera
        self.is_running = True
        self.bEOS = False
        self.frame_count = 0
        self.videoAppSinkListener = None
        self.pipeline = None
        self.loop = None
        self.lock = threading.Lock()
        self.memory_limit_mb = memory_limit_mb
        self.timeout_id = None

    def run(self):
        logger.info(f"Starting GStreamer Camera Capture for {self.camera.getCameraId()}...")
        rtsp_url = self.camera.getRtspUrl()
        logger.info(f"Start GStreamer streaming: {self.camera.getCameraId()}, URL: {rtsp_url}")

        self.create_pipeline(rtsp_url)
        self.pipeline.set_state(Gst.State.PLAYING)

        self.loop = GLib.MainLoop()
        try:
            self.loop.run()
        except Exception as e:
            logger.error(f"Error running main loop for {self.camera.getCameraId()}: {e}")

    def create_pipeline(self, rtsp_url):
        pipeline_name = f"pipe_{self.camera.getCameraId()}"
        gst_command = self.get_gpu_pipeline(rtsp_url) if self.camera.isUseGpuDecoder() else self.get_cpu_pipeline(rtsp_url)

        if self.pipeline:
            self.pipeline.set_state(Gst.State.NULL)
            self.pipeline = None

        self.pipeline = Gst.parse_launch(gst_command)
        if not self.pipeline:
            logger.error(f"Failed to create the GStreamer pipeline for {self.camera.getCameraId()}.")
            return

        self.pipeline.set_name(pipeline_name)
        video_app_sink = self.pipeline.get_by_name("videoAppSink")

        if not video_app_sink:
            logger.error(f"Failed to get video app Sink for {self.camera.getCameraId()}.")
            self.pipeline.set_state(Gst.State.NULL)
            return

        video_app_sink.set_property("emit-signals", True)
        video_app_sink.set_property('sync', False)
        video_app_sink.set_property('max-buffers', 1)
        video_app_sink.set_property('drop', True)

        inference = self.camera.get_inference()
        self.videoAppSinkListener = RtspAppSinkListener(self.camera, inference, self)
        video_app_sink.connect("new-sample", self.videoAppSinkListener)

        bus = self.pipeline.get_bus()
        bus.add_signal_watch()
        bus.connect("message::eos", self.on_eos)
        bus.connect("message::error", self.on_error)
        bus.connect("message::warning", self.on_warning)

    def on_eos(self, bus, message):
        logger.info(f"End of stream (EOS) received for {self.camera.getCameraId()}")
        self.bEOS = True
        self.pipeline.set_state(Gst.State.NULL)
        if self.loop:
            self.loop.quit()

    def on_error(self, bus, message):
        error, debug_info = message.parse_error()
        logger.error(f"Error from element {message.src.get_name()} for {self.camera.getCameraId()}: {error.message}, Debugging information: {debug_info}")
        self.bEOS = True
        self.pipeline.set_state(Gst.State.NULL)
        if self.loop:
            self.loop.quit()

    def on_warning(self, bus, message):
        warning, debug_info = message.parse_warning()
        logger.warning(f"Warning from element {message.src.get_name()} for {self.camera.getCameraId()}: {warning.message}, Debugging information: {debug_info}")

    def get_cpu_pipeline1(self, rtsp_url):
        pipeline = (f'rtspsrc protocols=GST_RTSP_LOWER_TRANS_TCP name={self.camera.getCameraId()} location="{rtsp_url}" ! decodebin ! videoconvert ! video/x-raw,format={self.camera.get_formats()},width={self.camera.get_width()},height={self.camera.get_height()} ! appsink name=videoAppSink')
        return pipeline

    def get_cpu_pipeline(self, rtsp_url):
        #ipeline = (f'rtspsrc location="{rtsp_url}" ! rtp{self.camera.get_encode_mode()}depay ! {self.camera.get_encode_mode()}parse ! avdec_{self.camera.get_encode_mode()} ! videoconvert ! video/x-raw,format={self.camera.get_formats()},width={self.camera.get_width()},height={self.camera.get_height()} ! appsink name=videoAppSink')
        pipeline = (f'rtspsrc location="{rtsp_url}" ! rtp{self.camera.get_encode_mode()}depay ! {self.camera.get_encode_mode()}parse ! avdec_{self.camera.get_encode_mode()} ! videoconvert ! video/x-raw,format={self.camera.get_formats()} ! appsink name=videoAppSink')
        # substream
        #pipeline = (f'rtspsrc location="{rtsp_url}" ! rtp{self.camera.get_encode_mode()}depay ! {self.camera.get_encode_mode()}parse ! avdec_{self.camera.get_encode_mode()} ! videoconvert ! video/x-raw,format={self.camera.get_formats()} ! appsink name=videoAppSink')
        return pipeline


    def get_cpu_pipeline_i7(self, rtsp_url):
        return (
            f"rtspsrc protocols=GST_RTSP_LOWER_TRANS_TCP name={self.camera.getCameraId()} location={rtsp_url} ! "
            f"rtp{self.camera.get_encode_mode()}depay ! {self.camera.get_encode_mode()}parse ! avdec_{self.camera.get_encode_mode()} ! "
            f"videoconvert ! video/x-raw,width={self.camera.get_width()},height={self.camera.get_height()} ! "
            "appsink name=videoAppSink"
        )

    def get_gpu_pipeline(self, rtsp_url):
        return (
            f"rtspsrc protocols=GST_RTSP_LOWER_TRANS_TCP name={self.camera.getCameraId()} location={rtsp_url} ! "
            f"rtp{self.camera.get_encode_mode()}depay ! {self.camera.get_encode_mode()}parse ! nvv4l2decoder ! "
            f"nvvideoconvert ! video/x-raw,width={self.camera.get_width()},height={self.camera.get_height()},format={self.camera.get_formats()} ! "
            f"videoscale ! videoconvert ! video/x-raw,width={self.camera.get_width()},height={self.camera.get_height()} ! "
            "appsink name=videoAppSink"
        )
'''
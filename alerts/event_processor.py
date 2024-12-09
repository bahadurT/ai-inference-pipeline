"""
********************************************
*                                          *
*           Author: Bahadur Singh Thakur
*           E-mail: bahadur.th7@gmail.com  *
*           Date: 12-Dec-2024              *
*                                          *
********************************************
"""
import cv2
import time
from datetime import datetime
import json
import requests
import threading
import io

class EventProcessor:
    def __init__(self):
        """
        Initializes the EventProcessor class for handling event processing and uploading data.
        """
        pass

    def process_event(self, server_url, cv_image, camera_id, eventType, eventTag, sensorName, sensorId, serverPort, count, status):
        """
        Processes an event and sends the associated data and image to the specified server URL.

        :param server_url: URL to send the multipart data.
        :param cv_image: The OpenCV image to be uploaded.
        :param camera_id: ID of the camera.
        :param eventType: Type of the event.
        :param eventTag: Tag of the event.
        :param sensorName: Name of the sensor.
        :param sensorId: ID of the sensor.
        :param serverPort: Server port (typically not used in the payload but included for metadata).
        :param count: Count value associated with the event.
        :param status: Status metadata to include in the payload.
        """
        # Encode the image
        success, encoded_image = cv2.imencode('.jpg', cv_image)
        if not success:
            print("Image encoding failed.")
            return

        # Convert encoded image to bytes
        image_bytes = encoded_image.tobytes()

        # Get current time for event metadata
        current_time = time.time()
        event_time = int(current_time * 1000)  # Convert to milliseconds
        time_stamp_str = datetime.fromtimestamp(current_time).strftime('%d-%m-%Y-%H-%M-%S')

        # Create payload data
        payload = {
            "cameraId": camera_id,
            "eventTime": event_time,
            "timeStampStr": time_stamp_str,
            "eventType": eventType,
            "eventTag": eventTag,
            "sensorName": sensorName,
            "sensorId": sensorId,
            "serverPort": serverPort,
            "count": count,
            "extras": {"status": str(status)}
        }

        # JSON data for payload
        data = {'data': json.dumps(payload)}

        # Define the function to send the request
        def send_request(image_data, json_data, url):
            try:
                # Files dictionary with image
                with io.BytesIO(image_data) as image_file:
                    files = {'image': (camera_id+"_"+str(event_time)+'.jpg', image_file, 'image/jpeg')}

                    # Sending the POST request with image and JSON data
                    response = requests.post(url, data=json_data, files=files)
                    print(f"Response Code: {response.status_code}")
                    print(f"Response Content: {response.content.decode('utf-8')}")
            except Exception as e:
                print(f"An error occurred: {e}")

        # Create a non-daemon thread
        request_thread = threading.Thread(target=send_request, args=(image_bytes, data, server_url))
        request_thread.daemon = False  # Ensure thread lifecycle depends on the calling thread
        request_thread.start()

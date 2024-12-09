"""
********************************************
*                                          *
*           Author: Bahadur Singh Thakur
*           E-mail: bahadur.th7@gmail.com  *
*           Date: 12-Dec-2024              *
*                                          *
********************************************
"""
class Prediction:
    def __init__(self, label: str, top: int, left: int, width: int, height: int, score: float):
        self.label = label
        self.top = top
        self.left = left
        self.width = width
        self.height = height
        self.score = score

    def get_label(self) -> str:
        return self.label

    def set_label(self, label: str):
        self.label = label

    def get_top(self) -> int:
        return self.top

    def set_top(self, top: int):
        self.top = top

    def get_left(self) -> int:
        return self.left

    def set_left(self, left: int):
        self.left = left

    def get_width(self) -> int:
        return self.width

    def set_width(self, width: int):
        self.width = width

    def get_height(self) -> int:
        return self.height

    def set_height(self, height: int):
        self.height = height

    def get_score(self) -> float:
        return self.score

    def set_score(self, score: float):
        self.score = score

    def __str__(self) -> str:
        return f"Prediction [label={self.label}, top={self.top}, width={self.width}, left={self.left}, height={self.height}, score={self.score}]"

    def to_dict(self) -> dict:
        """Convert Prediction instance to a dictionary for easy serialization."""
        return {
            'label': self.label,
            'top': self.top,
            'left': self.left,
            'width': self.width,
            'height': self.height,
            'score': self.score
        }

    @classmethod
    def process_results(cls, results: str, labels: list) -> list:
        prediction_list = []
        values = results.split("#")
        values = values[:-1]
        
        # Debugging: Print the split values
        #print(f"Split values: {values}")
        
        for value in values:
            if not value:
                continue  # Skip empty entries
            
            detection_list = value.split(",")
            
            # Debugging: Check the parsed detection list
            #print(f"Detection list: {detection_list}")
            
            if len(detection_list) != 6:  # Ensure there are 6 elements
                print(f"Unexpected detection format: {detection_list}")
                continue
            
            try:
                label_index = int(detection_list[0])
                left = int(detection_list[1])
                top = int(detection_list[2])
                width = int(detection_list[3])
                height = int(detection_list[4])
                score = float(detection_list[5])
                
                # Ensure the label index is within bounds
                if label_index >= len(labels):
                    print(f"Invalid label index: {label_index}")
                    continue
                
                # Create the prediction object
                prediction = cls(
                    label=labels[label_index], 
                    top=int(top), 
                    left=int(left), 
                    width=int(width), 
                    height=int(height), 
                    score=score
                )
                prediction_list.append(prediction)
            
            except ValueError as e:
                print(f"Error parsing detection values: {e}")
                continue
        
        # Debugging: Check the final prediction list
        #print(f"Predictions: {prediction_list}")
        
        return prediction_list

'''class Prediction:
    def __init__(self, label: str, top: int, left: int, width: int, height: int, score: float):
        self.label = label
        self.top = top
        self.left = left
        self.width = width
        self.height = height
        self.score = score

    def get_label(self) -> str:
        return self.label

    def set_label(self, label: str):
        self.label = label

    def get_top(self) -> int:
        return self.top

    def set_top(self, top: int):
        self.top = top

    def get_left(self) -> int:
        return self.left

    def set_left(self, left: int):
        self.left = left

    def get_width(self) -> int:
        return self.width

    def set_width(self, width: int):
        self.width = width

    def get_height(self) -> int:
        return self.height

    def set_height(self, height: int):
        self.height = height

    def get_score(self) -> float:
        return self.score

    def set_score(self, score: float):
        self.score = score

    def __str__(self) -> str:
        return f"Prediction [label={self.label}, top={self.top}, width={self.width}, left={self.left}, height={self.height}, score={self.score}]"

    @classmethod
    def process_results(cls, results: str, labels: list) -> list:
        prediction_list = []
        values = results.split("#")
        values = values[:-1]
        
        # Debugging: Print the split values
        #print(f"Split values: {values}")
        
        for value in values:
            if not value:
                continue  # Skip empty entries
            
            detection_list = value.split(",")
            
            # Debugging: Check the parsed detection list
            #print(f"Detection list: {detection_list}")
            
            if len(detection_list) != 6:  # Ensure there are 6 elements
                print(f"Unexpected detection format: {detection_list}")
                continue
            
            try:
                label_index = int(detection_list[0])
                left = int(detection_list[1])
                top = int(detection_list[2])
                width = int(detection_list[3])
                height = int(detection_list[4])
                score = float(detection_list[5])
                
                # Ensure the label index is within bounds
                if label_index >= len(labels):
                    print(f"Invalid label index: {label_index}")
                    continue
                
                # Create the prediction object
                prediction = cls(
                    label=labels[label_index], 
                    top=int(top), 
                    left=int(left), 
                    width=int(width), 
                    height=int(height), 
                    score=score
                )
                prediction_list.append(prediction)
            
            except ValueError as e:
                print(f"Error parsing detection values: {e}")
                continue
        
        # Debugging: Check the final prediction list
        #print(f"Predictions: {prediction_list}")
        
        return prediction_list
'''
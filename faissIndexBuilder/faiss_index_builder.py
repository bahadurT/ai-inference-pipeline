"""
********************************************
*                                          *
*           Author: Bahadur Singh Thakur
*           E-mail: bahadur.th7@gmail.com  *
*           Date: 12-Oct-2024              *
*                                          *
********************************************
"""
import os
import json
import numpy as np
import faiss
import time

class FaissIndexBuilder:
    def __init__(self, fv_dir):
        self.fv_dir = fv_dir
        self.features = []
        self.names = []

    def load_feature_vectors(self):
        print(self.fv_dir, "------------------------------->")
        for filename in os.listdir(self.fv_dir):
            if filename.endswith('.txt'):
                with open(os.path.join(self.fv_dir, filename), 'r') as file:
                    data = file.read()
                try:
                    feature_list = json.loads(data)['featureList']
                    feature = np.array(feature_list, dtype=np.float32)

                    # Normalize the feature vector
                    feature = feature / np.linalg.norm(feature) if np.linalg.norm(feature) > 0 else feature

                    # Ensure feature has the expected shape
                    if feature.ndim == 2 and feature.shape[0] == 1:
                        feature = np.squeeze(feature, axis=0)
                    elif feature.ndim == 1:
                        pass
                    else:
                        raise ValueError("Unexpected feature dimensions")

                    self.features.append(feature)
                    name = json.loads(data)['name']
                    self.names.append(name)
                except (json.JSONDecodeError, KeyError, ValueError) as e:
                    print(f"Error reading file {filename}: {e}")

        self.features = np.array(self.features)
        self.features = self.features / np.linalg.norm(self.features, axis=1, keepdims=True) if np.linalg.norm(self.features, axis=1, keepdims=True).all() else self.features
        print(f'Loaded {self.features.shape[0]} feature vectors with shape {self.features.shape[1]}')
        print(f'Loaded {len(self.names)} names')

    def create_faiss_index(self, dimension):
        # Use IndexFlatIP for cosine similarity
        index = faiss.IndexFlatIP(dimension)

        print(f"Adding features to FAISS index with dimension {dimension}")
        index.add(self.features)
        
        return index

    def search_similar_vectors(self, query_filename, k=5):
        query_filepath = os.path.join(self.fv_dir, query_filename)
        with open(query_filepath, 'r') as file:
            data = file.read()
        try:
            query_data = json.loads(data)
            if 'featureList' not in query_data or 'name' not in query_data:
                raise ValueError("Query file does not contain 'featureList' or 'name'")

            query_feature = np.array(query_data['featureList'], dtype=np.float32)

            # Normalize the query feature
            query_feature = query_feature / np.linalg.norm(query_feature) if np.linalg.norm(query_feature) > 0 else query_feature

            # Ensure the query feature has the expected shape
            if query_feature.ndim == 1:
                query_feature = np.expand_dims(query_feature, axis=0)
            elif query_feature.ndim == 2 and query_feature.shape[0] == 1:
                query_feature = np.squeeze(query_feature, axis=0)
            else:
                raise ValueError(f"Unexpected shape for query feature: {query_feature.shape}")

            # Print the dimensions of query feature for debugging
            print(f"Query feature shape: {query_feature.shape}")

            # Create the FAISS index
            index = self.create_faiss_index(query_feature.shape[1])

            t1 = time.time()
            D, I = index.search(query_feature, k=k)
            t2 = time.time()
            time_taken = (t2 - t1)
            print(f"Time taken: {time_taken}")

            print('Similar vectors:')
            for i in range(len(I[0])):
                print(f'- {self.names[I[0][i]]} (distance: {D[0][i]:.5f})')

        except (json.JSONDecodeError, KeyError, ValueError) as e:
            print(f"Error reading query file {query_filename}: {e}")

if __name__ == "__main__":
    fv_dir = '/home/ivis/analytics/ivis-arcface-frs/face_db_fv/'
    faiss_builder = FaissIndexBuilder(fv_dir)
    faiss_builder.load_feature_vectors()
    query_file = 'bahadur.txt'  # Update with your query file
    faiss_builder.search_similar_vectors(query_file)


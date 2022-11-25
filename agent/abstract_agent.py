import os
from abc import ABC, abstractmethod

import numpy as np

CSV_FOLDER_PATH = "<local-path-to-collected-fingerprints-folders>"
RPI_MODEL_PREFIX = "mod4-"


class AbstractAgent(ABC):
    @staticmethod
    def standardize_inputs(inputs):
        csv_normal = np.loadtxt(fname=os.path.join(CSV_FOLDER_PATH, RPI_MODEL_PREFIX + "normal-behavior.csv"), delimiter=",", skiprows=1)
        norm_min = np.min(csv_normal, axis=0).reshape(-1, 1)
        norm_max = np.max(csv_normal, axis=0).reshape(-1, 1)
        # print("ABSAGENT: normal min/max", csv_normal.shape, norm_min.shape, norm_max.shape)
        # print("ABSAGENT: min/max min/max", norm_min, np.min(norm_min), np.max(norm_min), norm_max, np.min(norm_max), np.max(norm_max))

        std = (inputs - norm_min) / (norm_max - norm_min + 0.001)
        # print("ABSAGENT: input min/max", np.min(inputs), np.max(inputs))
        # print("ABSAGENT: std min/max", np.min(std), np.max(std))

        return std

    @abstractmethod
    def predict(self, fingerprint):
        pass

    @abstractmethod
    def update_weights(self, fingerprint, reward):
        pass

r"""This module provides package-wide configuration management."""
from typing import Any, List
import time
import os, sys
from yacs.config import CfgNode as CN

class Config(object):
    r"""
    A collection of all the required configuration parameters. This class is a nested dict-like
    structure, with nested keys accessible as attributes. It contains sensible default values for
    all the parameters, which may be overriden by (first) through a YAML file and (second) through
    a list of attributes and values.

    Extended Summary
    ----------------
    This class definition contains default values corresponding to ``joint_training`` phase, as it
    is the final training phase and uses almost all the configuration parameters. Modification of
    any parameter after instantiating this class is not possible, so you must override required
    parameter values in either through ``config_yaml`` file or ``config_override`` list.

    Parameters
    ----------
    config_yaml: str
        Path to a YAML file containing configuration parameters to override.
    config_override: List[Any], optional (default= [])
        A list of sequential attributes and values of parameters to override. This happens after
        overriding from YAML file.

    Examples
    --------
    Let a YAML file named "config.yaml" specify these parameters to override::

        ALPHA: 1000.0
        BETA: 0.5

    >>> _C = Config("config.yaml", ["OPTIM.BATCH_SIZE", 2048, "BETA", 0.7])
    >>> _C.ALPHA  # default: 100.0
    1000.0
    >>> _C.BATCH_SIZE  # default: 256
    2048
    >>> _C.BETA  # default: 0.1
    0.7
    """

    def __init__(self, config_yaml: str, config_override: List[Any] = []):
        self._C = CN()
        self._C.RANDOM_SEED = 0
        self._C.PHASE = "training"
        self._C.EXPERIMENT_NAME = "default"
        self._C.RESULTS_DIR = "results"
        self._C.OVERFIT= False
        self._C.Z= False

        self._C.SHAPENET_DATA = CN()
        self._C.SHAPENET_DATA.PATH = '/scratch/jiadeng_root/jiadeng/shared_data/datasets/ShapeNetCore.v1/'
        # self._C.SHAPENET_DATA.TRANSFORM = None
        

        #REMOVE OPTIM OR SOLVER
        self._C.SOLVER = CN()
        self._C.SOLVER.LR_SCHEDULER_NAME = "constant"  # {'constant', 'cosine'}
        self._C.SOLVER.BATCH_SIZE = 32
        self._C.SOLVER.BATCH_SIZE_EVAL = 8
        self._C.SOLVER.NUM_EPOCHS = 25
        self._C.SOLVER.BASE_LR = 0.0001
        self._C.SOLVER.OPTIMIZER = "adam"  # {'sgd', 'adam'}
        self._C.SOLVER.MOMENTUM = 0.9
        self._C.SOLVER.WARMUP_ITERS = 500
        self._C.SOLVER.WARMUP_FACTOR = 0.1
        self._C.SOLVER.CHECKPOINT_PERIOD = 24949  # in iters
        self._C.SOLVER.LOGGING_PERIOD = 50  # in iters
        # stable training
        self._C.SOLVER.SKIP_LOSS_THRESH = 50.0
        self._C.SOLVER.LOSS_SKIP_GAMMA = 0.9

        self._C.G = CN()
        self._C.G.BACKBONE = "resnet50"
 
        self._C.G.MESH_HEAD = CN()
        self._C.G.MESH_HEAD.NAME = "Pixel2MeshHead"
        self._C.G.MESH_HEAD.NUM_STAGES = 1
        self._C.G.MESH_HEAD.NUM_GRAPH_CONVS = 1
        self._C.G.MESH_HEAD.GRAPH_CONV_DIM = 256
        self._C.G.MESH_HEAD.GRAPH_CONV_INIT = "normal"
        self._C.G.MESH_HEAD.GT_NUM_SAMPLES = 5000
        self._C.G.MESH_HEAD.PRED_NUM_SAMPLES = 5000
        self._C.G.MESH_HEAD.CHAMFER_LOSS_WEIGHT = 1.0
        self._C.G.MESH_HEAD.NORMAL_LOSS_WEIGHT = 1.0
        self._C.G.MESH_HEAD.EDGE_LOSS_WEIGHT = 1.0
        self._C.G.MESH_HEAD.LAPLACIAN_LOSS_WEIGHT = 1.0
        self._C.G.MESH_HEAD.ICO_SPHERE_LEVEL = -1
        

        
        self._C.D = CN()
        self._C.D.INPUT_MESH_FEATS = 3
        self._C.D.HIDDEN_DIMS = [32, 64, 128]
        self._C.D.CLASSES = 57
        self._C.D.CONV_INIT = "normal"
        
        self._C.DATASETS = CN()
        self._C.DATASETS.NAME = "shapenet"
        self._C.DATASETS.SPLITS_FILE = "/scratch/jiadeng_root/jiadeng/shared_data/datasets/SICGAN_data/p2m_splits.json"
        self._C.DATASETS.DATA_DIR = "/scratch/jiadeng_root/jiadeng/shared_data/datasets/SICGAN_data/"
        
        self._C.merge_from_file(config_yaml)
        self._C.merge_from_list(config_override)
        
        self._C.CKP = CN()
        self._C.CKP.full_experiment_name = self._C.EXPERIMENT_NAME#("exp_%s_%s" % ( time.strftime("%m_%d_%H_%M_%S"), self._C.EXPERIMENT_NAME) )
        self._C.CKP.experiment_path = os.path.join(self._C.RESULTS_DIR, self._C.CKP.full_experiment_name)
        self._C.CKP.best_loss = sys.float_info.max

        # Make an instantiated object of this class immutable.
        #self._C.freeze()

    def dump(self, file_path: str):
        r"""Save config at the specified file path.

        Parameters
        ----------
        file_path: str
            (YAML) path to save config at.
        """
        self._C.dump(stream=open(file_path, "w"))

    def __getattr__(self, attr: str):
        return self._C.__getattr__(attr)

    def __str__(self):
        common_string: str = str(CN({"RANDOM_SEED": self._C.RANDOM_SEED})) + "\n"
        common_string += str(CN({"DATA": self._C.DATASETS})) + "\n"
        common_string += str(CN({"BASE_MODEL": self._C.G})) + "\n"
        common_string += str(CN({"SOLVER": self._C.SOLVER})) + "\n"
        common_string += str(CN({"CHECKPOINT": self._C.CKP})) + "\n"
        return common_string

    def __repr__(self):
        return self._C.__repr__()


import numpy as np
import tensorflow as tf
from loguru import logger
from typing import List, Callable, Tuple

def _bytes_feature(value):
    """
    Returns a bytes_list from a string / byte.
    SOURCE: https://www.tensorflow.org/tutorials/load_data/tfrecord
    """
    if isinstance(value, type(tf.constant(0))):
        value = value.numpy() # BytesList won't unpack a string from an EagerTensor.
    return tf.train.Feature(bytes_list=tf.train.BytesList(value=[value]))

def _float_feature(value):
    """
    Returns a float_list from a float / double.
    SOURCE: https://www.tensorflow.org/tutorials/load_data/tfrecord
    """
    return tf.train.Feature(float_list=tf.train.FloatList(value=[value]))

def _int64_feature(value):
    """
    Returns an int64_list from a bool / enum / int / uint.
    SOURCE: https://www.tensorflow.org/tutorials/load_data/tfrecord
    """
    return tf.train.Feature(int64_list=tf.train.Int64List(value=[value]))

def to_tfrecords(image_paths: List[str], 
                 mask_paths: List[str], 
                 img_read_func: Callable, 
                 tfrecords_filename: str) -> None:
    """
    REFERENCE SOURCE: https://www.kaggle.com/code/kawaitsoi/convert-images-and-masks-to-tfrecords-file - by      user kawaitsoi
    """
    # get a writer for the tfrecord file.
    with tf.io.TFRecordWriter(tfrecords_filename) as writer:
        # write data/masks into tfrecords
        for img_pth, mask_pth in zip(image_paths, mask_paths):
            img = np.array(img_read_func(img_pth))
            mask = np.array(img_read_func(mask_pth))
        
            height, width = img.shape[0], img.shape[1]
            img_raw, mask_raw = img.tostring(), mask.tostring()
            
            # save the heights and widths as well so, which 
            # are needed when decoding from tfrecords back to images
            example = tf.train.Example(features=tf.train.Features(feature={
                                                                  'height': _int64_feature(height),
                                                                  'width': _int64_feature(width),
                                                                  'image_raw': _bytes_feature(img_raw),
                                                                  'mask_raw': _bytes_feature(mask_raw)}
                                                                  ))
            writer.write(example.SerializeToString())

    logger.info(f'Wrote file to: {tfrecords_filename}')

def read_record(string_record: str) -> Tuple[np.ndarray, np.ndarray]:
    """
    """
    example = tf.train.Example()
    example.ParseFromString(string_record)
    
    height = int(example.features.feature['height'].int64_list.value[0])
    width = int(example.features.feature['width'].int64_list.value[0])
    
    img_string = (example.features.feature['image_raw'].bytes_list.value[0])
    mask_string = (example.features.feature['mask_raw'].bytes_list.value[0])
    
    img_1d = np.fromstring(img_string, dtype=np.uint8)
    mask_1d = np.fromstring(mask_string, dtype=np.uint8)
    
    #reshape back to their original shape from a 1D array read from tfrecords
    img = img_1d.reshape((height, width, -1))
    mask = mask_1d.reshape((height, width))
    
    return img, mask
from styx_msgs.msg import TrafficLight
impport tensorflow as tf
import cv2
import numpy as np
import rospy
import os


class TLClassifier(object):
    def __init__(self, config):
        self.threshold = config['CNN']['threshold']
        self.load_model(config['CNN']['model'])

        self.tf_lights = {
            1: TrafficLight.GREEN,
            2: TrafficLight.YELLOW,
            3: TrafficLight.RED
        }


    def load_model(self, model_path):
        base_folder = os.path.dirname(os.path.realpath(__file__))
        model_path = os.path.join(base_folder, model_path)

        rospy.loginfo('Loading model from %s', model_path)

        graph = tf.Graph()

        with graph.as_default():
            graph_def = tf.GraphDef()

            with tf.gfile.GFile(model_path, 'rb') as fid:
                serialized_graph = fid.read()
                graph_def.ParseFromString(serialized_graph)
                tf.import_graph_def(graph_def, name='')

        self.sess = tf.Session(graph=graph)

        self.image_tensor = graph.get_tensor_by_name('image_tensor:0')
        self.detection_boxes = graph.get_tensor_by_name('detection_boxes:0')
        self.detection_scores = graph.get_tensor_by_name('detection_scores:0')
        self.detection_classes = graph.get_tensor_by_name('detection_classes:0')
        self.num_detections = graph.get_tensor_by_name('num_detections:0')

        rospy.loginfo("Model loaded!")


    def get_classification(self, image):
        """Determines the color of the traffic light in the image

        Args:
            image (cv::Mat): image containing the traffic light

        Returns:
            int: ID of traffic light color (specified in styx_msgs/TrafficLight)

        """
        input_img = np.expand_dims(image, axis=0)

        options = [self.num_detections, self.detection_boxes, self.detection_scores, self.detection_classes]
        _, _, scores, classes = self.sess.run(options, feed_dict = {self.image_tensor : input_img})

        confidence = scores[0]
        class_id = classes[0].astype(np.uint8)

        if confidence[0] >= self.threshold:
            tl_color = self.tf_lights.get(class_id[0], TrafficLight.UNKNOWN)
        else:
            rospy.loginfo("Traffic light color not recognized!")
            tl_color = TrafficLight.UNKNOWN

        return tl_color

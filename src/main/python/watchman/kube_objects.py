from kubernetes import config, client, watch
import time
import json
import pickle
# import only system from os 
from os import system, name 


class KubeObjects:
    all_nodes = []
    all_pods  = []

    def __init__(self, config_file=None, file_store = '/tmp'):
        self._file_store = file_store
        self.config_file = config_file
        self.config = config.load_kube_config(config_file = self.config_file)
        self.kubectl = client.CoreV1Api()
        # self.refresh()

    def refresh(self, save = True, use_cache = False):
        if use_cache:
            with open(self._file_store + "/nodes.bin", 'rb') as f:
                self.all_nodes = pickle.load(f)
            with open(self._file_store + "/pods.bin", 'rb') as f:
                self.all_pods = pickle.load(f)
        else:
            self.all_nodes.clear()
            self.all_pods.clear()

            for node in self.kubectl.list_node().items:
                self.all_nodes.append(node)
                self.all_nodes.sort(key=lambda n: n.metadata.labels['nodegroup'])
            for pod in self.kubectl.list_pod_for_all_namespaces().items:
                self.all_pods.append(pod)

        if save and not use_cache:
            with open(self._file_store + "/nodes.bin", 'wb') as f:
                pickle.dump(self.all_nodes, f)
            with open(self._file_store + "/pods.bin", 'wb') as f:
                pickle.dump(self.all_pods, f)

    @staticmethod
    def name(kube_object):
        if kube_object is not None:
            return kube_object.metadata.name
        else:
            return 'NA'

    def pods_with_node(self, node):
        node_pods = []
        for pod in self.all_pods:
            if pod.spec.node_name == self.name(node):
                node_pods.append(pod)
        return node_pods
 
    def pod_node(self, pod):
        for node in self.all_nodes:
            if self.name(node) == pod.spec.node_name:
                return node

    @staticmethod
    def node_group(node):
        if node is None:
            return 'NA'

        return node.metadata.labels['nodegroup']
    
    @staticmethod
    def safe_value(k8s_object, expression):
        return 

    @staticmethod
    def label(k8s_object, key):
        if k8s_object is None or k8s_object.metadata is None or k8s_object.metadata.labels is None:
            return None

        if key in k8s_object.metadata.labels:
            return k8s_object.metadata.labels[key]
        else:
            return None
    
    def filter_pod(self, label_key, label_value):
        if label_key is None:
            return self.all_pods
        to_ret = []
        for pod in self.all_pods:
            if self.label(pod, label_key) == label_value :
                to_ret.append(pod)
        return to_ret                

    def pod_nodes(self, label_key = None, label_value = None):
        pod_nodes = []
        for pod in self.filter_pod(label_key, label_value):
            pod_node = self.pod_node(pod)
            pod_nodes.append({'namespace': pod.metadata.namespace, 
                                'pod_name': self.name(pod), 
                                'pod_state':  pod.status.phase,
                                'app_name': self.label(pod, 'app'),
                                'node_name': self.name(pod_node), 
                                'node_group' : self.node_group(pod_node), 
                                'node_lifecycle': self.label(pod_node, 'lifecycle')})
        return pod_nodes
        

    def node_pods(self):
        to_ret = []
        for node in self.all_nodes:
            print(f"{self.name(node)} \t {node.metadata.labels['nodegroup']}")
            node_pods = self.pods_with_node(node)
            for pod in node_pods: 
                to_ret.append({'node_name': self.name(node), 
                    'node_group': node.metadata.labels['nodegroup'], 
                    'pod_name': self.name(pod), 
                    'pod_status': pod.status.phase})
        return to_ret        

    @staticmethod
    def is_good_state(state):
        good_states = ['Running', 'Succeeded', 'Completed']
        if state in good_states:
            return True
        else:
            return False




def clear():
    # for windows 
    if name == 'nt': 
        _ = system('cls') 
  
    # for mac and linux(here, os.name is 'posix') 
    else: 
        _ = system('clear')     

# kube_objects = KubeObjects()
# kube_objects.refresh(use_cache=True)


# while True:
#     kube_objects.refresh(use_cache=False)
#     clear()

#     print("******************* Not Running Pods **************")
#     for i in kube_objects.pod_nodes():
#         if kube_objects.is_good_state(i['pod_state']) or 'overprovisioner-pause-pod' in i['pod_name']:
#             continue
#         else:
#             kube_objects.print_preety(i, 'pod_name', 'pod_state', 'node_group', 'node_lifecycle')
#     print("---------------------------------------------------")

#     print("******************* Not Running Overprivisioning Pods **************")
#     for i in kube_objects.pod_nodes(label_key='run', label_value='overprovisioner-pause-pod'):
#         if kube_objects.is_good_state(i['pod_state']):
#             continue
#         else:
#             kube_objects.print_preety(i, 'pod_name', 'pod_state', 'node_group', 'node_lifecycle')
#     print("---------------------------------------------------")

#     time.sleep(2)

# print("******************* OverProvisioner Pods **************")



# kube_objects.pods_with_node(kube_objects.all_nodes[0])

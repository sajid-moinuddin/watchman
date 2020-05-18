from nrql.api import NRQL
import os
import json

class NewrelicInsight: 
    nrql_api_key = ''
    nr_account_id = ''
    nrql = None

    def __init__(self, account_id, ap1_key):
        self.nr_account_id = account_id
        self.nrql_api_key = ap1_key
        self.nrql = NRQL()
        self.nrql.api_key = self.nrql_api_key
        self.nrql.account_id = self.nr_account_id

    def execute_ql(self, q):
        response = self.nrql.query(q)
        return response 

    def get_events(self, eventType, size = 10):
        ql = f"""Select * from  InfrastructureEvent 
            WHERE category = \'{eventType}\'  limit {size}
            """
        response = self.execute_ql(ql)
        return response['results'][0]['events']

    def get_events_not_normal(self, eventType, size = 10):
        ql = f"""Select * from  InfrastructureEvent 
            WHERE category = \'{eventType}\'  AND event.type != 'Normal' limit {size}
            """
        response = self.execute_ql(ql)
        return response['results'][0]['events']        



# {
#     "category": "kubernetes",
#     "clusterName": "platform-prod",
#     "entityGuid": "MjExNTExM3xJTkZSQXxOQXw1Njc0OTkzNDI3NDA1MTIwNjc1",
#     "entityId": "5674993427405120675",
#     "entityKey": "k8s:platform-prod:content:pod:content-ares-watchlist-api-f7f67ffcf-xmplp",
#     "entityName": "k8s:platform-prod:content:pod:content-ares-watchlist-api-f7f67ffcf-xmplp",
#     "event.count": 1.0,
#     "event.firstTimestamp": "2020-05-07T13:06:36Z",
#     "event.involvedObject.apiVersion": "v1",
#     "event.involvedObject.fieldPath": "spec.containers{ares-watchlist-api}",
#     "event.involvedObject.kind": "Pod",
#     "event.involvedObject.name": "content-ares-watchlist-api-f7f67ffcf-xmplp",
#     "event.involvedObject.namespace": "content",
#     "event.involvedObject.resourceVersion": "64881569",
#     "event.involvedObject.uid": "71a688c9-8f5a-11ea-a3c6-0a838e5c56b8",
#     "event.lastTimestamp": "2020-05-07T13:06:36Z",
#     "event.message": "Liveness probe failed: Get http://10.100.125.128:8080/actuator/health: net/http: request canceled (Client.Timeout exceeded while awaiting headers)",
#     "event.metadata.creationTimestamp": "2020-05-07T13:06:36Z",
#     "event.metadata.name": "content-ares-watchlist-api-f7f67ffcf-xmplp.160cc0d6ae1daa93",
#     "event.metadata.namespace": "content",
#     "event.metadata.resourceVersion": "66148631",
#     "event.metadata.selfLink": "/api/v1/namespaces/content/events/content-ares-watchlist-api-f7f67ffcf-xmplp.160cc0d6ae1daa93",
#     "event.metadata.uid": "953f1b81-9063-11ea-b87d-029b5b996164",
#     "event.reason": "Unhealthy",
#     "event.source.component": "kubelet",
#     "event.source.host": "ip-10-100-113-182.ap-southeast-2.compute.internal",
#     "event.type": "Warning",
#     "eventRouterVersion": "0.0.1",
#     "externalKey": "k8s:platform-prod:content:pod:content-ares-watchlist-api-f7f67ffcf-xmplp",
#     "old_event.count": 1.0,
#     "old_event.firstTimestamp": "2020-05-07T13:06:36Z",
#     "old_event.involvedObject.apiVersion": "v1",
#     "old_event.involvedObject.fieldPath": "spec.containers{ares-watchlist-api}",
#     "old_event.involvedObject.kind": "Pod",
#     "old_event.involvedObject.name": "content-ares-watchlist-api-f7f67ffcf-xmplp",
#     "old_event.involvedObject.namespace": "content",
#     "old_event.involvedObject.resourceVersion": "64881569",
#     "old_event.involvedObject.uid": "71a688c9-8f5a-11ea-a3c6-0a838e5c56b8",
#     "old_event.lastTimestamp": "2020-05-07T13:06:36Z",
#     "old_event.message": "Liveness probe failed: Get http://10.100.125.128:8080/actuator/health: net/http: request canceled (Client.Timeout exceeded while awaiting headers)",
#     "old_event.metadata.creationTimestamp": "2020-05-07T13:06:36Z",
#     "old_event.metadata.name": "content-ares-watchlist-api-f7f67ffcf-xmplp.160cc0d6ae1daa93",
#     "old_event.metadata.namespace": "content",
#     "old_event.metadata.resourceVersion": "66148631",
#     "old_event.metadata.selfLink": "/api/v1/namespaces/content/events/content-ares-watchlist-api-f7f67ffcf-xmplp.160cc0d6ae1daa93",
#     "old_event.metadata.uid": "953f1b81-9063-11ea-b87d-029b5b996164",
#     "old_event.reason": "Unhealthy",
#     "old_event.source.component": "kubelet",
#     "old_event.source.host": "ip-10-100-113-182.ap-southeast-2.compute.internal",
#     "old_event.type": "Warning",
#     "summary": "Liveness probe failed: Get http://10.100.125.128:8080/actuator/health: net/http: request canceled (Client.Timeout exceeded while awaiting headers)",
#     "timestamp": 1588858031000,
#     "verb": "UPDATE"
# }
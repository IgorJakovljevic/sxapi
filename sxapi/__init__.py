#!/usr/bin/python
# coding: utf8

__version__ = '0.9'


import time
import logging
import requests

from .low import LowLevelPublicAPI, LowLevelInternAPI
from .models import User, Animal, Organisation, Annotation
from .helper import fromTS, toTS

class API(object):
    def __init__(self, email=None, password=None, api_key=None, endpoint=None):
        """Initialize a new API client instance.
        """
        self.low = LowLevelPublicAPI(email=email, password=password, api_key=api_key, endpoint=endpoint)

    @property
    def status(self):
        return self.low.get_status()

    def print_stats(self):
        for p in self.low.stats():
            print(p)

    @property
    def user(self):
        return User(api=self.low, data=self.low.get_user())

    @property
    def organisations(self):
        return [Organisation.create_from_data(api=self.low, data=x, _id=x["organisation_id"])
            for x in self.low.get_organisations()]

    def get_annotation(self, annotation_id):
        return Annotation(api=self.low, _id=annotation_id)

    def get_animal(self, animal_id):
        return Animal(api=self.low, _id=animal_id)

    def get_organisation(self, organisation_id):
        return Organisation(api=self.low, _id=organisation_id)


class LowLevelAPI(object):
    def __init__(self, email=None, password=None, private_endpoint=None, api_key=None, public_endpoint=None):
        """Initialize a new API client instance.
        """
        self.publiclow = LowLevelPublicAPI(email=email, password=password, api_key=api_key, endpoint=public_endpoint)
        if private_endpoint is not None and api_key is not None:
            self.privatelow = LowLevelInternAPI(endpoint=private_endpoint, api_key=api_key)
        else:
            pass
            # self.privatelow = self._privatelow
            # do something to raise warning

    @property
    def _privatelow(self):
        raise RuntimeError("internal API not accessable without endpoint and token")

    # Status Calls

    def get_public_status(self):
        return self.publiclow.get_status()

    def get_private_status(self):
        return self.privatelow.get_status()

    # Calls to Public API

    def get_organisation_animal_ids(self, organisation_id):
        return self.publiclow.get_organisation_animal_ids(organisation_id)

    def get_animal_by_id(self, animal_id):
        return self.publiclow.get_animal_by_id(animal_id)

    def get_device_by_id(self, device_id):
        return self.publiclow.get_device_by_id(device_id)

    def get_organisation_by_id(self, organisation_id):
        return self.publiclow.get_organisation_by_id(organisation_id)

    def get_device_sensordata(self, device_id, metric, from_date, to_date):
        f = toTS(from_date)
        t = toTS(to_date)
        return self.publiclow.get_device_sensordata(device_id, metric, f, t)

    def get_animal_sensordata(self, animal_id, metric, from_date, to_date):
        f = toTS(from_date)
        t = toTS(to_date)
        return self.publiclow.get_animal_sensordata(animal_id, metric, f, t)

    def get_animal_events(self, animal_id, from_date=None, to_date=None):
        f = None
        if from_date is not None:
            f = toTS(from_date)
        t = None
        if to_date is not None:
            t = toTS(to_date)
        return self.publiclow.get_animal_events(animal_id, f, t)

    def get_device_events(self, device_id, from_date=None, to_date=None):
        f = None
        if from_date is not None:
            f = toTS(from_date)
        t = None
        if to_date is not None:
            t = toTS(to_date)
        return self.publiclow.get_device_events(device_id, f, t)

    # Deprecated Calls to Public (old name)

    def getAnimalIdsForOrganisation(self, organisation_id):
        raise DeprecationWarning("use get_organisation_animal_ids")

    def getAnimalsForOrganisation(self, organisation_id):
        raise DeprecationWarning("use get_animal_by_id")

    def getDeviceEventList(self, device_id, from_date, to_date):
        raise DeprecationWarning("use get_device_events")

    def getAnimalEventList(self, animal_id, from_date, to_date):
        raise DeprecationWarning("use get_animal_events")

    # Old internal calls

    def updateSensorData(self, device_id, metric, data):
        return self.privatelow.updateSensorData(device_id, metric, data)

    def updateSensorDataBulk(self, sensordata):
        return self.privatelow.updateSensorDataBulk(sensordata)

    def insertSensorData(self, device_id, metric, data):
        return self.privatelow.insertSensorData(device_id, metric, data)

    def insertSensorDataBulk(self, sensordata):
        return self.privatelow.insertSensorDataBulk(sensordata)

    def getSensorData(self, device_id, metric, from_date, to_date):
        return self.privatelow.getSensorData(device_id, metric, from_date, to_date)

    def getSensorDataRange(self, device_id, metric):
        return self.privatelow.getSensorDataRange(device_id, metric)

    def getSensorDataBulk(self, device_id, metrics, from_date, to_date):
        return self.privatelow.getSensorDataBulk(device_id, metrics, from_date, to_date)

    def getLastSensorData(self, device_id, metric):
        return self.privatelow.getLastSensorData(device_id, metric)

    def getLastSensorDataBulk(self, device_id, metrics):
        return self.privatelow.getLastSensorDataBulk(device_id, metrics)

    def insertEvent(self, device_id, event_type, timestamp, value,
                    metadata, level=10, disable_notifications=False):
        return self.privatelow.insertEvent(device_id, event_type, timestamp, value,
                                           metadata, level=level,
                                           disable_notifications=disable_notifications)

    def updateEventMeta(self, device_id, _id, event_meta):
        return self.privatelow.updateEventMeta(device_id, _id, event_meta)

    def getLastEventTimestamps(self, device_id):
        return self.privatelow.getLastEventTimestamps(device_id)

    def setDeviceMeta(self, device_id, metadata):
        return self.privatelow.setDeviceMeta(device_id, metadata)

    def getSensorInfo(self, device_id):
        return self.privatelow.getSensorInfo(device_id)

    def deleteEvent(self, event_id):
        return self.privatelow.deleteEvent(event_id)

    def getDevice(self, device_id, with_animal=True, with_organisation=True,
                  with_allmeta=True):
        return self.privatelow.getDevice(device_id, with_animal=with_animal,
                                         with_organisation=with_organisation,
                                         with_allmeta=with_allmeta)

    def getOrganisation(self, organisation_id):
        return self.privatelow.getOrganisation(organisation_id)

    def getAnimal(self, animal_id):
        return self.privatelow.getAnimal(animal_id)

    def getOrganisationList(self):
        return self.privatelow.getOrganisationList()

    # Annotation Calls

    def get_annotation_by_id(self, annotation_id):
        return self.publiclow.get_annotation_by_id(annotation_id)

    def get_annotation_definitions(self):
        return self.publiclow.get_annotation_definition()

    def get_annotations_by_class(self, annotation_class, from_date, to_date):
        return self.publiclow.get_annotations_by_class(annotation_class, from_date, to_date)

    def get_annotations_by_organisation(self, organisation_id, from_date, to_date):
        return self.publiclow.get_annotations_by_organisation(organisation_id, from_date, to_date)

    def get_animal_annotations(self, animal_id, from_date, to_date):
        return self.publiclow.get_animal_annotations(animal_id, from_date, to_date)

    def insert_animal_annotation(self, animal_id, ts, end_ts, classes, attributes):
        return self.publiclow.insert_animal_annotation(animal_id=animal_id, ts=ts,
                                                       end_ts=end_ts, classes=classes, attributes=attributes)

    def update_annotation(self, annotation_id, ts=None, end_ts=None, classes=None, attributes=None):
        return self.publiclow.update_annotation(annotation_id, ts, end_ts, classes, attributes)

    def insert_testset(self, name, meta_data, annotation_ids):
        return self.publiclow.insert_testset(name, meta_data, annotation_ids)

    def update_testset(self, testset_id, annotation_ids):
        return self.publiclow.update_testset(testset_id, annotation_ids)

    def get_testset_by_id(self, testset_id):
        return self.publiclow.get_testset_by_id(testset_id)

    def get_testset_by_name(self, name):
        return self.publiclow.get_testset_by_name(name)

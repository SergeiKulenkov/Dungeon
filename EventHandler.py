import pygame
from typing import Any
from typing import List

class EventHandler:
    def __init__(self):
        self._subscribers = {}

    def dispatchEvents(self, events: List[pygame.event.Event]):
        for event in events:
            subscribed = self._getSubscribers(event.type)
            for subscriber in subscribed:
                if callable(subscriber):
                    subscriber(*event.dict.values())

    def _getSubscribers(self, eventType: pygame.event.EventType):
        subscribers = self._subscribers.get(eventType)
        return subscribers if subscribers else []

    def subscribe(self, eventType: pygame.event.EventType, subscriber: Any):
        subscribers = self._subscribers.get(eventType)
        if subscribers:
            subscribers.append(subscriber)
        else:
            self._subscribers.update({eventType : [subscriber]})

    def unsubscribe(self, eventType: pygame.event.EventType, subscriber: Any):
        subscribers = self._getSubscribers(eventType)
        if subscribers:
            subscribers.remove(subscriber)
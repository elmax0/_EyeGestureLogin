class EventManager:
    def __init__(self):
        self._events = []

    def clear(self):
        self._events = []

    def get_events(self):
        return [event.to_row() for event in self._events]
        # return self._events

    def add_event(self, event):
        self._events.append(event)

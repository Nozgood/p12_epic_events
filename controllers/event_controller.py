class EventController:
    def __init__(self, session, view, collaborator=None):
        self.session = session
        self.view = view
        self.collaborator = collaborator

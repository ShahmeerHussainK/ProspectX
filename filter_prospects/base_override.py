
from django.db import models
from django_elasticsearch_dsl.signals import BaseSignalProcessor


class RealTimeSignalProcessorCustom(BaseSignalProcessor):
    """Real-time signal processor.

    Allows for observing when saves/deletes fire and automatically updates the
    search engine appropriately.
    """

    def setup(self):
        # Listen to all model saves.
        # models.signals.post_save.connect(self.handle_save)
        # models.signals.post_delete.connect(self.handle_delete)

        # Use to manage related objects update
        # models.signals.m2m_changed.connect(self.handle_m2m_changed)
        # models.signals.pre_delete.connect(self.handle_pre_delete)
        pass

    def teardown(self):
        # Listen to all model saves.
        # models.signals.post_save.disconnect(self.handle_save)
        # models.signals.post_delete.disconnect(self.handle_delete)
        # models.signals.m2m_changed.disconnect(self.handle_m2m_changed)
        # models.signals.pre_delete.disconnect(self.handle_pre_delete)
        pass
from modeltranslation.translator import translator, TranslationOptions
from travels import models

class CastTranslationOptions(TranslationOptions):
    fields = ('title', 'description')

class ItineraryTranslationOptions(TranslationOptions):
    fields = ('title', 'description')

class EventTranslationOptions(TranslationOptions):
    fields = ('title', 'description')

class SettingsTranslationOptions(TranslationOptions):
    fields = ('project_title', 'project_description', 'window_title')

translator.register(models.Cast, CastTranslationOptions)
translator.register(models.Itinerary, ItineraryTranslationOptions)
translator.register(models.Event, EventTranslationOptions)
translator.register(models.Settings, SettingsTranslationOptions)

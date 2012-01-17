from django.db.models import signals
from django.dispatch import receiver

from locast.api import cache

import models

GEOFEATURES_CACHE_GROUP = 'geofeatures'

@receiver(signals.post_save, sender=models.Itinerary)
@receiver(signals.post_delete, sender=models.Itinerary)
@receiver(signals.post_save, sender=models.Cast)
@receiver(signals.post_delete, sender=models.Cast)
def clear_geofeatures_cache(sender, **kwargs):
    cache.incr_group(GEOFEATURES_CACHE_GROUP)


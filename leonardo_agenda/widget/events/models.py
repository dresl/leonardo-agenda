
from django.db import models
from django.utils.translation import ugettext_lazy as _
from leonardo.module.web.models import ListWidget
import datetime
from elephantagenda.models import Category, Event, Venue


class EventsWidget(ListWidget):

    number = models.IntegerField(default=10)
    filter = models.CharField(max_length=1, choices=(
        ('a', _('all')),
        ('u', _('upcoming')),
        ('p', _('past')),
    ))
    category = models.ForeignKey(Category, null=True, blank=True,
                                 help_text=_('Leave blank for all categories.'))

    venue = models.ForeignKey(Venue, null=True, blank=True,
                              help_text=_('Leave blank for all venues.'))

    def get_items(self):

        if self.filter == 'u':
            events = Event.objects.filter(
                end_time__gte=datetime.datetime.now).order_by('start_time')
        elif self.filter == 'p':
            events = Event.objects.filter(
                end_time__lte=datetime.datetime.now).order_by('start_time')
        else:
            events = Event.objects.all().order_by('start_time')

        if hasattr(self.parent, 'language'):
            events = events.filter(language=self.parent.language)

        if self.category:
            events = events.filter(categories=self.category)

        if self.venue:
            events = events.filter(venue=self.category)

        return events[:self.number]

    class Meta:
        abstract = True
        verbose_name = _('event list')
        verbose_name_plural = _('event lists')

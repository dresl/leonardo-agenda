# coding=utf-8

from django.db import models
from django.utils.translation import ugettext_lazy as _
from leonardo.module.web.models import ListWidget
import datetime, calendar
from elephantagenda.models import Category, Event, Venue
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


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


    def get_all_calendar_items(self, request):
        def change_month(sourcedate, months):
            month = sourcedate.month - 1 + months
            year = int(sourcedate.year + month / 12)
            month = month % 12 + 1
            day = min(sourcedate.day, calendar.monthrange(year, month)[1])
            return datetime.date(year, month, day)

        today = datetime.date.today()
        get_categories = Category.objects.filter(name__startswith="Pro")
        start_date = change_month(today, -4)
        end_date = change_month(today, 5)
        events = Event.objects.filter(
            show_in_calendar=True,
            categories=get_categories).order_by('-start_time')
        events = events.exclude(start_time__range=(start_date, end_date))
        return events

    def get_calendar_items_on_load(self, request):
        def change_month(sourcedate, months):
            month = sourcedate.month - 1 + months
            year = int(sourcedate.year + month / 12)
            month = month % 12 + 1
            day = min(sourcedate.day, calendar.monthrange(year, month)[1])
            return datetime.date(year, month, day)

        today = datetime.date.today()
        get_categories = Category.objects.filter(name__startswith="Pro")
        start_date = change_month(today,-4)
        end_date = change_month(today, 5)
        events = Event.objects.filter(
            show_in_calendar=True,
            start_time__range=(start_date, end_date),
            categories=get_categories).order_by('-start_time')
        return events

    def get_semester_events(self, request):
        get_categories = Category.objects.filter(name="NUVČ")
        events = Event.objects.filter(
            categories=get_categories).order_by('start_time')
        return events

    def get_semester_names(self, request):
        get_semester_categories = Category.objects.filter(
            name__contains=". semestr")
        return get_semester_categories

    def get_items(self, request):
        if self.filter == 'u':
            if self.category:
                queryset = Event.objects.filter(
                    categories=self.category,
                    end_time__gte=datetime.datetime.now).order_by('start_time')
            else:
                queryset = Event.objects.filter(
                    end_time__gte=datetime.datetime.now).order_by('start_time')

            paginator = Paginator(queryset, self.objects_per_page)

            page = request.GET.get('page', None)

            try:
                events = paginator.page(page)
            except PageNotAnInteger:

                if page == "all":
                    events = queryset
                else:
                    events = paginator.page(1)

            except EmptyPage:
                events = paginator.page(paginator.num_pages)

            return events

        elif self.filter == 'p':
            if self.category:
                queryset = Event.objects.filter(
                    categories=self.category,
                    end_time__lte=datetime.datetime.now).order_by('-start_time')
            else:
                queryset = Event.objects.filter(
                    end_time__lte=datetime.datetime.now).order_by('-start_time')
            paginator = Paginator(queryset, self.objects_per_page)

            page = request.GET.get('page', None)

            try:
                events = paginator.page(page)
            except PageNotAnInteger:

                if page == "all":
                    events = queryset
                else:
                    events = paginator.page(1)

            except EmptyPage:
                events = paginator.page(paginator.num_pages)

            return events
        else:
            if self.category:
                queryset = Event.objects.filter(
                    categories=self.category).order_by('-start_time')
            else:
                queryset = Event.objects.all().order_by('-start_time')

            paginator = Paginator(queryset, self.objects_per_page)

            page = request.GET.get('page', None)

            try:
                events = paginator.page(page)
            except PageNotAnInteger:

                if page == "all":
                    events = queryset
                else:
                    events = paginator.page(1)

            except EmptyPage:
                events = paginator.page(paginator.num_pages)

            return events

        if hasattr(self.parent, 'language'):
            events = events.filter(language=self.parent.language)

        if self.venue:
            events = events.filter(venue=self.category)

        return events

    def get_events_actions(self, request):
        if self.filter == 'u':
            if self.category:
                queryset = Event.objects.filter(
                    categories=self.category,
                    upcoming_events=True,
                    end_time__gte=datetime.datetime.now).order_by('start_time')
            else:
                queryset = Event.objects.filter(
                    upcoming_events=True,
                    end_time__gte=datetime.datetime.now).order_by('start_time')

            paginator = Paginator(queryset, self.objects_per_page)

            page = request.GET.get('page', None)

            try:
                events = paginator.page(page)
            except PageNotAnInteger:

                if page == "all":
                    events = queryset
                else:
                    events = paginator.page(1)

            except EmptyPage:
                events = paginator.page(paginator.num_pages)

            return events

        elif self.filter == 'p':
            if self.category:
                queryset = Event.objects.filter(
                    categories=self.category,
                    upcoming_events=True,
                    end_time__lte=datetime.datetime.now).order_by('-start_time')
            else:
                queryset = Event.objects.filter(
                    upcoming_events=True,
                    end_time__lte=datetime.datetime.now).order_by('-start_time')
            paginator = Paginator(queryset, self.objects_per_page)

            page = request.GET.get('page', None)

            try:
                events = paginator.page(page)
            except PageNotAnInteger:

                if page == "all":
                    events = queryset
                else:
                    events = paginator.page(1)

            except EmptyPage:
                events = paginator.page(paginator.num_pages)

            return events
        else:
            if self.category:
                queryset = Event.objects.filter(
                    upcoming_events=True,
                    categories=self.category).order_by('-start_time')
            else:
                queryset = Event.objects.filter(
                    upcoming_events=True).order_by('-start_time')

            paginator = Paginator(queryset, self.objects_per_page)

            page = request.GET.get('page', None)

            try:
                events = paginator.page(page)
            except PageNotAnInteger:

                if page == "all":
                    events = queryset
                else:
                    events = paginator.page(1)

            except EmptyPage:
                events = paginator.page(paginator.num_pages)

            return events

    def get_template_data(self, request, *args, **kwargs):

        data = {}

        data['get_items'] = self.get_items(request)
        data['get_all_calendar_items'] = self.get_all_calendar_items(request)
        data['get_events_actions'] = self.get_events_actions(request)
        data['get_semester_events'] = self.get_semester_events(request)
        data['get_semester_names'] = self.get_semester_names(request)
        data['get_calendar_items_on_load'] = self.get_calendar_items_on_load(request)

        return data

    class Meta:
        abstract = True
        verbose_name = _('event list')
        verbose_name_plural = _('event lists')

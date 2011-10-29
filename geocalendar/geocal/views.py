import calendar
import datetime
from django.shortcuts import render_to_response, get_object_or_404
from django.template.context import RequestContext
from geocal.forms import EntryKeywordVerify
from geocal.models import CalendarEntry

def list_events_year_and_month_links(request):
    today = datetime.datetime.today()
    events = list(CalendarEntry.objects.filter(entry_date__year=today.year)) # this query can be optimized somehow

    months_with_events = []

    for event in events:
        if event.entry_date.month not in months_with_events:
            months_with_events.append(event.entry_date)

    if len(months_with_events) == 1:
        return events_month(request, months_with_events[0].year, months_with_events[0].month)

    return render_to_response('geocal/index.html', {'events': months_with_events, 'today': today},
                              context_instance=RequestContext(request))


def events_month(request, year, month):
    events_from = datetime.datetime(int(year), int(month), 1)
    # the following three lines converts the weeks_in_month name to norwegian (e.g. January -> Januar)
    import locale

    locale.setlocale(locale.LC_TIME, 'nb_NO.UTF-8')
    month_name = events_from.strftime("%B")

    # https://docs.djangoproject.com/en/dev/topics/db/queries/#querysets-are-lazy)
    # force evaluation of the queryset here, to avoid a bunch of queries on further lookups on the set.
    events = list(CalendarEntry.objects.filter(entry_date__year=year, entry_date__month=month))

    calendar.setfirstweekday(calendar.MONDAY)

    weeks_in_month = []
    for weekdays in calendar.monthcalendar(events_from.year, events_from.month):
        week = []
        for weekday in weekdays:
            events_found = []
            for event in events:
                if event.entry_date.day == weekday:
                    events_found.append(event)
            week.append((weekday, events_found))
        weeks_in_month.append(week)

    events_to_context = {
        'weeks_in_month': weeks_in_month,
        'month_name': month_name,
        'year': year,
        'month': month,
        }

    return render_to_response('geocal/events_month.html', events_to_context, context_instance=RequestContext(request))


def events_day(request, year, month, day):
    print year, month, day
    events = list(CalendarEntry.objects.filter(entry_date__year=year, entry_date__month=month, entry_date__day=day))

    if (len(events) > 1):
        return details_with_many_entries(request, events)
    elif (len(events) == 1):
        return details(request, events[0])
    else:
        return list_events_year_and_month_links(request)


def details_with_many_entries(request, entries):
    return render_to_response('geocal/events_day_multiple.html', {'events': entries},
                              context_instance=RequestContext(request))


def details(request, entry):
    form = EntryKeywordVerify()

    return render_to_response('geocal/events_day.html', {'form': form, 'event': entry},
                              context_instance=RequestContext(request))


def verify_entry(request, entry):
    should_redirect = False
    entry = None

    entry = get_object_or_404(CalendarEntry, args=[entry.pk])


def about(request):
    return render_to_response('geocal/about.html', {}, context_instance=RequestContext(request))
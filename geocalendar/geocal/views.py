import calendar
from datetime import date, datetime, timedelta
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.shortcuts import render_to_response, get_object_or_404
from django.template.context import RequestContext
from django.utils.translation import ugettext as _
from geocal.forms import EntryKeywordVerify
from geocal.models import CalendarEntry

def list_events_year_and_month_links(request):
    today = datetime.today()
    events = list(CalendarEntry.objects.filter(entry_date__year=today.year)) # this query can be optimized somehow

    MAX_YEARS_BACK = 5
    counter = 1;
    while len(events) == 0 and counter <= MAX_YEARS_BACK:
        today = datetime.today() - timedelta(days=365.2425*counter)
        events = list(CalendarEntry.objects.filter(entry_date__year=today.year)) # this query can be optimized somehow

    months_with_events = []

    for event in events:
        if event.entry_date.month not in map(lambda x : x.month, months_with_events):
            months_with_events.append(event.entry_date)

    if len(months_with_events) == 1:
        return events_month(request, months_with_events[0].year, months_with_events[0].month)

    return render_to_response('geocal/index.html', {'events': months_with_events, 'today': today},
                              context_instance=RequestContext(request))


def events_month(request, year, month):
    events_from = datetime(int(year), int(month), 1)
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
    events = list(CalendarEntry.objects.filter(entry_date__year=year, entry_date__month=month, entry_date__day=day))

    if (len(events) > 1):
        return details_with_many_entries(request, events)
    elif (len(events) == 1):
        return verify_entry(request, events[0].pk)
    else:
        return list_events_year_and_month_links(request)


def details_with_many_entries(request, entries):
    return render_to_response('geocal/events_day_multiple.html', {'events': entries},
                              context_instance=RequestContext(request))


def details(request, entry):
    keys = request.session.get('keys')
    if keys:
        if int(entry) in keys.keys():
            event = get_object_or_404(CalendarEntry, pk=entry)
            if date.today() < event.entry_date:
                messages.error(request, _("This event is still locked, please wait for the day to come - no cheating"))
            elif event.keyword == keys[int(entry)]:
                return render_to_response('geocal/details.html', {'event': event},
                                          context_instance=RequestContext(request))

    return render_to_response('geocal/forbidden.html', {"entry_id": entry},
                              context_instance=RequestContext(request))


def enter_codeword_entry(request, entry):
    should_redirect = False
    event = get_object_or_404(CalendarEntry, pk=entry)

    keys = request.session.get('keys')
    
    if keys:
        if event.pk in keys.keys():
            return details(request, event.pk)

    form = EntryKeywordVerify()
    request.session.set_test_cookie()

    response_dict = {
        'form': form,
        'event': event,
        }

    if should_redirect:
        return HttpResponseRedirect(reverse(details, args=[event.pk]))
    else:
        return render_to_response('geocal/events_day.html', response_dict, context_instance=RequestContext(request))

def verify_entry(request, entry):
    should_redirect = False
    event = get_object_or_404(CalendarEntry, pk=entry)

    keys = request.session.get('keys')

    if keys:
        if event.pk in keys.keys():
            return details(request, event.pk)

    if event and request.method == 'POST':
        form = EntryKeywordVerify(request.POST)

        if form.is_valid():
            keyword = form.cleaned_data['keyword']

            if request.session.test_cookie_worked():
                # The test cookie worked, so delete it.
                request.session.delete_test_cookie()

                if date.today() < event.entry_date:
                    messages.error(request, _("This event is still locked, please wait for the day to come - no cheating"))
                elif not keyword:
                    messages.error(request, _("You need to submit a keyword to verify, try again"))
                elif event.keyword == keyword:
                    messages.success(request, _("You entered the correct keyword, here is your secret picture"))
                    should_redirect = True

                    if not keys:
                        keys = {}

                    if event.pk not in keys:
                        keys[event.pk] = keyword

                    request.session['keys'] = keys

                else:
                    messages.error(request, _("Wrong keyword for this secret, try again"))
            else:
                messages.error(request, _("This site requires cookies to be enabled, please enable em in your webbrowser"))

    if should_redirect:
        return HttpResponseRedirect(reverse(details, args=[event.pk]))
    else:
        #* ``test_cookie_worked()``
        #Returns either ``True`` or ``False``, depending on whether the user's
        #browser accepted the test cookie. Due to the way cookies work, you'll
        #have to call ``set_test_cookie()`` on a previous, separate page request.
        #See "Setting test cookies" below for more information.
        #
        # hence we redirect the user to another page so our test cookie test always works.
        return HttpResponseRedirect(reverse(enter_codeword_entry, args=[event.pk]))


def reset(request, entry):
    keys = request.session.get('keys')
    if keys and int(entry) in keys.keys():
        del keys[int(entry)]
        request.session['keys'] = keys

    return HttpResponseRedirect(request.META.get('HTTP_REFERER', reverse('geocal_list')))


def about(request):
    return render_to_response('geocal/about.html', {}, context_instance=RequestContext(request))
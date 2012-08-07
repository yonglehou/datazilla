import json

from django.http import HttpResponse

from datazilla.controller.admin.stats import perftest_stats
from datazilla.model import utils

APP_JS = 'application/json'

def get_runs_by_branch(request, project):
    """
    Return the testruns for a project broken down by branches.

    days_ago: required.  Number of days ago for the "start" of the range.
    numdays: optional.  Number of days since days_ago.  Will default to
        "all since days ago"

    """
    range = get_range(request)
    stats = perftest_stats.get_runs_by_branch(
        project,
        range["start"],
        range["stop"],
        )
    return HttpResponse(json.dumps(stats), mimetype=APP_JS)


def get_ref_data(request, project, table):
    """Get simple list of ref_data for ``table`` in ``project``"""
    stats = perftest_stats.get_ref_data(project, table)
    return HttpResponse(json.dumps(stats), mimetype=APP_JS)


def get_range(request):
    """Utility function to extract the date range from the request."""
    days_ago = int(request.GET.get("days_ago"))
    numdays = int(request.GET.get("numdays", 0))

    return utils.get_day_range(days_ago, numdays)

import ast
import requests
from django.conf import settings


def list_to_dict(lst):
    result = {}
    for item in lst:
        key, value = item.split(":")
        if key in result:
            if isinstance(result[key], list):
                result[key].append(value)
            else:
                result[key] = [result[key], value]
        else:
            result[key] = [value]
    return result


def dict_to_geo_string(geo_dict):
    return ";".join([f"{k}:{','.join(v)}" for k, v in geo_dict.items()])


def get_list_of_signals_filtered_by_geo(geos):
    geos = list_to_dict(ast.literal_eval(geos))
    # send request to epidata api here
    # temporary disabled
    # ------------------------------------------
    # url = f"{settings.COVIDCAST_URL}geo_coverage"
    url = "http://localhost:10080/epidata/covidcast/geo_coverage"
    params = {"geo": dict_to_geo_string(geos)}
    response = requests.get(url, params=params)
    # return response.json()
    # ------------------------------------------
    return {
        "epidata": [
            {"source": "fb-survey", "signal": "7dav_outpatient_covid"},
            {"source": "fluview_meta", "signal": "adult_icu_bed_covid_utilization"},
            {
                "source": "fluview_meta",
                "signal": "adult_icu_bed_covid_utilization_numerator",
            },
            {
                "source": "fluview_meta",
                "signal": "adult_icu_bed_utilization_denominator",
            },
            {"source": "nchs-mortality", "signal": "confirmed_7dav_incidence_prop"},
            {"source": "usa-facts", "signal": "confirmed_incidence_prop"},
        ]
    }

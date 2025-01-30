import ast
import requests


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


def get_list_of_signals_filtered_by_geo(geos):
    geos = list_to_dict(ast.literal_eval(geos))
    # send request to epidata api here
    # url = f"{settings.SIGNALS_API_URL}/geo_coverage?geo=hrr:geo1,geo2;county:*"
    # params = {"geo": [f"{k}:{','.join(v)}" for k, v in geos.items()]}
    # response = requests.get(url, params=params)
    print(geos)
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

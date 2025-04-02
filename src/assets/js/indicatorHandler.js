class IndicatorHandler{
    constructor() {
        this.indicators = {};
    }

    fluviewIndicatorsMapping = {
        "wili": "%wILI",
        "ili": "%ILI", 
    }

    fluSurvRegions = [
        { value: 'network_all', label: 'Entire Network' },
        { value: 'network_eip', label: 'EIP Netowrk' },
        { value: 'network_ihsp', label: 'IHSP Network' },
        { value: 'CA', label: 'CA' },
        { value: 'CO', label: 'CO' },
        { value: 'CT', label: 'CT' },
        { value: 'GA', label: 'GA' },
        { value: 'IA', label: 'IA' },
        { value: 'ID', label: 'ID' },
        { value: 'MD', label: 'MD' },
        { value: 'MI', label: 'MI' },
        { value: 'MN', label: 'MN' },
        { value: 'NM', label: 'NM' },
        { value: 'NY_albany', label: 'NY (Albany)' },
        { value: 'NY_rochester', label: 'NY (Rochester)' },
        { value: 'OH', label: 'OH' },
        { value: 'OK', label: 'OK' },
        { value: 'OR', label: 'OR' },
        { value: 'RI', label: 'RI' },
        { value: 'SD', label: 'SD' },
        { value: 'TN', label: 'TN' },
        { value: 'UT', label: 'UT' },
    ]

    fluviewRegions = [
        { id: 'nat', text: 'U.S. National' },
        { id: 'hhs1', text: 'HHS Region 1' },
        { id: 'hhs2', text: 'HHS Region 2' },
        { id: 'hhs3', text: 'HHS Region 3' },
        { id: 'hhs4', text: 'HHS Region 4' },
        { id: 'hhs5', text: 'HHS Region 5' },
        { id: 'hhs6', text: 'HHS Region 6' },
        { id: 'hhs7', text: 'HHS Region 7' },
        { id: 'hhs8', text: 'HHS Region 8' },
        { id: 'hhs9', text: 'HHS Region 9' },
        { id: 'hhs10', text: 'HHS Region 10' },
        { id: 'cen1', text: 'Census Region 1' },
        { id: 'cen2', text: 'Census Region 2' },
        { id: 'cen3', text: 'Census Region 3' },
        { id: 'cen4', text: 'Census Region 4' },
        { id: 'cen5', text: 'Census Region 5' },
        { id: 'cen6', text: 'Census Region 6' },
        { id: 'cen7', text: 'Census Region 7' },
        { id: 'cen8', text: 'Census Region 8' },
        { id: 'cen9', text: 'Census Region 9' },
        { id: 'AK', text: 'AK' },
        { id: 'AL', text: 'AL' },
        { id: 'AR', text: 'AR' },
        { id: 'AZ', text: 'AZ' },
        { id: 'CA', text: 'CA' },
        { id: 'CO', text: 'CO' },
        { id: 'CT', text: 'CT' },
        { id: 'DC', text: 'DC' },
        { id: 'DE', text: 'DE' },
        { id: 'FL', text: 'FL' },
        { id: 'GA', text: 'GA' },
        { id: 'HI', text: 'HI' },
        { id: 'IA', text: 'IA' },
        { id: 'ID', text: 'ID' },
        { id: 'IL', text: 'IL' },
        { id: 'IN', text: 'IN' },
        { id: 'KS', text: 'KS' },
        { id: 'KY', text: 'KY' },
        { id: 'LA', text: 'LA' },
        { id: 'MA', text: 'MA' },
        { id: 'MD', text: 'MD' },
        { id: 'ME', text: 'ME' },
        { id: 'MI', text: 'MI' },
        { id: 'MN', text: 'MN' },
        { id: 'MO', text: 'MO' },
        { id: 'MS', text: 'MS' },
        { id: 'MT', text: 'MT' },
        { id: 'NC', text: 'NC' },
        { id: 'ND', text: 'ND' },
        { id: 'NE', text: 'NE' },
        { id: 'NH', text: 'NH' },
        { id: 'NJ', text: 'NJ' },
        { id: 'NM', text: 'NM' },
        { id: 'NV', text: 'NV' },
        { id: 'NY', text: 'NY' },
        { id: 'OH', text: 'OH' },
        { id: 'OK', text: 'OK' },
        { id: 'OR', text: 'OR' },
        { id: 'PA', text: 'PA' },
        { id: 'RI', text: 'RI' },
        { id: 'SC', text: 'SC' },
        { id: 'SD', text: 'SD' },
        { id: 'TN', text: 'TN' },
        { id: 'TX', text: 'TX' },
        { id: 'UT', text: 'UT' },
        { id: 'VA', text: 'VA' },
        { id: 'VT', text: 'VT' },
        { id: 'WA', text: 'WA' },
        { id: 'WI', text: 'WI' },
        { id: 'WV', text: 'WV' },
        { id: 'WY', text: 'WY' },
        { id: 'ny_minus_jfk', text: 'NY (minus NYC)' },
        { id: 'as', text: 'American Samoa' },
        { id: 'mp', text: 'Mariana Islands' },
        { id: 'gu', text: 'Guam' },
        { id: 'pr', text: 'Puerto Rico' },
        { id: 'vi', text: 'Virgin Islands' },
        { id: 'ord', text: 'Chicago' },
        { id: 'lax', text: 'Los Angeles' },
        { id: 'jfk', text: 'New York City' },
    ]

    checkForCovidcastIndicators() {
        return this.indicators.some((indicator) => {
            return indicator["_endpoint"] === "covidcast";
        });
    }

    showFluviewRegions() {
        var fluviewRegionSelect = `
        <div class="row margin-top-1rem">
            <div class="col-2">
                <label for="fluviewRegions" class="col-form-label">ILINet Location(s):</label>
            </div>
            <div class="col-10">
                <select id="fluviewRegions" name="fluviewRegions" class="form-select" multiple="multiple"></select>
            </div>
        </div>`
        $("#otherEndpointLocations").append(fluviewRegionSelect)
        $("#fluviewRegions").select2({
            placeholder: "Select ILINet Location(s)",
            data: this.fluviewRegions,
            allowClear: true,
            width: '100%',
        });
    }

    generateEpivisCustomTitle(indicator, geoValue) {
        var epivisCustomTitle;
        if (indicator["member_short_name"]) {
            epivisCustomTitle = `${indicator["signal_set_short_name"]}:${indicator["member_short_name"]} : ${geoValue}`
        } else {
            epivisCustomTitle = `${indicator["signal_set_short_name"]} : ${geoValue}`
        }
        return epivisCustomTitle;
    }

    plotData(){
        var dataSets = {};
        var covidCastGeographicValues = $('#geographic_value').select2('data');
        var fluviewRegions = $('#fluviewRegions').select2('data');
        console.log(fluviewRegions)
        
        this.indicators.forEach((indicator) => {
            if (indicator["_endpoint"] === "covidcast") {
                covidCastGeographicValues.forEach((geoValue) => {
                    var geographicValue = (typeof geoValue.id === 'string') ? geoValue.id.toLowerCase() : geoValue.id;
                    var geographicType = geoValue.geoType;
                    dataSets[`${indicator["signal"]}_${geographicValue}`] = {
                        color: '#'+(Math.random() * 0xFFFFFF << 0).toString(16).padStart(6, '0'),
                        title: "value",
                        params: {
                            _endpoint: indicator["_endpoint"],
                            data_source: indicator["data_source"],
                            signal: indicator["signal"],
                            time_type: indicator["time_type"],
                            geo_type: geographicType,
                            geo_value: geographicValue,
                            custom_title: this.generateEpivisCustomTitle(indicator, geoValue.text)
                        }
                    }
                })
            } else if (indicator["_endpoint"] === "fluview") {
                fluviewRegions.forEach((region) => {
                    dataSets[`${indicator["signal"]}_${indicator["_endpoint"]}_${region.id}`] = {
                        color: '#'+(Math.random() * 0xFFFFFF << 0).toString(16).padStart(6, '0'),
                        title: this.fluviewIndicatorsMapping[indicator["signal"]] || indicator["signal"],
                        params: {
                            _endpoint: indicator["_endpoint"],
                            regions: region.id,
                            custom_title: this.generateEpivisCustomTitle(indicator, region.text)
                        }
                    }
                })
            }
            // else if (indicator["_endpoint"] === "flusurv") {
            //     // TODO: Add support for flusurv. Need to figure out how to get the geographic value for flusurv.
            //     // For now, we will just use the static geographic value.
            //     dataSets[`${indicator["signal"]}_${indicator["_endpoint"]}`] = {
            //         color: '#'+(Math.random() * 0xFFFFFF << 0).toString(16).padStart(6, '0'),
            //         title: indicator["signal"],
            //         params: {
            //             _endpoint: indicator["_endpoint"],
            //             locations: "network_all",
            //             custom_title: this.generateEpivisCustomTitle(indicator, "Entire Network")
            //         }
            //     }
            // } else if (indicator["_endpoint"] === "gft") {
            //     // TODO: Add support for gft. Need to figure out how to get the geographic value for gft.
            //     // For now, we will just use the static geographic value.
            //     dataSets[`${indicator["signal"]}_${indicator["_endpoint"]}`] = {
            //         color: '#'+(Math.random() * 0xFFFFFF << 0).toString(16).padStart(6, '0'),
            //         title: indicator["signal"],
            //         params: {
            //             _endpoint: indicator["_endpoint"],
            //             locations: "nat",
            //             custom_title: this.generateEpivisCustomTitle(indicator, "U.S. National")
            //         }
            //     }
            // } else if (indicator["_endpoint"] === "wiki") {
            //     dataSets[`${indicator["signal"]}_${indicator["_endpoint"]}`] = {
            //         color: '#'+(Math.random() * 0xFFFFFF << 0).toString(16).padStart(6, '0'),
            //         title: indicator["signal"],
            //         params: {
            //             _endpoint: indicator["_endpoint"],
            //             articles: "fatigue_(medical)",
            //             language: "en",
            //             resolution: "daily",
            //             custom_title: this.generateEpivisCustomTitle(indicator, "U.S. National")
            //         }
            //     }
            // } else if (indicator["_endpoint"] === "cdc") {
            //     dataSets[`${indicator["signal"]}_${indicator["_endpoint"]}`] = {
            //         color: '#'+(Math.random() * 0xFFFFFF << 0).toString(16).padStart(6, '0'),
            //         title: indicator["signal"],
            //         params: {
            //             _endpoint: indicator["_endpoint"],
            //             auth: "390da13640f61",
            //             locations: "nat",
            //             custom_title: this.generateEpivisCustomTitle(indicator, "U.S. National")
            //         }
            //     }
            // } else if(indicator["_endpoint"] === "sensors") {
            //     dataSets[`${indicator["signal"]}_${indicator["_endpoint"]}`] = {
            //         color: '#'+(Math.random() * 0xFFFFFF << 0).toString(16).padStart(6, '0'),
            //         title: indicator["signal"],
            //         params: {
            //             _endpoint: indicator["_endpoint"],
            //             auth: "390da13640f61",
            //             names: "wiki",
            //             locations: "nat",
            //             custom_title: this.generateEpivisCustomTitle(indicator, "U.S. National")
            //         }
            //     }
            // }
        });
        var requestParams = [];
        for (var key in dataSets) {
            requestParams.push(dataSets[key]);
        }

        var urlParamsEncoded = btoa(`{"datasets":${JSON.stringify(requestParams)}}`);
        
        var linkToEpivis = `${epiVisUrl}#${urlParamsEncoded}`
        window.open(linkToEpivis, '_blank').focus();
    }   
}
function initSelect2(elementId, data) {
    $(`#${elementId}`).select2({
        data: data,
        minimumInputLength: 0,
        maximumSelectionLength: 5,
    });
}

let checkedSignalMembers = []

function showWarningAlert(warningMessage, slideUpTime = 2000) {
    $("#warning-alert").html(warningMessage);
    $("#warning-alert").fadeTo(2000, 500).slideUp(slideUpTime, function() {
        $("#warning-alert").slideUp(slideUpTime);
    });
}

function checkGeoCoverage(geoType, geoValue) {
    var notCoveredSignals = [];
    $.ajax({
        url: "epidata/covidcast/geo_coverage/",
        type: 'GET',
        async: false,
        data: {
            'geo': `${geoType}:${geoValue}`
        },
        success: function (result) {
            checkedSignalMembers.forEach(signal => {
                var covered = result["epidata"].some(
                    e => (e.source === signal.data_source && e.signal === signal.signal)
                )
                if (!covered) {
                    notCoveredSignals.push(signal);
                }
            })
        }
    })
    return notCoveredSignals;
}

function showNotCoveredGeoWarningMessage(notCoveredSignals, geoValue) {
    var warningMessage = `The following signals are not available at selected geographic level "${geoValue}": <br>`;
    notCoveredSignals.forEach(signal => {
        warningMessage += `${signal.display_name} <br>`
    })
    showWarningAlert(warningMessage, 5000);

}

$('#geographic_value').on('select2:select', function (e) {
    var geo = e.params.data;
    var notCoveredSignals = checkGeoCoverage(geo.geoType, geo.id)
    if (notCoveredSignals.length > 0) {
        showNotCoveredGeoWarningMessage(notCoveredSignals, geo.text);
    }
});

function plotData() {
    var dataSets = {};
    var geographicValues = $('#geographic_value').select2('data');
    checkedSignalMembers.forEach((signal) => {
        geographicValues.forEach((geoValue) => {
            var geographicValue = (typeof geoValue.id === 'string') ? geoValue.id.toLowerCase() : geoValue.id;
            var geographicType = geoValue.geoType;
            dataSets[`${signal["signal"]}_${geographicValue}`] = {
                color: '#'+(Math.random() * 0xFFFFFF << 0).toString(16).padStart(6, '0'),
                title: "value",
                params: {
                    _endpoint: signal["_endpoint"],
                    data_source: signal["data_source"],
                    signal: signal["signal"],
                    time_type: signal["time_type"],
                    geo_type: geographicType,
                    geo_value: geographicValue,
                    custom_title: `${signal["data_source"]}:${signal["signal"]} - ${geoValue.text}`
                }
            }
        })
        
    });
    
    var requestParams = [];
    for (var key in dataSets) {
        requestParams.push(dataSets[key]);
    }

    var urlParamsEncoded = btoa(`{"datasets":${JSON.stringify(requestParams)}}`);
    
    var linkToEpivis = `${epiVisUrl}#${urlParamsEncoded}`
    window.open(linkToEpivis, '_blank').focus();
}


// Function to update the modal content
function updateSelectedSignals(dataSource, signalDisplayName, signalSet, signal) {
    var selectedSignalsList = document.getElementById('selectedSignalsList');

    var tr = document.createElement('tr');
    tr.setAttribute('id', `${dataSource}_${signal}`);
    var signalSetName = document.createElement('td');
    signalSetName.textContent = signalSet;
    tr.appendChild(signalSetName);
    var signalName = document.createElement('td');
    signalName.textContent = signalDisplayName;
    tr.appendChild(signalName);
    selectedSignalsList.appendChild(tr);
}

function addSelectedSignal(element) {
    if (element.checked) {
        checkedSignalMembers.push({
            _endpoint: element.dataset.endpoint,
            data_source: element.dataset.datasource,
            signal: element.dataset.signal,
            time_type: element.dataset.timeType,
            signal_set: element.dataset.signalSet,
            display_name: element.dataset.signalDisplayname
        });
        updateSelectedSignals(element.dataset.datasource, element.dataset.signalDisplayname, element.dataset.signalSet, element.dataset.signal);
    } else {
        checkedSignalMembers = checkedSignalMembers.filter(signal => signal.signal !== element.dataset.signal);
        document.getElementById(`${element.dataset.datasource}_${element.dataset.signal}`).remove();
    }


    if (checkedSignalMembers.length > 0) {
        $("#showSelectedSignalsButton").show();
    } else {
        $("#showSelectedSignalsButton").hide();
    }
}

// Add an event listener to each 'bulk-select' element
let bulkSelectDivs = document.querySelectorAll('.bulk-select');
bulkSelectDivs.forEach(div => {
    div.addEventListener('click', function(event) {
        let form = this.nextElementSibling;
        let showMoreLink = form.querySelector('a');
        let checkboxes = form.querySelectorAll('input[type="checkbox"]');

        if (event.target.checked === true) {
            checkboxes.forEach((checkbox, index) => {
                checkbox.checked = true;
                if (index > 4) {
                    checkbox.parentElement.style.display = checkbox.parentElement.style.display === 'none' ? 'block' : null;
                }
            })
            if (showMoreLink) {
                showMoreLink.innerText = 'Show less...';
            }
        } else if (event.target.checked === false) {
            checkboxes.forEach((checkbox, index) => {
                checkbox.checked = false
                if (index > 4) {
                    checkbox.parentElement.style.display = checkbox.parentElement.style.display === 'block' ? 'none' : null;
                }
            });
            if (showMoreLink) {
                showMoreLink.innerText = 'Show more...';
            }
        }
    });
});

var tableHeight = window.screen.width / 3.4;

function calculate_table_height() {
    var h = Math.max(document.documentElement.clientHeight, window.innerHeight || 0);
    var percent = 60;
    if (h > 1000) {
        percent = 70;
    }
    return (percent * h) / 100;
}


var table = new DataTable('#signalSetsTable', {
    fixedHeader: true,
    searching: false,
    paging: false,
    scrollCollapse: true,
    scrollX: true,
    scrollY: calculate_table_height(),
    fixedColumns: {
        left: 2
    },
    ordering: false,
    mark: true,
    layout: {
        topStart: {
            buttons: [
                {
                    extend: 'colvis',
                    columns: 'th:nth-child(n+3)'
                }
            ]
        }
    },
    language: {
        "info":           "Showing _TOTAL_ / _MAX_ Signal Sets",
        "infoEmpty":      "",
        "infoFiltered":   "",
    },
});

function format (signalSetId, relatedSignals) {
    var signals = relatedSignals.filter((signal) => signal.signal_set === signalSetId)

    if (signals.length > 0) {
        var tableMarkup = '<table class="table" cellpadding="5" cellspacing="0" border="0" style="padding-left:50px;">'+
                    '<thead>'+
                        '<th></th>'+
                        '<th>Signal Name</th>'+
                        '<th>Signal Description</th>'+
                        '<th></th>'+
                    '</thead>'+
                    '<tbody>'
        signals.forEach((signal) => {
            checked = checkedSignalMembers.filter((obj) => obj.data_source == signal.source && obj.signal == signal.name).length;
            checked = checked ? "checked" : ""
            tableMarkup += '<tr>'+
                                `<td><input type="checkbox" name="selectedSignal" onclick="addSelectedSignal(this)" data-signal-displayname='${signal.display_name}' data-endpoint="${signal.endpoint}" data-datasource="${signal.source}" data-signal="${signal.name}" data-time-type="${signal.time_type}" data-signal-set="${signal.signal_set_name}" ${checked}></td>`+
                                `<td>${signal.display_name}</td>`+
                                `<td>${signal.description}</td>`+
                                '<td style="width: 60%"></td>'+
                            '</tr>'
        }) 
        tableMarkup += '</tbody></table>'
    } else {
        tableMarkup = "<p>No available signals yet.</p>"
    }
    return tableMarkup;
}


function exportData() {
    var geographicValues = $('#geographic_value').select2('data');
    geographicValues = Object.groupBy(geographicValues, ({ geoType }) => [geoType])
    var geoTypes = Object.keys(geographicValues);

    var startDate = document.getElementById('start_date').value;
    var endDate = document.getElementById('end_date').value;

    var manualDataExport = "To download data, please click on the link or copy/paste command into your terminal: \n\n"
    
    checkedSignalMembers.forEach((signal) => {
        geoTypes.forEach((geoType) => {
            var geoValues = geographicValues[geoType].map((el) => (typeof el.id === 'string') ? el.id.toLowerCase() : el.id).join(",");
            if (signal["time_type"] === "week") {
                startDate = getDateYearWeek(new Date(startDate));
                endDate = getDateYearWeek(new Date(endDate));
            };
            var exportUrl = `https://api.delphi.cmu.edu/epidata/covidcast/csv?signal=${signal["data_source"]}:${signal["signal"]}&start_day=${startDate}&end_day=${endDate}&geo_type=${geoType}&geo_values=${geoValues}`;
            manualDataExport += `wget --content-disposition <a href="${exportUrl}">${exportUrl}</a>\n`
        });
    });
    $('#modeSubmitResult').html(manualDataExport);
}

function previewData() {
    var geographicValues = $('#geographic_value').select2('data');
    geographicValues = Object.groupBy(geographicValues, ({ geoType }) => [geoType])
    var geoTypes = Object.keys(geographicValues);
    var previewExample = [];
    var requests = [];
    checkedSignalMembers.forEach((signal) => {
        var startDate = document.getElementById("start_date").value;
        var endDate = document.getElementById("end_date").value;
        if (signal["time_type"] === "week") {
            startDate = getDateYearWeek(new Date(startDate));
            endDate = getDateYearWeek(new Date(endDate));
        };
        
        var requestSent = false;
        if (!requestSent) {
            geoTypes.forEach((geoType) => {
                var geoValues = geographicValues[geoType].map((el) => (typeof el.id === 'string') ? el.id.toLowerCase() : el.id).join(",");
                $('#loader').show();
                var request = $.ajax({
                    url: "epidata/covidcast/",
                    type: 'GET',
                    async: true,
                    data: {
                        'time_type': signal["time_type"],
                        'time_values': `${startDate}--${endDate}`,
                        'data_source': signal["data_source"],
                        'signal': signal["signal"],
                        'geo_type': geoType,
                        'geo_values': geoValues
                    },
                    success: function (result) {
                        if (result["epidata"].length != 0) {
                            previewExample.push({epidata: result["epidata"][0], result: result["result"], message: result["message"]})
                        } else {
                            previewExample.push({epidata: result["epidata"], result: result["result"], message: result["message"]})
                        }
                    }
                })
                requests.push(request);
            })
        }
    })
    $.when.apply($, requests).then(function() {
        $('#loader').hide();
    $('#modeSubmitResult').html(JSON.stringify(previewExample, null, 2));
    requestSent = true;
    })
}


// Plot/Export/Preview data block

var currentMode = 'preview';

function handleModeChange(mode) {
    $('#modeSubmitResult').html('');

    var choose_dates = document.getElementsByName('choose_date');

    if (mode === 'epivis') {
        currentMode = 'epivis';
        choose_dates.forEach((el) => {
            el.style.display = 'none';
        });
        $('#modeSubmitResult').html('');
    } else if (mode === 'export') {
        currentMode = 'export';
        choose_dates.forEach((el) => {
            el.style.display = 'flex';
        });
        $('#modeSubmitResult').html('');
    } else {
        currentMode = 'preview';
        choose_dates.forEach((el) => {
            el.style.display = 'flex';
        });
    }
    document.getElementsByName("modes").forEach((el) => {
        if (currentMode === el.value) {
            el.checked = true;
        }
    });
}

function getDateYearWeek(date) {
    const currentDate =
        (typeof date === 'object') ? date : new Date();
    const januaryFirst =
        new Date(currentDate.getFullYear(), 0, 1);
    const daysToNextMonday =
        (januaryFirst.getDay() === 1) ? 0 :
        (7 - januaryFirst.getDay()) % 7;
    const nextMonday =
        new Date(currentDate.getFullYear(), 0,
        januaryFirst.getDate() + daysToNextMonday);

    var weekNumber = (currentDate < nextMonday) ? 52 :
    (currentDate > nextMonday ? Math.ceil(
    (currentDate - nextMonday) / (24 * 3600 * 1000) / 7) : 1);

    if (weekNumber < 10) {
        weekNumber = `0${weekNumber}`;
    }

    const year = currentDate.getFullYear()

    return `${year}${weekNumber}`;
}

function submitMode(event) {
    event.preventDefault();

    if (currentMode === 'epivis') {
        plotData();
    } else if (currentMode === 'export') {
        exportData();
    } else {
        previewData();
    }
}
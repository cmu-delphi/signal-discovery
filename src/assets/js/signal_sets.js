function initSelect2(elementId, data) {
    $(`#${elementId}`).select2({
        data: data,
        minimumInputLength: 0,
        maximumSelectionLength: 5,
    });
}


function getFilteredGeographicValues(geographicType, geoValues) {
    var data = geoValues.reduce((data, geoValue) => {
        if (geoValue.geoType === geographicType) {
            data.push(geoValue);
        }
        return data;
    }, []);
    return data;
}

function initGeographicValueSelect(geoValues, geographicType = null) {
    if (geographicType) {
        var data = getFilteredGeographicValues(geographicType, geoValues);
    } else {
        data = [];
    }

    initSelect2('geographic_value', data)
}

document.getElementById('geographic_type').addEventListener("change", (event) => {
    $('#geographic_value').empty();
    $('#modeSubmitResult').html('');
    initGeographicValueSelect(geoValues, event.target.value);
})

let checkedSignalMembers = []

function plotData(epivisUrl) {
    var dataSets = {};

    var geographicType = document.getElementById('geographic_type').value;
    var geographicValues = $('#geographic_value').select2('data').map((el) => (typeof el.id === 'string') ? el.id.toLowerCase() : el.id);
    if (geographicType === 'Choose...' || geographicValues.length === 0) {
        showWarningAlert("Geographic Type or Geographic Value is not selected.");
        return;
    }

    checkedSignalMembers.forEach((signal) => {
        geographicValues.forEach((geoValue) => {
            dataSets[`${signal["signal"]}_${geoValue}`] = {
                color: '#'+(Math.random() * 0xFFFFFF << 0).toString(16).padStart(6, '0'),
                title: "value",
                params: {
                    _endpoint: signal["_endpoint"],
                    data_source: signal["data_source"],
                    signal: signal["signal"],
                    time_type: signal["time_type"],
                    geo_type: geographicType,
                    geo_value: geoValue
                }
            }
        })
        
    });
    
    var requestParams = [];
    for (var key in dataSets) {
        requestParams.push(dataSets[key]);
    }

    var urlParamsEncoded = btoa(`{"datasets":${JSON.stringify(requestParams)}}`);
    
    var linkToEpivis = `${epivisUrl}#${urlParamsEncoded}`
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
            time_type: element.dataset.timetype,
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


var table = new DataTable('#signalSetsTable', {
    fixedHeader: true,
    paging: false,
    scrollCollapse: true,
    scrollX: true,
    scrollY: 550,
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
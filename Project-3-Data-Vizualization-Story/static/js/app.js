// Hi Team!!
// This is a PLACEHOLDER for our JS file
// Add Leaflet Map
// Add filters
// Add chart
// Add table













// Get metadata for selected sample
function buildMetadata(sample) {
  var meta_sample = d3.json(`/metadata/${sample}`);

  // Use d3 to select the panel with id of `#sample-metadata` and clear existing metadata
  meta_sample.then(sample => {
    var panel_body = d3.select('#sample-metadata');
    panel_body.html('');

    // Use `Object.entries` to add each key and value pair to the panel
    Object.entries(sample).forEach(([key, value]) => {
      panel_body.append('h6').text(`${key}: ${value}`);
    });
  });
}

function buildCharts(sample) {
  // Use `d3.json` to fetch the sample data for the plots
  var chart_sample = d3.json(`/samples/${sample}`);

  chart_sample.then(sample => {

    // Build a Bubble Chart using the sample data
    var bubble_data = [{
      type: 'scatter',
      x: sample.otu_ids,
      y: sample.sample_values,
      text: sample.otu_labels,
      mode: 'markers',
      marker: {
        size: sample.sample_values,
        color: sample.otu_ids,
        colorscale: 'Earth'
      },
    }];

    var bubble_layout = {
      xaxis: {
        title: 'Operational Taxonomic Units (OTIs) IDs'
      }
    };

    Plotly.newPlot('bubble', bubble_data, bubble_layout);

    // Build a Pie Chart of top 10 values
    var pieData = [{
      values: sample.sample_values.slice(0, 10),
      labels: sample.otu_ids.slice(0, 10),
      hovertext: sample.otu_labels.slice(0, 10),
      hoverinfo: 'hovertext',
      type: 'pie'
    }];

    var pieLayout = {
      margin: {
        t: 0,
        l: 0
      }
    };

    Plotly.plot('pie', pieData, pieLayout);
  });
}

function init() {
  // Grab a reference to the dropdown select element
  var selector = d3.select('#selDataset');

  // Use the list of sample names to populate the select options
  d3.json('/names').then(sampleNames => {
    sampleNames.forEach(sample => {
      selector
        .append('option')
        .text(sample)
        .property('value', sample);
    });

    // Use the first sample from the list to build the initial plots
    const firstSample = sampleNames[0];
    buildCharts(firstSample);
    buildMetadata(firstSample);
  });
}

// Fetch new data each time a new sample is selected
function optionChanged(newSample) {
  buildCharts(newSample);
  buildMetadata(newSample);
}

// Initialize the dashboard
init();
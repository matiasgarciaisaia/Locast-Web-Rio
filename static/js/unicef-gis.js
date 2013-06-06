//Let's use this as a way to decouple code from global variables :/
var UNICEF_GIS_CONSTANTS = {
  static_url : STATIC_URL,
}

//TODO: move to its own file
function Report(geofeature) {
  this.feature = geofeature;

  this.iconByUrgencyLevel = [
    UNICEF_GIS_CONSTANTS.static_url + 'img/pins/green.png',
    UNICEF_GIS_CONSTANTS.static_url + 'img/pins/yellow.png',
    UNICEF_GIS_CONSTANTS.static_url + 'img/pins/orange.png',
    UNICEF_GIS_CONSTANTS.static_url + 'img/pins/red_orange.png',
    UNICEF_GIS_CONSTANTS.static_url + 'img/pins/red.png',
  ];
}

Report.prototype.iconMarker = function() {
  return this.feature.data.urgency_level >= this.iconByUrgencyLevel.length ?
    this.iconByUrgencyLevel[this.iconByUrgencyLevel.length - 1] :
    this.iconByUrgencyLevel[this.feature.data.urgency_level];
}


function UnicefGIS() {}

UnicefGIS.prototype.iconMarker = function(feature) {
  return (new Report(feature)).iconMarker();
}

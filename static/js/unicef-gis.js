//Let's use this as a way to decouple code from global variables :/
var UNICEF_GIS_CONSTANTS = {
  static_url : STATIC_URL,
  app_name : APP_NAME,
  full_base_url : FULL_BASE_URL,
  project_description : PROJECT_DESCRIPTION,
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

function postToFB(name, link, pic) {
  FB.ui(
    {
      method: 'feed',
      name: name,
      link: UNICEF_GIS_CONSTANTS.full_base_url + link,
      picture: UNICEF_GIS_CONSTANTS.full_base_url + pic,
      caption: UNICEF_GIS_CONSTANTS.app_name,
      description: UNICEF_GIS_CONSTANTS.project_description,
    },
    function(response) {}
  );    
}

function UnicefGIS() {}

UnicefGIS.prototype.iconMarker = function(feature) {
  var marker = (new Report(feature)).iconMarker()

  if (marker) return marker;
  return UNICEF_GIS_CONSTANTS.static_url + 'img/pins/green.png';
}



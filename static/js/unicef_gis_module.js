function UrgencyRankController($scope, $http) {
  $http.get('/api/cast/urgency_rank.json').success(function(data) {
    $scope.casts = data;
  });

  $scope.update = function(query) {
    //Update the rank view with the ones corresponding to the current itinerary
    if (query.startsWith("?itinerary=")){
      //Ok, this is nasty, but we're transitioning...
      var itineraryId = query.substring(11);

      $http.get('/api/cast/urgency_rank/' + itineraryId + '.json').success(function(data) {
        $scope.casts = data;
      });
    } else if (query == "?") {
      //If there's no filter by itinerary we'll want the general ranking
      $http.get('/api/cast/urgency_rank.json').success(function(data) {
        $scope.casts = data;
      });
    }
  }
}

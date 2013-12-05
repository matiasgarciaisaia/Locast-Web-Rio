var galleryModule = angular.module('galleryModule', ['components']);

galleryModule.controller('GalleryController', function($scope, $http) {
  $scope.currentPage = 1;
  $scope.items = [];
  $scope.currentCategory = null;
  $scope.lastPage = null;

  $scope.nextPage = function() {
    $scope.currentPage = $scope.currentPage + 1;
  };

  $scope.previousPage = function() {
    $scope.currentPage = $scope.currentPage - 1;
  }

  $scope.setCategory = function(category) {
    if ($scope.currentCategory != null && $scope.currentCategory.id == category.id)
      return;

    $scope.currentCategory = category;
  }

  var refreshData = function() {
    if ($scope.currentCategory == null) {
      $scope.items = [];
    } else {
      var cat = $scope.currentCategory.id;
      var page = $scope.currentPage;
      var query = '/api/cast/?itinerary=' + cat + '&page=' + page + '&pagesize=20';

      $scope.working = true;

      $http.get(query)
        .success(function(data) {
            if (page == $scope.currentPage)
              $scope.items = data;
          })
        .error(function(data, status, headers, config) {
          if (data == "Empty Page" && status == 400) {
            $scope.lastPage = page - 1;

            if ($scope.lastPage != null && $scope.currentPage > $scope.lastPage)
              $scope.currentPage = $scope.lastPage;
          }
        });
    }
  }

  $scope.$watch('currentPage', refreshData);
  $scope.$watch('currentCategory', function(newValue, oldValue) {
    if (newValue == null || oldValue == null || newValue.id != oldValue.id) {
      if ($scope.currentPage == 1)
        refreshData();
      else
        $scope.currentPage = 1;  

      $scope.lastPage = null;
    }
  });
});
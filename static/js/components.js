//I know this sucks. TODO: design a robust client-side route policy
var templates = {
	'ugisGallery' : '/static/js/galleryTemplate.html',
	'ugisCategoriesCombo' : '/static/js/categoriesComboTemplate.html',
};

var components = angular.module('components', [])

components.directive('ugisGallery', function() {
	return {
		restrict: 'E',
		transclude: false,
		scope: {
			items: '&',
			nextPage: '&',
			previousPage: '&',
			currentPage: '&',
			lastPage: '&',
			enableControls: '&'
		},
		controller: function($scope) {
			$scope.elementsToShow = function() {
				return $scope.items() != null && $scope.items().length > 0;
			}

			$scope.atFirstPage = function() {
				return $scope.currentPage() == 1;
			}

			$scope.atLastPage = function() {
				return $scope.lastPage() != null && $scope.lastPage() <= $scope.currentPage();
			}

			$scope.nextPageCaption = function() {
				if ($scope.atLastPage())
					return "Currently at last page"
				else
					return "Next page";
			}

			$scope.previousPageCaption = function() {
				if ($scope.atFirstPage())
					return "Currently at first page"
				else
					return "Previous page";
			}
		},
		templateUrl: templates['ugisGallery'],
		replace: false
	};
});

components.directive('ugisCategoriesCombo', function() {
	return {
		restrict: 'E',
		transclude: false,
		scope: {
			selectionChanged: '&'
		},
		controller: function($scope, $http) {
		  $scope.categories = [];  
		  $scope.selectedCategory = null;

		  var query = '/api/itinerary/';

		  $http.get(query).success(function(data) {
		      $scope.categories = data;

		      if ($scope.selectedCategory == null && $scope.categories != null && $scope.categories.length > 0)
		      	$scope.selectedCategory = $scope.categories[0];
		  });

		  $scope.$watch('selectedCategory', function() {
		  	$scope.selectionChanged({category: $scope.selectedCategory});
		  });
		},
		templateUrl: templates['ugisCategoriesCombo'],
		replace: true,
	}
});
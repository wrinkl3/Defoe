  angular.module('defoe', ['ngAnimate', 'ngSanitize', 'ui.bootstrap', 'angularLoadingDots']).controller('CheckController', ['$scope', '$log', '$http', '$timeout',
  function($scope, $log, $http, $timeout) {


  $scope.isLoading1 = false;
  $scope.isLoading2 = false;

  $scope.putMessage1 = function(text, color){
    $scope.result1 = text;
    $scope.rescolor1 = color;
  }

  $scope.putMessage2 = function(text, color){
    $scope.result2 = text;
    $scope.rescolor2 = color;
  }

  $scope.getResult = function(url) {
    $scope.isLoading1 = true;
    $scope.putMessage1('checking', 'orange');
    // get the URL from the input
    encoded = encodeURIComponent(encodeURIComponent(url));
    // fire the API request
    $http.get('/defoe/api/v1.0/' + encoded)
    .then(function(success) {
        $scope.isLoading1 = false;
        var res = success.data.isDefaced;
        $log.log(res);
        if(res == 'true'){
          $scope.putMessage1('yes', 'red');
        }else{
          $scope.putMessage1('no', 'green');
        }
      },
      function(error) {
        $scope.isLoading1 = false;
        $scope.putMessage1('bad url', 'orange');
        $log.log(error);
      });
    };
   $scope.reportUrl = function(url, status) {
    $scope.isLoading2 = true;
    $scope.putMessage2('reporting', 'orange');
    encoded = encodeURIComponent(encodeURIComponent(url));
    var defaced = (status == 'defaced');
    var data = {'url': encoded, 'isDefaced': defaced};
    $log.log(data);
    $http.post('/defoe/api/v1.0/report', data)
    .then(function(success) {
        $scope.isLoading2 = false;
        $scope.putMessage2('reported', 'green');
      },
      function(error) {
        $scope.isLoading2 = false;
        $scope.putMessage2('bad url', 'orange');
        $log.log(error);
      });
    };

}
]);
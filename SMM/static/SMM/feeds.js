var app = angular.module('FeedsApp', []);
app.config(function ($interpolateProvider) {
  $interpolateProvider.startSymbol('{$');
  $interpolateProvider.endSymbol('$}');
});
app.controller('FeedsController', ["$scope", "$http", "$interval", function ($scope, $http, $interval) {

  $scope.update_sentiment = function (sentiment) {
    $http.get('update_sentiment/', { params: { "post_id": $scope.post_id, "sentiment": sentiment } });
  };

  $interval(function () { $scope.resetAlertBadges(); }, 300000);

  $scope.resetAlertBadges = function () {
    $scope.badges = [];
    console.log('time')
    $http.get('display_feed_badge/').then(function (data) {
      angular.forEach(data.data, function (value, key) {
        var keyword = JSON.parse(value);
        $scope.badges.push(keyword.alert_badge_count);
      });
    });
  };

  $scope.loadFeedsAndBadges = function () {
    $scope.alerts = [];
    $scope.badges = [];
    console.log('time')
    $http.get('display_feed_badge/').then(function (data) {
      angular.forEach(data.data, function (value, key) {
        var keyword = JSON.parse(value);
        $scope.alerts.push(
          {
            "alert_id": keyword.alert_id,
            "alert_name": keyword.alert_name
          }
        );
        $scope.badges.push(keyword.alert_badge_count);
      });
    });
  };
  $scope.loadData = function (id) {
    var no_of_feeds = 10;
    if (id == $scope.kwd_ID) {
      console.log(no_of_feeds);
      no_of_feeds = no_of_feeds + $scope.feeds.length;
    } else {
      $scope.kwd_ID = id;
    }
    $scope.feeds = [];
    $http.get('display_feed_angular/', { params: { "alert_id": id, "no_of_feeds": no_of_feeds } }).then(function (data) {

      if (data.data.length >= $scope.feeds.length) {
        angular.forEach(data.data, function (value, key) {
          var feed = JSON.parse(value);
          $scope.feeds.push(
            {
              "ID": feed.ID,
              "StatusID": feed.statusID,
              "Content": feed.Content,
              "EscapedContent": feed.EscapedContent,
              "Sentiment": feed.Sentiment,
              "DisplayPicture": feed.DisplayPicture,
              "DisplayName": feed.DisplayName,
              "CreatedAt": feed.CreatedAt,
              "UserID": feed.UserID
            }
          );
        });
      }
      if (no_of_feeds == 10) {
        $('#scroll').scrollTop(0);
        scrollTrack = 0;
        $scope.reply_click($scope.feeds[0])
      }
    });
  };
  $scope.reply_click = function (feed) {
    $scope.post_id = feed.ID;
    $("#display_name").text(feed.DisplayName);
    $("#created_at").text(feed.CreatedAt);
    $("#text").text(feed.EscapedContent);
    $('#display_picture').attr('src', feed.DisplayPicture);
    $('#display_picture_link').attr('href', "https://twitter.com/" + feed.DisplayName);
    $("#post_url").attr('href', "https://twitter.com/" + name + "/status/" + feed.StatusID);
    $("#post_url").html("https://twitter.com/" + name + "/status/" + feed.StatusID);
    if (feed.Sentiment == '1') {
      $('#dropdownEmotionButton').attr('src', '/static/images/happy.png');
    } else if (feed.Sentiment == '0') {
      $('#dropdownEmotionButton').attr('src', '/static/images/emotion.svg');
    }
    else {
      $('#dropdownEmotionButton').attr('src', '/static/images/sad.svg');
    }
  };

  angular.element(document.querySelector('#scroll')).bind('scroll', function () {
    if ($('#scroll').scrollTop() + $('#scroll').innerHeight() >= $('#scroll')[0].scrollHeight) {
      scrollTrack++;
      if (scrollTrack == 1) {
        $scope.loadData($scope.kwd_ID)
        console.log("here")
      } else {
        scrollTrack = 0;
      }
    }
  })
  //initial load
  $scope.feeds = [];
  $scope.post_id = 0;
  $scope.loadData('init');
  $scope.loadFeedsAndBadges();
  var scrollTrack = 0;

}]);

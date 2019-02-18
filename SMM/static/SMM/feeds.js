var app = angular.module('FeedsApp', []);

app.config(function ($interpolateProvider) {
  $interpolateProvider.startSymbol('{$');
  $interpolateProvider.endSymbol('$}');
});

app.directive('scrollFeeds', function () {
  return function (scope, element, attributes) {
    setTimeout(function () {
      if (scope.$eval(attributes.scrollFeeds)) {
        //      alert(element[0].outerHeight())
        //        $('#scroll').scrollTo(element[0].offsetTop,500,1000);
        $('#scroll').scrollTo(element[0].offsetTop + $('#scroll').scrollHeight, 500, 1000);
      }
    });
  }
});
app.controller('FeedsController', ["$scope", "$http", "$interval", function ($scope, $http, $interval) {

  $scope.update_sentiment = function (sentiment) {
    $http.get('update_sentiment/', {
      params: {
        "post_id": $scope.post_id,
        "sentiment": sentiment
      }
    }).then(function (data) {
      if (JSON.parse(data.data).is_updated == "True") {
        var feedIndex = $scope.feeds.findIndex(feed => {
          return feed.ID === $scope.post_id
        });
        $scope.feeds[feedIndex].Sentiment = sentiment;
      }
    });
  };

  $interval(function () {
    $scope.resetAlertBadges();
  }, 3000);

  $scope.resetAlertBadges = function () {
    $http.get('display_feed_badge/').then(function (data) {
      var count = 0;
      angular.forEach(data.data, function (value, key) {
        var keyword = JSON.parse(value);
        $scope.badges[count] = keyword.alert_badge_count;
        count++;
      });
    });
  };

  $scope.getKeywordBgColor = function (kwd_ID) {
    switch(kwd_ID){
        case $scope.kwd_ID: return '#c6e4c1';
        default: return 'white';
    }
    };

  $scope.loadFeedsAndBadges = function () {
    $http.get('display_feed_badge/').then(function (data) {
      angular.forEach(data.data, function (value, key) {
        var keyword = JSON.parse(value);
        $scope.alerts.push({
          "alert_id": keyword.alert_id,
          "alert_name": keyword.alert_name
        });
        $scope.badges.push(keyword.alert_badge_count);
        $scope.kwd_ID=$scope.alerts[0].alert_id;
      });
    });
  };
  $scope.loadData = function (id, index, caller) {
    var no_of_feeds = 10;
    $scope.kwd_index = index;
    $scope.kwd_ID = id;

    if (caller === 'scroll') {
      no_of_feeds = no_of_feeds + $scope.feeds.length;
    } else {
      $scope.feeds = [];
    }

    $http.get('display_feed_angular/', {
      params: {
        "alert_id": id,
        "no_of_feeds": no_of_feeds
      }
    }).then(function (data) {

      if (data.data.length >= $scope.feeds.length) {
        next_feeds = data.data.splice(0, no_of_feeds - 10)
        console.log(next_feeds)
        angular.forEach(data.data, function (value, key) {
          var feed = JSON.parse(value);
          $scope.feeds.push({
            "ID": feed.ID,
            "StatusID": feed.statusID,
            "Content": feed.Content,
            "EscapedContent": feed.EscapedContent,
            "Sentiment": feed.Sentiment,
            "DisplayPicture": feed.DisplayPicture,
            "DisplayName": feed.DisplayName,
            "CreatedAt": feed.CreatedAt,
            "UserID": feed.UserID
          });
        });
        $scope.scrolledFeedID = $scope.feeds[no_of_feeds - 10].ID;
      }
      scrollTrack = 0;
      if (no_of_feeds == 10) {
        $scope.reply_click($scope.feeds[0])
      }
    });
  };
  $scope.reply_click = function (feed) {
    $scope.post_id = feed.ID;
    $("#display_name").text(feed.DisplayName);
    $("#created_at").text(feed.CreatedAt);
    $("#text").text(feed.Content);
    $('#display_picture').attr('src', feed.DisplayPicture);
    $('#display_picture_link').attr('href', "https://twitter.com/" + feed.DisplayName);
    $("#post_url").attr('href', "https://twitter.com/" + name + "/status/" + feed.StatusID);
    $("#post_url").html("https://twitter.com/" + name + "/status/" + feed.StatusID);
    if (feed.Sentiment == '1') {
      $('#dropdownEmotionButton').attr('src', '/static/images/happy.png');
    } else if (feed.Sentiment == '-1') {
      $('#dropdownEmotionButton').attr('src', '/static/images/emotion.svg');
    } else {

      $('#dropdownEmotionButton').attr('src', '/static/images/sad.svg');
    }

  };

  angular.element(document.querySelector('#scroll')).bind('scroll', function () {
    if ($('#scroll').scrollTop() + $('#scroll').innerHeight() >= $('#scroll')[0].scrollHeight) {
      scrollTrack++;
      if (scrollTrack == 1 && $scope.feeds.length < ($scope.badges[$scope.kwd_index])) {
        $scope.loadData($scope.kwd_ID, $scope.kwd_index, 'scroll')
      } else {
        scrollTrack = 0;
      }
    }
  });

  //initial load
  $scope.feeds = [];
  $scope.kwd_ID = 'init';
  $scope.kwd_index = 0;
  $scope.scrolledFeedID = 0;
  $scope.alerts = [];
  $scope.post_id = 0;
  $scope.badges = [];
  $scope.loadData($scope.kwd_ID, 0);
  $scope.loadFeedsAndBadges();
  var scrollTrack = 0;

  $scope.scrollFeedsDivToAFeed = function (feed_no) {
    alert(feed_no)
    //  var element=$("#feed_"+feed_no);
    var element = angular.element(document.querySelector('#scroll'));
    $('#scroll').scrollTo("#feed_" + feed_no); //all divs w/class pane
    alert(element[0].offsetTop)
    $('#scroll').animate({
      scrollTop: element[0].offsetTop
    }, 200);
  };

}]);

$(document).ready(function () {
  // executes when HTML-Document is loaded and DOM is ready
  $('#scroll').css({
    'height': $(window).height() - $('#dashboardNav').outerHeight() - 10 + 'px'
  });
  $('#scroll1').css({
    'height': $(window).height() - $('#dashboardNav').height() - 100 + 'px'
  });

});
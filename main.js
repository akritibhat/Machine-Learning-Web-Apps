$(document).ready(function() {
  changeCurrentSong("hi");
  changeNextSongs("song", "song", "song", "song", "song");
  changeNextAmounts(0, 5, 6, 7, 9);
  var json = serializeJson('{"totalRaised": ["amount", 0], "current": [{"song": "name"}], "nextOne": [{"song": "verylongsongnameblahblahblahblahblahblah","amount": 0}],"nextTwo": [{"song": "name","amount": 0}],"nextThree": [{"song": "name","amount": 0}],"nextFour": [{"song": "name","amount": 0}],"nextFive": [{"song": "name","amount": 0}]}');
  update(json);
});
function changeCurrentSong(song) {
  $("#currentSong").html(song);
}

setInterval(function(){console.log("update")}, 5000);

function changeNextSongs(song1, song2, song3, song4, song5) {
  $("#nextSongOne").html(song1);
  $("#nextSongTwo").html(song2);
  $("#nextSongThree").html(song3);
  $("#nextSongFour").html(song4);
  $("#nextSongFive").html(song5);
}

function changeNextAmounts(amount1, amount2, amount3, amount4, amount5) {
  $("#nextSongOneAmount").html("$" + amount1);
  $("#nextSongTwoAmount").html("$" + amount2);
  $("#nextSongThreeAmount").html("$" + amount3);
  $("#nextSongFourAmount").html("$" + amount4);
  $("#nextSongFiveAmount").html("$" + amount5);
}

function changeTotalAmount(totalAmount) {

}

function serializeJson(json) {
  var json = jQuery.parseJSON(json);
  return json;
}

function update(json) {
  changeCurrentSong(json.current[0].song);
  changeNextSongs(json.nextOne[0].song, json.nextTwo[0].song, json.nextThree[0].song, json.nextFour[0].song, json.nextFive[0].song);
  changeNextAmounts(json.nextOne[0].amount, json.nextTwo[0].amount, json.nextThree[0].amount, json.nextFour[0].amount, json.nextFive[0].amount);
}

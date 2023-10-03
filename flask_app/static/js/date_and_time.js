//  https://www.plus2net.com/javascript_tutorial/clock.php
// https://www.w3schools.com/jsref/jsref_gethours.asp

function prefixZero(i) {
  if (i < 10) {i = "0" + i}
  return i;
}

function formatDateAndTime() {
    // updated vars to resemble unix time formats
    x = new Date()
    Y = x.getFullYear();
    m = prefixZero(x.getMonth()+1);
    d = prefixZero(x.getDate());
    H = prefixZero(x.getHours());
    M = prefixZero(x.getMinutes());
    S = prefixZero(x.getSeconds());
    farmatted_d_and_t = Y + "/" +  m + "/" + d + " - " + H + ":" +  M + ":" +  S;
    document.getElementById('date_and_time').innerHTML = farmatted_d_and_t;
    displayDateAndTime();
 }

function displayDateAndTime(){
    refresh=1000; // Refresh rate in milli seconds
    mytime=setTimeout('formatDateAndTime()',refresh)
}

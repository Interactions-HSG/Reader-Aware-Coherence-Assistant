//const toggleSidebar = document.getElementById('toggleSidebar');
//const sidebar = document.getElementById('sidebar');
const writingZone = document.getElementById("writingZone");
const personalIDs = document.getElementById("personal_ids");
const Recommendation = document.getElementById("Recommendation");

function colorCodingClauses(dictObj) {
  //  dictObj should have at least those 3 keys: 'scores', 'ranges', 'texts'
  //  FF0000(0),00FF00(1) //

  //1. to test if we have more than one value for the scores
  if (dictObj.scores.length == 0) {
    dictObj.nScores = [];
    dictObj.cScores = [];
    return dictObj;
  }
  if (dictObj.scores.length == 1) {
    minScore = dictObj.scores[0][0];
    maxScore = dictObj.scores[0][1];
    normalizedScores = [1 * (minScore != 0)];
  }

  //2. Normalize the scores (each score has its own range)
  normalizedScores = dictObj.scores.map(
    (s, idx) =>
      (s - dictObj.ranges[idx][0]) /
      (dictObj.ranges[idx][1] - dictObj.ranges[idx][0])
  );

  //3. color-code to each normalized value
  RED = 0xff0000;
  GREEN = 0x00ff00;
  colorCodedScores = normalizedScores.map(
    (n) => (RED * (1 - (n > 0.5))) | (GREEN * (n > 0.5))
  );

  //4. put the normalized and colored scores back into the dictionary
  dictObj.nScores = normalizedScores;
  dictObj.cScores = colorCodedScores;
  return dictObj;
}

function dNh(d, N) {
  /*
   * Transform a decimal value into an hexadecimal value as a *STRING*.
   * IN: d - decimal value
   * IN: N - length of the ouput string (add leading zeros if too short)
   * OUT: s - N-length string representing the hexadecimal value of d
   */
  var s = (+d).toString(16);
  n = s.length;
  while (n < N) {
    s = "0" + s;
    n = s.length;
  }
  return s;
}

// Add an event listener to the form submission
document
  .getElementById("coherenceForm")
  .addEventListener("submit", function (event) {
    event.preventDefault(); // Prevent the default form submission behavior

    const text = writingZone.value.trim();
    const ids = personalIDs.value;
    if (text && ids) {
      // Send a POST request to the Flask server

      fetch("/labeling-srv", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ txt: text, ids: ids }),
      })
        .then((response) => {
          if (!response.ok) {
            errMsg = "Network response was not ok";
            Recommendation.innerHTML = errMsg;
            throw new Error(errMsg);
          }
          print(response);
          return response.json();
        })
        .then((data) => {
          //console.log(data);

          dictObj = colorCodingClauses(data);
          //console.log(dictObj.cScores);
          
          // Update the Recommendation section with the server's response
          Recommendation.innerHTML = "";
          for (idx = 0; idx < dictObj.texts.length; idx++) {
            t = dictObj.texts[idx];
            c = dictObj.cScores[idx];
            htmlText = '<span style="color:#' + dNh(c, 6) + '">' + t + "<span>";
            Recommendation.innerHTML += htmlText;
          } //span is a container you can add CSS

        })
        .catch((error) => {
          //console.error("Error:", error);
          Recommendation.innerHTML = "An error occurred: " + error.message; // Display a more detailed error message
        });
    }
  });

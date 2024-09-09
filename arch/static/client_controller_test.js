// Add an event listener to the form submission 
//define diff objects
const selected_test = document.getElementById('selected_test');
const response_data = document.getElementById('response');
const txt_input = document.getElementById('txt_input')
const nb_words = document.getElementById('nb_of_words')
const txt_input2 = document.getElementById('txt_input2')
const metric = document.getElementById('metric');
const scale = document.getElementById('scale');

const provider = document.getElementById('provider');

const personal_ids = document.getElementById('personal_ids');


document
  .getElementById("test_form")
  .addEventListener("submit", function (event) {
    event.preventDefault(); // Prevent the default form submission behavior

    const test_name = selected_test.value.trim(); 
    if (test_name) {
      switch(test_name.toLowerCase()){
        case 'labeling':
          // Required to keep the rest of the code compatible with previous
          // versions of the code.
          const Recommendation = txt_input2;

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
                console.log(data);
                dictObj = colorCodingClauses(data);
                console.log(dictObj.cScores);
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
                console.error("Error:", error);
                //Recommendation.textContent = "An error occurred: " + error.message; // Display a more detailed error message
              });
          }
          break;
        default:
          // Send a POST request to the Flask server
          fetch("/test-srv", {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
            },
            body: JSON.stringify({ selected_test: test_name, //define all params
              param1: txt_input.value, 
              param2: nb_words.value,
              param3: txt_input2.value,
              metric: metric.value, 
              scale: scale.value,
              provider: provider.value,
              rp_id: personal_ids.value
            }), 
          })
            .then((response) => {
              if (!response.ok) {
                throw new Error("Network response was not ok");
              }          
              return response.json();
            })
            .then((data) => {
              // Update the Recommendation section with the server's response
              //console.log(data);
              response_data.innerHTML =
                data.text || "No suggestions received."; // Check if data.suggestions is defined
            })
            .catch((error) => {
              console.error("Error:", error);
              //Recommendation.textContent = "An error occurred: " + error.message; // Display a more detailed error message
            });
      }
    }
  });











/******************************************************************************
 * Function for LABELING
 */
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
  
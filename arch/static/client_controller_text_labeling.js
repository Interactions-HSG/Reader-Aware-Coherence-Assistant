//const toggleSidebar = document.getElementById('toggleSidebar');
//const sidebar = document.getElementById('sidebar');
const writingZone = document.getElementById("writingZone");
const personalIDs = document.getElementById("personal_ids");
const Recommendation = document.getElementById("Recommendation");

/*toggleSidebar.addEventListener('click', () => {
    sidebar.classList.toggle('hidden');
    });*/

//small function by th.s
// async function logFetchResponse(){
//response = await fetch('http');
//console.log(response);
//}

//// Define a variable to keep track of the selected profile
//let selectedProfile = null;

// Event listener for profile selection
/*document.querySelectorAll('.profile-button').forEach((button) => {
      button.addEventListener('click', () => {
        selectedProfile = button.getAttribute('data-profile');
        // You can add visual cues or styling to indicate the selected profile, if needed
      });
    });*/

//Event listener for fetching
// document.getElementById("fetchText").addEventListener("click", () => {
//   personal_id = document.getElementById("personal_ids");
//   //we want to get a list of personal_ids
//   fetch("/fetchGS", {
//     method: "POST",
//     headers: {
//       "Content-Type": "application/json",
//     },
//     body: JSON.stringify({ personal_id: personal_id.value }),
//   })
//     .then((response) => {
//       if (!response.ok) {
//         throw new Error("Network response was not ok");
//       }
//       return response.text();
//     })
//     .then((data) => {
//       console.log(data);
//       abstract.value = data; //show the abstract
//     })
//     .catch((error) => {
//       console.error("Error:", error);
//       //Recommendation.textContent = "An error occurred: " + error.message; // Display a more detailed error message
//     });
// });

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
    if (text && selectedProfile) {
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

          //Recommendation.textContent =
          //dictObj.texts || "No suggestions received."; // Check if data.suggestions is defined
        })
        .catch((error) => {
          console.error("Error:", error);
          //Recommendation.textContent = "An error occurred: " + error.message; // Display a more detailed error message
        });
    }
  });

/*document.addEventListener('click', (event) => {
    if (!sidebar.contains(event.target) && !toggleSidebar.contains(event.target)) {
        sidebar.classList.add('hidden');
    }
    });*/

// Event listener for profile selection
/*document.querySelectorAll('.profile-button').forEach((button) => {
      button.addEventListener('click', () => {
        // Remove "selected" class from all buttons
        document.querySelectorAll('.profile-button').forEach((btn) => {
          btn.classList.remove('selected');
        });

        // Add "selected" class to the clicked button
        button.classList.add('selected');

        selectedProfile = button.getAttribute('data-profile');
    
      document.getElementById('personal_ids').value = button.getAttribute('data-personal_id') //when click, the id appears
      });
    });*/

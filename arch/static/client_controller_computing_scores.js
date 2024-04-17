const the_selected_test = 'get_score';
//const toggleSidebar = document.getElementById('toggleSidebar');
//const sidebar = document.getElementById('sidebar');
const writingZone = document.getElementById("writingZone");
const abstract = document.getElementById("abstract");
//const recommendZone = document.getElementById('recommendZone');
const Recommendation = document.getElementById("Recommendation");

function colorCodingClauses(dictObj){
//  FF0000(0),00FF00(1) //
//1. to test if we have more than One value for the scores
if(dictObj.scores.length == 0){
dictObj.nScores=[]
dictObj.cScores=[]
return dictObj
}
if (dictObj.scores.length ==1){
  minScore=dictObj.scores[0]
  maxScore=dictObj.scores[0]
  normalizedScore = [1*(minScore !=0)]
}
else{
  //2. find the min and max in the list of scores
minScore = Math.min(...dictObj.scores)
maxScore = Math.max(...dictObj.scores)
if (minScore == maxScore){
  normalizedScore = (dictObj.scores).map(s=>1*(minScore !=0))
}
else{
//3. normalized the score bt 0 and 1(if you want the precision *256)
normalizedScore = (dictObj.scores).map(s=>(s-minScore)/(maxScore-minScore)) //2:03 change the way: function of all scores 
}
}
//transform the json string in two: one array with a list of clauses, another with scores
//dictObj = JSON.parse(jsonDict)

//4. color-code to each normalized value(deduct the value from the red and add to the green)
RED = 0xFF0000
GREEN = 0x00FF00
colorCodedScore = normalizedScore.map(n=>
  (RED*(1-n))|(GREEN*n))
//console.log(colorCodedScore)
//console.log(normalizedScore)
//5. return the result
dictObj.nScores = normalizedScore
dictObj.cScores = colorCodedScore
return dictObj

//0xFF0000 = 0xF00000 | 0x0F00000
//console.log(jsonDict)
}

//to predict the score, the behavior of the fuction; the format we dont expect
//each time you ask for a score, you get a score 0318

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
document.getElementById("fetchText").addEventListener("click", () => {
  personal_id = document.getElementById("personal_ids");
  //we want to get a list of personal_ids
  fetch("/test-srv", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ 
      selected_test: 'fetchGS', //hardcoded the selected_test
      personal_id: personal_id.value }), 
  })
    .then((response) => {
      if (!response.ok) {
        throw new Error("Network response was not ok");
      }
      return response.text();
    })
    .then((data) => {
      console.log(data);
      abstract.value = data.text; //show the abstract
    })
    .catch((error) => {
      console.error("Error:", error);
      //Recommendation.textContent = "An error occurred: " + error.message; // Display a more detailed error message
    });
});

// Add an event listener to the form submission
document
  .getElementById("coherenceForm")
  .addEventListener("submit", function (event) {
    event.preventDefault(); // Prevent the default form submission behavior

    const text = writingZone.value.trim();
    if (text && selectedProfile) {
      // Placeholder for coherence score logic
      const coherenceScore = "Coherence Score: 7/10";
      recommendZone.innerHTML = `<span class="coherence-icon mr-2">😂</span>Based on the selected reader's profile, ${coherenceScore}`;

      // Send a POST request to the Flask server

      fetch("/test-srv", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ 
          selected_test: the_selected_test,
          txt: text, abstract: abstract.value }), // Send the user's input text // and the profile
      })
        .then((response) => {
          if (!response.ok) {
            throw new Error("Network response was not ok");
          }
          jsonResponse = response.json()
          //console.log(jsonResponse)
          return jsonResponse;
        })
        .then((data) => {
          //console.log(data)
          dictObj = colorCodingClauses(data.dict)
          console.log(dictObj.cScores)
          // Update the Recommendation section with the server's response
          Recommendation.textContent =
            data.combinedOutput || "No suggestions received."; // Check if data.suggestions is defined
        })
        .catch((error) => {
          console.error("Error:", error);
          //Recommendation.textContent = "An error occurred: " + error.message; // Display a more detailed error message
        });

      // Fetch Simon's merged abstracts when Simon profile is selected
      if (selectedProfile === "Simon") {
        fetch("/merged-abstracts/simon")
          .then((response) => {
            if (!response.ok) {
              throw new Error("Network response was not ok");
            }
            return response.text();
          })
          .then((data) => {
            // Update the Recommendation section with Simon's merged abstracts
            // Recommendation.textContent = data || "No merged abstracts available for Simon.";
          })
          .catch((error) => {
            console.error("Error:", error);
            Recommendation.textContent = "An error occurred: " + error.message;
          });
      }
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

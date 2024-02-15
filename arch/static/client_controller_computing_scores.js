//const toggleSidebar = document.getElementById('toggleSidebar');
//const sidebar = document.getElementById('sidebar');
const writingZone = document.getElementById("writingZone");
const abstract = document.getElementById("abstract");
//const recommendZone = document.getElementById('recommendZone');
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
document.getElementById("fetchText").addEventListener("click", () => {
  personal_id = document.getElementById("personal_ids");
  //we want to get a list of personal_ids
  fetch("/fetchGS", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ personal_id: personal_id.value }), 
  })
    .then((response) => {
      if (!response.ok) {
        throw new Error("Network response was not ok");
      }
      return response.text();
    })
    .then((data) => {
      console.log(data);
      abstract.value = data; //show the abstract
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

      fetch("/get_score", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ txt: text, abstract: abstract.value }), // Send the user's input text // and the profile
      })
        .then((response) => {
          if (!response.ok) {
            throw new Error("Network response was not ok");
          }
          return response.json();
        })
        .then((data) => {
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

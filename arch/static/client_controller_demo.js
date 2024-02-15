// Add an event listener to the form submission
const selected_demo = document.getElementById('selected_demo');
const response_data = document.getElementById('response');
const txt_input = document.getElementById('txt_input')
const nb_words = document.getElementById('nb_of_words')


document
  .getElementById("demo_form")
  .addEventListener("submit", function (event) {
    event.preventDefault(); // Prevent the default form submission behavior

    const demo_name = selected_demo.value.trim(); 
    if (demo_name) {
      
      // Send a POST request to the Flask server

      fetch("/demo-srv", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ selected_demo: demo_name,
          param1: txt_input.value, 
          param2: nb_words.value }), // Send the user's input text // and the profile
      })
        .then((response) => {
          if (!response.ok) {
            throw new Error("Network response was not ok");
          }          
          return response.json();
        })
        .then((data) => {
          // Update the Recommendation section with the server's response
          // console.log(data);
          response_data.innerHTML =
            data.gptOutput || "No suggestions received."; // Check if data.suggestions is defined
        })
        .catch((error) => {
          console.error("Error:", error);
          //Recommendation.textContent = "An error occurred: " + error.message; // Display a more detailed error message
        });

    }
  });
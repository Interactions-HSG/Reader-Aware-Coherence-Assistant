// Add an event listener to the form submission 
//define diff objects
const selected_demo = document.getElementById('selected_demo');
const response_data = document.getElementById('response');
const txt_input = document.getElementById('txt_input')
const nb_words = document.getElementById('nb_of_words')
const txt_input2 = document.getElementById('txt_input2')
const metric = document.getElementById('metric');
const scale = document.getElementById('scale');


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
        body: JSON.stringify({ selected_demo: demo_name, //define all params
          param1: txt_input.value, 
          param2: nb_words.value,
          param3: txt_input2.value,
          metric: metric.value, 
          scale: scale.value
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
          // console.log(data);
          response_data.innerHTML =
            data.text || "No suggestions received."; // Check if data.suggestions is defined
        })
        .catch((error) => {
          console.error("Error:", error);
          //Recommendation.textContent = "An error occurred: " + error.message; // Display a more detailed error message
        });

    }
  });
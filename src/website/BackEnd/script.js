document.addEventListener("DOMContentLoaded", function () {
  const videoInput = document.getElementById("videoInput");
  const videoPlayer = document.getElementById("videoPlayer");
  const processButton = document.getElementById("processButton");
  const resultDiv = document.getElementById("result");

  let selectedFile = null;  // Store the file globally

  videoInput.addEventListener("change", function (event) {
    event.preventDefault();  // Stop page reload

    selectedFile = event.target.files[0];  // Store the selected file globally

    if (selectedFile) {
      const url = URL.createObjectURL(selectedFile);
      videoPlayer.src = url;
      processButton.disabled = false;
    }
  });

  processButton.addEventListener("click", function (event) {
    event.preventDefault();  // Prevent unexpected form submission

    if (!selectedFile) {
      alert("Veuillez sélectionner un fichier vidéo.");
      return;
    }

    // Show loading indicator
    if (resultDiv) {
      resultDiv.innerHTML = "Processing video, please wait...";
    }
    
    // Disable process button while processing
    processButton.disabled = true;

    const formData = new FormData();
    formData.append("file", selectedFile);

    fetch("http://127.0.0.1:5000/upload", {
      method: "POST",
      body: formData // Correct way to send file data
    })
      .then(response => {
        // Check if the response is ok
        if (!response.ok) {
          throw new Error(`Server responded with status: ${response.status}`);
        }
        return response.json();
      })
      .then(data => {
        console.log("Server Response:", data);
        
        // Display the results
        if (resultDiv) {
          resultDiv.innerHTML = `
            <h3>Analysis Results:</h3>
            <p>Step Count: ${data.step_count}</p>
            <p>Peak Indices: ${data.peak_indices ? data.peak_indices.length : 0} points detected</p>
            <p>Distances: ${data.distances ? data.distances.length : 0} measurements</p>
          `;
        }
        
        // Re-enable the process button
        processButton.disabled = false;
      })
      .catch(error => {
        console.error("Error:", error);
        
        // Show error message
        if (resultDiv) {
          resultDiv.innerHTML = `<p style="color: red;">Error: ${error.message}</p>`;
        }
        
        // Re-enable the process button
        processButton.disabled = false;
      });
  });
});
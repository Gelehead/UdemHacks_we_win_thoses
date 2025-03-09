document.addEventListener("DOMContentLoaded", function () {
  const videoInput = document.getElementById("videoInput");
  const videoPlayer = document.getElementById("videoPlayer");
  const processButton = document.getElementById("processButton");
  const resultDiv = document.getElementById("result");
  const animationDiv = document.getElementById("animation");

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
      resultDiv.innerHTML = "<p>Processing video, please wait...</p>";
    }
    
    // Clear animation div
    if (animationDiv) {
      animationDiv.innerHTML = "";
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
          let resultHTML = `<h3>Analysis Results:</h3>`;
          
          if (data.error) {
            resultHTML += `<p class="error">Error: ${data.error}</p>`;
          } else {
            resultHTML += `
              <p><strong>Step Count:</strong> ${data.step_count}</p>
              <p><strong>Peak Indices:</strong> ${data.peak_indices ? data.peak_indices.length : 0} points detected</p>
              <p><strong>Distances:</strong> ${data.distances ? data.distances.length : 0} measurements</p>
            `;
          }
          
          resultDiv.innerHTML = resultHTML;
        }
        
        // Display the animation if available
        if (animationDiv && data.animation_url) {
          const baseUrl = "http://127.0.0.1:5000";
          const animationUrl = baseUrl + data.animation_url;
          
          animationDiv.innerHTML = `
            <h3>Animation Output:</h3>
            <video id="animationPlayer" controls width="640" height="480">
              <source src="${animationUrl}" type="video/mp4">
              Your browser does not support the video tag.
            </video>
            <p>
              <a href="${animationUrl}" download class="download-btn">Download Animation</a>
            </p>
          `;
          
          // Play the animation automatically
          const animationPlayer = document.getElementById("animationPlayer");
          if (animationPlayer) {
            animationPlayer.play().catch(e => console.log("Auto-play prevented:", e));
          }
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
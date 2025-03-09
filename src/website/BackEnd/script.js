document.addEventListener("DOMContentLoaded", function () {
  const videoInput = document.getElementById("videoInput");
  const videoPlayer = document.getElementById("videoPlayer");
  const processButton = document.getElementById("processButton");
  const resultDiv = document.getElementById("result");
  const animationDiv = document.getElementById("animation");
  const analysisSections = document.getElementById("analysis-sections");
  
  // Create visualizer instance
  const visualizer = new RunningAnalyticsVisualizer();
  visualizer.init('chart-container', 'video-comparison');
  
  // Function to show analysis sections
  const showAnalysisSections = () => {
    console.log("Showing analysis sections");
    if (analysisSections) {
      analysisSections.style.display = "block";
    } else {
      console.error("Analysis sections element not found");
    }
  };

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
        
        // Show analysis sections FIRST before attempting to render content
        showAnalysisSections();
        
        // Process data for visualization - add safety checks
        if (data && data.peak_indices && data.distances) {
          console.log("Loading data for visualization");
          // Load the data for visualization
          visualizer.loadData(data);
          
          // Create the distance chart
          console.log("Creating distance chart");
          visualizer.createDistanceChart();
        } else {
          console.error("Missing required data for visualization", data);
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
        
        // Set up video comparison
        if (data.animation_path) {
          // Extract the filename from the animation path
          const pathParts = data.animation_path.split('\\');
          const filename = pathParts[pathParts.length - 1];
          const baseFilename = filename.replace('_animation.mp4', '');
          
          console.log("Setting up video comparison");
          // Set up the paths for the original and processed videos
          const originalVideoPath = URL.createObjectURL(selectedFile);
          const processedVideoPath = `../../../out/animations/${filename}`;
          
          visualizer.setupVideoComparison(originalVideoPath, processedVideoPath);
        }
        
        // Re-enable the process button
        processButton.disabled = false;
      })
      .catch(error => {
        console.error("Error:", error);
        
        // Show error message
        if (resultDiv) {
          resultDiv.innerHTML = `<p style="color: red;">Error: ${error.message}</p>
            <p>Using fallback sample data for demonstration.</p>`;
        }
        
        // Use fallback sample data from paste.txt
        const fallbackData = {
          "step_count": 17,
          "peak_indices": [3, 9, 19, 32, 44, 57, 69, 80, 93, 105, 117, 129, 141, 151, 154, 166, 177],
          "distances": [0.6062727257883002, 0.6324852060879529, 0.63891018378206, 0.6568997131118386,
            0.6430783363437111, 0.6696965921844427, 0.7232203749372823, 0.7446738107837908,
            0.7582737739368184, 0.791042051258273, 0.7502847563335824, 0.6384770745002577,
            0.5759411018664783, 0.5170184605789105, 0.5019710325256868, 0.5589929245887881,
            0.6494647209998672, 0.7209868547313253, 0.7485998532705631, 0.7537991966211595,
            0.7202753458367771, 0.6813873452539486, 0.6567878074645278, 0.6821764660818999,
            0.7159142242178925, 0.8347942973515561, 0.9613891338383168, 1.0931660060292856,
            1.2255024679373927, 1.3641943542910162, 1.4071284164223155, 1.4194352158130288,
            1.422860625332954, 1.360998373513093, 1.2208082863204188, 1.0346533762567536],
          "animation_path": "../../../out/animations/thomasRunning2_animation.mp4"
        };
        
        // Show analysis sections despite the error
        showAnalysisSections();
        
        // Use fallback data for visualization
        visualizer.loadData(fallbackData);
        visualizer.createDistanceChart();
        
        // Set up video comparison with fallback if available
        if (selectedFile) {
          const originalVideoPath = URL.createObjectURL(selectedFile);
          const processedVideoPath = "../../../out/animations/thomasRunning2_animation.mp4";
          visualizer.setupVideoComparison(originalVideoPath, processedVideoPath);
        }
        
        // Re-enable the process button
        processButton.disabled = false;
      });
  });
  
  // Function to manually load provided JSON data
  window.loadProvidedData = function() {
    // Use the data from paste.txt
    const jsonData = {
      "step_count": 17,
      "peak_indices": [3, 9, 19, 32, 44, 57, 69, 80, 93, 105, 117, 129, 141, 151, 154, 166, 177],
      "distances": [
        0.6062727257883002, 0.6324852060879529, 0.63891018378206, 0.6568997131118386,
        0.6430783363437111, 0.6696965921844427, 0.7232203749372823, 0.7446738107837908,
        0.7582737739368184, 0.791042051258273, 0.7502847563335824, 0.6384770745002577,
        0.5759411018664783, 0.5170184605789105, 0.5019710325256868, 0.5589929245887881,
        0.6494647209998672, 0.7209868547313253, 0.7485998532705631, 0.7537991966211595,
        0.7202753458367771, 0.6813873452539486, 0.6567878074645278, 0.6821764660818999,
        0.7159142242178925, 0.8347942973515561, 0.9613891338383168, 1.0931660060292856,
        1.2255024679373927, 1.3641943542910162, 1.4071284164223155, 1.4194352158130288,
        1.422860625332954, 1.360998373513093, 1.2208082863204188, 1.0346533762567536,
        0.8196860098886928, 0.532086435095331, 0.31358930654812395, 0.32951930727117024,
        0.4388912503428456, 0.5587024688844195, 0.6511675433119086, 0.712627880293427,
        0.729492855779985, 0.7162079688451842, 0.6777883478704024, 0.6181209125651621,
        0.6168892805083444, 0.6607013684161425, 0.7417343542817548, 0.8835584465258952,
        1.080622023237634, 1.2791322098884894, 1.5337894323427812, 1.7694636829768757,
        1.920094031315623, 1.932894624026866, 1.8163178351930005, 1.5352318027265384,
        1.2503864815816144, 0.8834082080238951, 0.5454097726556064, 0.28619384403127446,
        0.2656836998739626, 0.3707131897192196, 0.47765900638468173, 0.5525942009383801,
        0.5884616246502655, 0.5950804138029068, 0.5821225664731783, 0.5710205283027879,
        0.6031884058500694, 0.732770169490261, 0.8784782508267682, 1.0312015847402531,
        1.1717033551804674, 1.274693312332169, 1.3464510049273672, 1.4490921407457644,
        1.5103420597019326, 1.4399692808195628, 1.298174093796991, 1.1069540645439042,
        0.8977438781704853, 0.6253850635559439, 0.4317528459220762
      ],
      "animation_path": "C:\\Users\\oscar\\OneDrive\\Escritorio\\Univ\\Code\\hackathons\\UdemHacks\\out\\animations\\thomasRunning2_animation.mp4"
    };
    
    // Load the data
    visualizer.loadData(jsonData);
    
    // Create the chart
    visualizer.createDistanceChart();
    
    // Set up the video comparison
    const originalVideoPath = "videos/thomasRunning2.mp4"; // Adjust to your actual path
    const processedVideoPath = "../../../out/animations/thomasRunning2_animation.mp4";
    
    visualizer.setupVideoComparison(originalVideoPath, processedVideoPath);
    
    // Update the result display
    if (resultDiv) {
      resultDiv.innerHTML = `
        <h3>Analysis Results:</h3>
        <p><strong>Step Count:</strong> ${jsonData.step_count}</p>
        <p><strong>Peak Indices:</strong> ${jsonData.peak_indices.length} points detected</p>
        <p><strong>Distances:</strong> ${jsonData.distances.length} measurements</p>
      `;
    }
  };
});
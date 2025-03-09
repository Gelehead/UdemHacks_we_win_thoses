document.addEventListener("DOMContentLoaded", function () {
  const videoInput = document.getElementById("videoInput");
  const videoPlayer = document.getElementById("videoPlayer");
  const processButton = document.getElementById("processButton");

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

    const formData = new FormData();
    formData.append("file", selectedFile);

    fetch("http://127.0.0.1:5000/upload", {
      method: "POST",
      body: formData, // Correct way to send file data
    })
      .then((response) => response.json())
      .then((data) => {
        console.log("Server Response:", data);
      })
      .catch((error) => {
        console.log("Error:", error);
      });
  });
});

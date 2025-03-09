document.addEventListener("DOMContentLoaded", function () {
  const videoInput = document.getElementById("videoInput");
  const videoPlayer = document.getElementById("videoPlayer");
  const processButton = document.getElementById("processButton");

  videoInput.addEventListener("change", function (event) {
    const file = event.target.files[0];
    let base64String = "";
    if (file) {
      const url = URL.createObjectURL(file);
      videoPlayer.src = url;
      processButton.disabled = false;
      const reader = new FileReader();
      reader.onloadend = function () {
        // Le résultat est une URL de données, on prend la partie après la virgule
        base64String = reader.result.split(",")[1];
        console.log(base64String); // Affiche la chaîne Base64
      };
    }
    a = fetch("http://127.0.0.1:5000", {
      method: "POST",
      body: JSON.stringify({ file: file }),
      headers: { "Content-Type": "multipart/form-data" },
    })
      .then((response) => response.json())
      .then((data) => console.log(data))
      .catch((error) => console.log(error));
  });

  processButton.addEventListener("click", function () {
    const file = videoInput.files[0];
    if (file) {
      alert("Lancement du script pour traiter la vidéo : " + file.name);
      // Ici, tu pourras appeler ton vrai script plus tard
    }
  });
});

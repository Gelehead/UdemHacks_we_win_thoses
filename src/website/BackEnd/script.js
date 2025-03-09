document.addEventListener("DOMContentLoaded", function () {
    const videoInput = document.getElementById("videoInput");
    const videoPlayer = document.getElementById("videoPlayer");
    const processButton = document.getElementById("processButton");

    videoInput.addEventListener("change", function (event) {
        const file = event.target.files[0];
        if (file) {
            const url = URL.createObjectURL(file);
            videoPlayer.src = url;
            processButton.disabled = false;
        }
    });

    processButton.addEventListener("click", function () {
        const file = videoInput.files[0];
        if (file) {
            alert("Lancement du script pour traiter la vidéo : " + file.name);
            // Ici, tu pourras appeler ton vrai script plus tard
        }
    });
});

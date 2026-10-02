/* =========================================
   SHADOW PLAYER
========================================= */

document.addEventListener("DOMContentLoaded", function () {

    const video = document.getElementById("shadowVideo");

    const playButton = document.getElementById("playButton");

    const backwardButton =
        document.getElementById("backwardButton");

    const forwardButton =
        document.getElementById("forwardButton");

    const muteButton =
        document.getElementById("muteButton");

    const volumeBar =
        document.getElementById("volumeBar");

    const progressBar =
        document.getElementById("progressBar");

    const timeDisplay =
        document.getElementById("timeDisplay");

    const speedSelect =
        document.getElementById("speedSelect");

    const fullscreenButton =
        document.getElementById("fullscreenButton");

    const videoMessage =
        document.getElementById("videoMessage");


    /* =========================================
       VERIFICATION
    ========================================== */

    if (!video) {
        console.error("SHADOW PLAYER : vidéo introuvable.");
        return;
    }


    /* =========================================
       FORMAT TEMPS
    ========================================== */

    function formatTime(seconds) {

        if (!Number.isFinite(seconds)) {
            return "00:00";
        }

        const hours =
            Math.floor(seconds / 3600);

        const minutes =
            Math.floor((seconds % 3600) / 60);

        const secs =
            Math.floor(seconds % 60);


        if (hours > 0) {

            return (
                String(hours).padStart(2, "0") +
                ":" +
                String(minutes).padStart(2, "0") +
                ":" +
                String(secs).padStart(2, "0")
            );

        }


        return (
            String(minutes).padStart(2, "0") +
            ":" +
            String(secs).padStart(2, "0")
        );
    }


    /* =========================================
       AFFICHER LE TEMPS
    ========================================== */

    function updateTime() {

        const current =
            video.currentTime || 0;

        const duration =
            video.duration || 0;

        timeDisplay.textContent =
            formatTime(current) +
            " / " +
            formatTime(duration);
    }


    /* =========================================
       PROGRESSION
    ========================================== */

    function updateProgress() {

        if (!video.duration) {
            progressBar.value = 0;
            return;
        }

        const percentage =
            (video.currentTime / video.duration) * 100;

        progressBar.value = percentage;
    }


    /* =========================================
       PLAY / PAUSE
    ========================================== */

    function togglePlay() {

        if (video.paused) {

            video.play()
                .catch(function (error) {

                    console.log(
                        "Lecture bloquée :",
                        error
                    );

                });

        } else {

            video.pause();

        }
    }


    playButton.addEventListener(
        "click",
        togglePlay
    );


    video.addEventListener(
        "play",
        function () {

            playButton.textContent = "❚❚";

            if (videoMessage) {
                videoMessage.classList.add("hidden");
            }

        }
    );


    video.addEventListener(
        "pause",
        function () {

            playButton.textContent = "▶";

        }
    );


    /* =========================================
       -10 SECONDES
    ========================================== */

    backwardButton.addEventListener(
        "click",
        function () {

            video.currentTime =
                Math.max(
                    0,
                    video.currentTime - 10
                );

        }
    );


    /* =========================================
       +10 SECONDES
    ========================================== */

    forwardButton.addEventListener(
        "click",
        function () {

            video.currentTime =
                Math.min(
                    video.duration || Infinity,
                    video.currentTime + 10
                );

        }
    );


    /* =========================================
       VOLUME
    ========================================== */

    volumeBar.addEventListener(
        "input",
        function () {

            video.volume =
                Number(volumeBar.value);

            video.muted =
                video.volume === 0;

            updateMuteButton();

        }
    );


    /* =========================================
       MUET
    ========================================== */

    function updateMuteButton() {

        if (
            video.muted ||
            video.volume === 0
        ) {

            muteButton.textContent = "🔇";

        } else if (video.volume < 0.5) {

            muteButton.textContent = "🔉";

        } else {

            muteButton.textContent = "🔊";

        }
    }


    muteButton.addEventListener(
        "click",
        function () {

            video.muted =
                !video.muted;

            updateMuteButton();

        }
    );


    /* =========================================
       BARRE DE PROGRESSION
    ========================================== */

    progressBar.addEventListener(
        "input",
        function () {

            if (!video.duration) {
                return;
            }

            const percentage =
                Number(progressBar.value);

            video.currentTime =
                (percentage / 100) *
                video.duration;

        }
    );


    /* =========================================
       VITESSE
    ========================================== */

    speedSelect.addEventListener(
        "change",
        function () {

            video.playbackRate =
                Number(speedSelect.value);

        }
    );


    /* =========================================
       PLEIN ECRAN
    ========================================== */

    fullscreenButton.addEventListener(
        "click",
        function () {

            const player =
                document.querySelector(
                    ".video-wrapper"
                );


            if (
                document.fullscreenElement
            ) {

                document.exitFullscreen();

                return;
            }


            if (
                player.requestFullscreen
            ) {

                player.requestFullscreen();

            } else if (
                video.webkitEnterFullscreen
            ) {

                video.webkitEnterFullscreen();

            }

        }
    );


    /* =========================================
       EVENEMENTS VIDEO
    ========================================== */

    video.addEventListener(
        "timeupdate",
        function () {

            updateProgress();

            updateTime();

        }
    );


    video.addEventListener(
        "loadedmetadata",
        function () {

            updateTime();

            updateProgress();

            if (videoMessage) {
                videoMessage.classList.add("hidden");
            }

        }
    );


    video.addEventListener(
        "canplay",
        function () {

            if (videoMessage) {
                videoMessage.classList.add("hidden");
            }

        }
    );


    video.addEventListener(
        "ended",
        function () {

            playButton.textContent = "▶";

        }
    );


    /* =========================================
       ERREUR VIDEO
    ========================================== */

    video.addEventListener(
        "error",
        function () {

            console.error(
                "SHADOW PLAYER : erreur de lecture vidéo."
            );

            if (videoMessage) {

                videoMessage.classList.remove(
                    "hidden"
                );

                videoMessage.querySelector(
                    "p"
                ).textContent =
                    "La vidéo ne peut pas être chargée.";

            }

        }
    );


    /* =========================================
       RACCOURCIS CLAVIER
    ========================================== */

    document.addEventListener(
        "keydown",
        function (event) {

            /*
             * Ne pas intercepter les touches
             * lorsqu'on écrit dans un champ.
             */

            const tag =
                document.activeElement.tagName;

            if (
                tag === "INPUT" ||
                tag === "SELECT" ||
                tag === "TEXTAREA"
            ) {

                return;
            }


            /* Espace */

            if (event.code === "Space") {

                event.preventDefault();

                togglePlay();

            }


            /* Flèche gauche */

            if (
                event.key === "ArrowLeft"
            ) {

                video.currentTime =
                    Math.max(
                        0,
                        video.currentTime - 10
                    );

            }


            /* Flèche droite */

            if (
                event.key === "ArrowRight"
            ) {

                video.currentTime =
                    Math.min(
                        video.duration || Infinity,
                        video.currentTime + 10
                    );

            }


            /* M = mute */

            if (
                event.key.toLowerCase() === "m"
            ) {

                video.muted =
                    !video.muted;

                updateMuteButton();

            }


            /* F = fullscreen */

            if (
                event.key.toLowerCase() === "f"
            ) {

                fullscreenButton.click();

            }

        }
    );


    /* =========================================
       INITIALISATION
    ========================================== */

    video.volume = 1;

    volumeBar.value = 1;

    updateMuteButton();

    updateTime();

    updateProgress();

});
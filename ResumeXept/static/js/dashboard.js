/* =========================================
   ResumeXpert Dashboard JavaScript
========================================= */

document.addEventListener("DOMContentLoaded", function () {

    /* ================= ACTIVE MENU ================= */
    const currentPath = window.location.pathname;

    document.querySelectorAll(".menu a").forEach(function (link) {
        link.classList.remove("active");

        if (link.getAttribute("href") === currentPath) {
            link.classList.add("active");
        }
    });


    /* ================= RESUME FILE NAME ================= */
    const resumeInput = document.getElementById("resume");
    const resumeName = document.getElementById("resumeName");

    if (resumeInput && resumeName) {
        resumeInput.addEventListener("change", function () {

            if (resumeInput.files.length > 0) {
                resumeName.textContent = resumeInput.files[0].name;
            } else {
                resumeName.textContent = "No file selected";
            }

        });
    }


    /* ================= JOB DESCRIPTION FILE NAME ================= */
    const jdInput = document.getElementById("job_description");
    const jdName = document.getElementById("jdName");

    if (jdInput && jdName) {
        jdInput.addEventListener("change", function () {

            if (jdInput.files.length > 0) {
                jdName.textContent = jdInput.files[0].name;
            } else {
                jdName.textContent = "No file selected";
            }

        });
    }


    /* ================= PROGRESS BARS ================= */
    const progressBars = document.querySelectorAll(".progress-bar");

    progressBars.forEach(function (bar) {

        let width = bar.getAttribute("data-width");

        if (!width) {
            width = bar.style.width || "0%";
        }

        bar.style.width = "0%";

        setTimeout(function () {
            bar.style.width = width;
        }, 300);

    });


    /* ================= ATS TREND CHART ================= */
    const chartCanvas = document.getElementById("atsChart");

    if (chartCanvas && typeof Chart !== "undefined") {

        let score = parseFloat(chartCanvas.dataset.score);

        if (isNaN(score)) {
            score = 0;
        }

        /* Keep score between 0 and 100 */
        score = Math.max(0, Math.min(100, score));

        new Chart(chartCanvas, {

            type: "doughnut",

            data: {
                labels: [
                    "ATS Score",
                    "Remaining"
                ],

                datasets: [{
                    data: [
                        score,
                        100 - score
                    ],
                    borderWidth: 0
                }]
            },

            options: {

                responsive: true,

                maintainAspectRatio: false,

                cutout: "70%",

                plugins: {

                    legend: {
                        display: true,
                        position: "bottom"
                    }

                }

            }

        });

    }


    /* ================= UPLOAD FORM ================= */
    const uploadForm = document.querySelector(".upload-form");
    const compareBtn = document.querySelector(".compare-btn");

    if (uploadForm && compareBtn) {

        uploadForm.addEventListener("submit", function () {

            compareBtn.disabled = true;

            compareBtn.innerHTML =
                '<i class="fa-solid fa-spinner fa-spin"></i> Analyzing...';

        });

    }


    /* ================= DOWNLOAD BUTTON ================= */
    const downloadBtn = document.querySelector(".download-btn");

    if (downloadBtn) {

        downloadBtn.addEventListener("click", function () {

            alert(
                "Analysis report download will be available soon."
            );

        });

    }


    /* ================= CARD ANIMATION ================= */
    const animatedElements =
        document.querySelectorAll(
            ".card, .panel, .suggestion, .upload-card"
        );

    animatedElements.forEach(function (element, index) {

        element.style.opacity = "0";

        element.style.transform =
            "translateY(15px)";

        setTimeout(function () {

            element.style.transition =
                "opacity 0.5s ease, transform 0.5s ease";

            element.style.opacity = "1";

            element.style.transform =
                "translateY(0)";

        }, index * 60);

    });

});
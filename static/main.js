function checkURL() {
    const urlInput = document.getElementById("url");
    const resultBox = document.getElementById("result");

    if (!urlInput) {
        alert("URL input box not found");
        return;
    }

    const url = urlInput.value.trim();

    if (url === "") {
        alert("Please enter a URL");
        return;
    }

    resultBox.innerText = "Checking...";

    fetch("/predict", {  // ← FIXED: relative path
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ url: url })
    })
    .then(response => {
        if (!response.ok) {
            throw new Error(`HTTP ${response.status}`);
        }
        return response.json();
    })
    .then(data => {
        if (data.result === "Phishing Website") {
            resultBox.innerHTML = '<span style="color: #dc3545; font-size: 24px;">⚠️ PHISHING WEBSITE!</span>';
        } else {
            resultBox.innerHTML = '<span style="color: #28a745; font-size: 24px;">✅ SAFE WEBSITE</span>';
        }
    })
    .catch(error => {
        resultBox.innerHTML = '<span style="color: #ff9800;">❌ Error: Backend issue. Check console.</span>';
        console.error("Fetch error:", error);
    });
}

async function testRegex() {

    const pattern = document.getElementById("pattern").value;
    const text = document.getElementById("text").value;

    const response = await fetch("/test", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({pattern, text})
    });

    const data = await response.json();

    document.getElementById("count").textContent = data.count;

    document.getElementById("explanation").textContent =
        data.explanation;

    if (data.error) {

        document.getElementById("message").innerHTML =
            '<span class="error">Invalid regex: '
            + data.error + '</span>';

        document.getElementById("visual").innerHTML = "";

        return;
    }

    document.getElementById("message").textContent =
        data.count
        ? "Pattern matched successfully."
        : "No match found.";

    document.getElementById("visual").innerHTML =
        data.matches.map(x =>
            '<span class="match">'
            + escapeHtml(x)
            + '</span>'
        ).join("");
}


async function saveCase() {

    const pattern = document.getElementById("pattern").value;
    const text = document.getElementById("text").value;

    const response = await fetch("/save", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({pattern, text})
    });

    const data = await response.json();

    alert(data.message);
}


async function compareRegex() {

    const text = document.getElementById("text").value;

    const patterns = document.getElementById("patterns").value
        .split(",")
        .map(x => x.trim())
        .filter(Boolean);

    const response = await fetch("/compare", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({patterns, text})
    });

    const data = await response.json();

    document.getElementById("comparison").innerHTML =
        data.map(x =>
            `<p>
                <b>${escapeHtml(x.pattern)}</b>
                → ${x.matches} matches,
                ${x.time_ms} ms
            </p>`
        ).join("");
}


function escapeHtml(text) {

    return text.replace(/[&<>"']/g, c => ({
        "&": "&amp;",
        "<": "&lt;",
        ">": "&gt;",
        '"': "&quot;",
        "'": "&#039;"
    }[c]));

}

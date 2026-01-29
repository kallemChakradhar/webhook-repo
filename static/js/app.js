let shownEvents = new Set();

async function fetchEvents() {
    try {
        const res = await fetch("/events");
        const data = await res.json();

        const container = document.getElementById("events");

        container.innerHTML = ""; // clear old UI (to keep correct order)

        data.forEach(item => {
            const key = item.type + item.message;

            if (!shownEvents.has(key)) {
                shownEvents.add(key);
            }

            let typeClass = "push";
            if (item.type === "PULL_REQUEST") typeClass = "pr";
            if (item.type === "MERGE") typeClass = "merge";

            const div = document.createElement("div");
            div.className = "event";
            div.innerHTML = `<span class="badge ${typeClass}">${item.type}</span> ${item.message}`;

            container.append(div); //latest already sorted from backend
        });

    } catch (err) {
        console.error("Error fetching events:", err);
    }
}

// initial load
fetchEvents();

// poll every 15 seconds
setInterval(fetchEvents, 15000);

const currentFlipDowns = []

function initFlipDown(containerId, targetTime, leppMinutes) {
    return new FlipDown(
        targetTime - leppMinutes * 60,
        containerId,
        { headings: ["Dagar", "Timmar", "Minuter", "Sekunder"], theme: "light" },
    ).start().ifEnded(() => {
        setTimeout(() => window.location.reload(), 2000)
    })
}

function initFlipDowns(leppMinutes = 0) {
    const containers = document.getElementsByClassName("flipdown")
    for (const container of containers) {
        container.innerHTML = "";
        currentFlipDowns.push(initFlipDown(container.id, parseInt(container.dataset.target), leppMinutes))
    }
}

window.setLepp = function () {
    const rangeInput = document.getElementById("lepp-range")
    if (!rangeInput) {
        return
    }
    const leppMinutes = parseInt(rangeInput.value)
    if (leppMinutes > 0) {
        rangeInput.value = 0
        document.getElementById("lepp-mins").textContent = "0"
        document.getElementById("lepp-panel").classList.remove("show")
        while (currentFlipDowns.length > 0) {
            currentFlipDowns.pop()
        }
        initFlipDowns(leppMinutes)
    }
}

let hideTimeout
function resetCursorTimer() {
    document.body.classList.remove("hide-cursor")
    clearTimeout(hideTimeout)
    hideTimeout = setTimeout(() => {
        document.body.classList.add("hide-cursor")
    }, 2000)
}

document.addEventListener("mousemove", resetCursorTimer)
document.addEventListener("DOMContentLoaded", resetCursorTimer)
document.addEventListener("DOMContentLoaded", () => initFlipDowns())

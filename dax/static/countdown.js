let currentFlipDown
let currentTargetTime

function initFlipDown() {
    const container = document.getElementById("flipdown")
    if (!container) {
        return
    }
    // Unix timestamp (in seconds) to count down to
    currentTargetTime = Number.parseInt(container.dataset.target)

    // Set up FlipDown
    currentFlipDown = new FlipDown(
        currentTargetTime,
        { headings: ["Dagar", "Timmar", "Minuter", "Sekunder"], theme: "light" },
    ).start().ifEnded(() => {
        setTimeout(() => window.location.reload(), 2000)
    })
}

document.addEventListener("DOMContentLoaded", initFlipDown)

window.setLepp = function () {
    const leppMinutes = parseInt(document.getElementById("lepp-range").value)
    if (leppMinutes > 0) {
        currentTargetTime -= (leppMinutes * 60)

        document.getElementById("lepp-range").value = 0
        document.getElementById("lepp-mins").textContent = "0"
        document.getElementById("lepp-panel").classList.remove("show")

        const container = document.getElementById("flipdown")
        container.innerHTML = ""

        currentFlipDown = new FlipDown(
            currentTargetTime,
            { headings: ["Dagar", "Timmar", "Minuter", "Sekunder"], theme: "light" },
        ).start().ifEnded(() => {
            setTimeout(() => window.location.reload(), 2000)
        })
    }
}

let hideTimeout
function resetCursorTimer() {
    document.body.classList.remove("hide-cursor")
    clearTimeout(hideTimeout)
    hideTimeout = setTimeout(() => {
        {
            document.body.classList.add("hide-cursor")
        }
    }, 2000)
}

document.addEventListener("mousemove", resetCursorTimer)
document.addEventListener("DOMContentLoaded", resetCursorTimer)

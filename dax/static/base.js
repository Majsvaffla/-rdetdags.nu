document.addEventListener("DOMContentLoaded", () => {
    const root = document.documentElement
    const button = document.getElementById("theme-toggle")

    const savedTheme = localStorage.getItem("theme")
    if (savedTheme) {
        root.setAttribute("data-theme", savedTheme)
    }

    function updateIcon() {
        const theme = root.getAttribute("data-theme")
        button.textContent = theme === "dark" ? "☀️" : "🌙"
    }
    updateIcon()

    if (button) {
        button.addEventListener("click", () => {
            const current = root.getAttribute("data-theme")
            const newTheme = current === "dark" ? "light" : "dark"
            root.setAttribute("data-theme", newTheme)
            localStorage.setItem("theme", newTheme)
            updateIcon()
        })
    }

    window.toggleFullScreen = function () {
        if ((document.fullScreenElement && document.fullScreenElement !== null) ||
            (!document.mozFullScreen && !document.webkitIsFullScreen)) {
            if (document.documentElement.requestFullScreen) {
                document.documentElement.requestFullScreen()
            } else if (document.documentElement.mozRequestFullScreen) {
                document.documentElement.mozRequestFullScreen()
            } else if (document.documentElement.webkitRequestFullScreen) {
                document.documentElement.webkitRequestFullScreen(Element.ALLOW_KEYBOARD_INPUT)
            }
        } else {
            if (document.cancelFullScreen) {
                document.cancelFullScreen()
            } else if (document.mozCancelFullScreen) {
                document.mozCancelFullScreen()
            } else if (document.webkitCancelFullScreen) {
                document.webkitCancelFullScreen()
            }
        }
    }

    window.copyURL = function () {
        navigator.clipboard.writeText(window.location.href)
            .then(() => { })
            .catch(err => {
                console.error("Failed to copy: ", err)
            })
    }

    window.toggleLepp = function () {
        const panel = document.getElementById('lepp-panel')
        panel.classList.toggle('show')
    }

    window.updateLepp = function (value) {
        document.getElementById('lepp-mins').textContent = value
    }
})

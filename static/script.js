// ======================================================
// AI POWER BI ASSISTANT
// script.js
// ======================================================


// ======================================================
// ELEMENT REFERENCES
// ======================================================

const aiButton = document.getElementById("aiButton");
const chatWindow = document.getElementById("chatWindow");

const closeBtn = document.getElementById("closeBtn");
const minimizeBtn = document.getElementById("minimizeBtn");
const clearBtn = document.getElementById("clearBtn");

const sendButton = document.getElementById("sendButton");
const questionInput = document.getElementById("questionInput");

const chatMessages = document.getElementById("chatMessages");
const typingIndicator = document.getElementById("typingIndicator");

const suggestions = document.querySelectorAll(".suggestion");
const chatHeader = document.getElementById("chatHeader");

const STORAGE_KEY = "ai_powerbi_chat";


// ======================================================
// CHART STORAGE
// ======================================================

const charts = {};


// ======================================================
// DEFAULT WELCOME MESSAGE
// ======================================================

const defaultWelcome = `
<div class="bot-wrapper">
    <div class="avatar">🤖</div>

    <div class="bot-message">
        <h3>Welcome!</h3>

        <p>I'm your AI Business Intelligence Assistant.</p>

        <p>Ask me anything about your dashboard.</p>

        <div class="timestamp">
            Just now
        </div>
    </div>
</div>
`;


// ======================================================
// OPEN CHAT
// ======================================================

if (aiButton) {

    aiButton.addEventListener("click", () => {

        if (chatWindow) {
            chatWindow.classList.remove("hidden");
        }

        aiButton.style.display = "none";

        if (questionInput) {
            questionInput.focus();
        }

    });

}


// ======================================================
// CLOSE CHAT
// ======================================================

if (closeBtn) {

    closeBtn.addEventListener("click", () => {

        if (chatWindow) {
            chatWindow.classList.add("hidden");
        }

        if (aiButton) {
            aiButton.style.display = "block";
        }

    });

}


// ======================================================
// MINIMIZE CHAT
// ======================================================

let minimized = false;

if (minimizeBtn) {

    minimizeBtn.addEventListener("click", () => {

        minimized = !minimized;

        const messages = document.getElementById("chatMessages");
        const input = document.getElementById("chatInput");
        const suggestionBox = document.getElementById("suggestions");

        if (minimized) {

            if (messages) messages.style.display = "none";
            if (input) input.style.display = "none";
            if (suggestionBox) suggestionBox.style.display = "none";
            if (typingIndicator) typingIndicator.style.display = "none";

            if (chatWindow) {
                chatWindow.style.height = "65px";
            }

        } else {

            if (messages) messages.style.display = "flex";
            if (input) input.style.display = "flex";
            if (suggestionBox) suggestionBox.style.display = "flex";

            if (chatWindow) {
                chatWindow.style.height = "620px";
            }

        }

    });

}


// ======================================================
// TIMESTAMP
// ======================================================

function getTimeStamp() {

    return new Date().toLocaleTimeString([], {
        hour: "2-digit",
        minute: "2-digit"
    });

}


// ======================================================
// LOCAL STORAGE
// ======================================================

function saveChat() {

    if (!chatMessages) return;

    localStorage.setItem(
        STORAGE_KEY,
        chatMessages.innerHTML
    );

}


function loadChat() {

    if (!chatMessages) return;

    const history = localStorage.getItem(STORAGE_KEY);

    if (history && history.trim() !== "") {

        chatMessages.innerHTML = history;

    } else {

        chatMessages.innerHTML = defaultWelcome;

    }

    chatMessages.scrollTop = chatMessages.scrollHeight;

}


function clearChat() {

    if (!confirm("Clear chat history?")) return;

    localStorage.removeItem(STORAGE_KEY);

    if (chatMessages) {
        chatMessages.innerHTML = defaultWelcome;
    }

    saveChat();

}


if (clearBtn) {
    clearBtn.addEventListener("click", clearChat);
}

// ======================================================
// MESSAGE RENDERER
// ======================================================

function addMessage(message, sender) {

    if (!chatMessages) return;

    const wrapper = document.createElement("div");
    wrapper.className = `${sender}-wrapper`;

    const avatar = document.createElement("div");
    avatar.className = "avatar";
    avatar.innerHTML = sender === "user" ? "🧑" : "🤖";

    const bubble = document.createElement("div");
    bubble.className = `${sender}-message`;

    if (window.marked) {
        bubble.innerHTML = marked.parse(String(message));
    } else {
        bubble.innerHTML = String(message).replace(/\n/g, "<br>");
    }

    const time = document.createElement("div");
    time.className = "timestamp";
    time.innerText = getTimeStamp();

    bubble.appendChild(time);

    wrapper.appendChild(avatar);
    wrapper.appendChild(bubble);

    chatMessages.appendChild(wrapper);

    chatMessages.scrollTo({
        top: chatMessages.scrollHeight,
        behavior: "smooth"
    });

    saveChat();

}


// ======================================================
// TYPING INDICATOR
// ======================================================

function showTyping() {

    if (typingIndicator) {
        typingIndicator.classList.remove("hidden");
    }

}


function hideTyping() {

    if (typingIndicator) {
        typingIndicator.classList.add("hidden");
    }

}


// ======================================================
// SEND MESSAGE
// ======================================================

async function sendMessage() {

    if (!questionInput) return;

    const question = questionInput.value.trim();

    if (!question) return;

    addMessage(question, "user");

    questionInput.value = "";

    // Improvement #1
    if (questionInput) {
        questionInput.focus();
    }

    if (sendButton) {
        sendButton.disabled = true;
        sendButton.innerText = "Sending...";
    }

    showTyping();

    try {

        const response = await fetch("/chat", {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                question
            })

        });

        if (!response.ok) {
            throw new Error(`Server returned ${response.status}`);
        }

        // Improvement #7
        const contentType = response.headers.get("content-type");

        if (!contentType || !contentType.includes("application/json")) {
            throw new Error("Server did not return JSON.");
        }

        const data = await response.json();

        hideTyping();

        if (data.success) {

            addMessage(data.answer, "bot");

        } else {

            addMessage(`❌ ${data.answer}`, "bot");

        }

    }
    catch (err) {

        hideTyping();

        console.error(err);

        addMessage(

`❌ Unable to contact the AI Assistant.

Please verify:

• FastAPI server is running
• Backend is online
• Internet connection is available

Error:
${err.message}`,

        "bot");

    }
    finally {

        if (sendButton) {
            sendButton.disabled = false;
            sendButton.innerText = "Send";
        }

    }

}

// ======================================================
// EVENTS
// ======================================================

if (sendButton) {

    sendButton.addEventListener("click", sendMessage);

}

if (questionInput) {

    questionInput.addEventListener("keydown", function (e) {

        if (e.key === "Enter") {

            e.preventDefault();
            sendMessage();

        }

    });

}


// ======================================================
// SUGGESTION BUTTONS
// ======================================================

if (suggestions.length) {

    suggestions.forEach(button => {

        button.addEventListener("click", () => {

            if (!questionInput) return;

            questionInput.value = button.textContent.trim();

            sendMessage();

        });

    });

}


// ======================================================
// DRAGGABLE CHAT WINDOW
// ======================================================

let isDragging = false;
let offsetX = 0;
let offsetY = 0;

if (chatHeader && chatWindow) {

    chatHeader.addEventListener("mousedown", function (e) {

        e.preventDefault();

        isDragging = true;

        const rect = chatWindow.getBoundingClientRect();

        offsetX = e.clientX - rect.left;
        offsetY = e.clientY - rect.top;

        chatWindow.style.right = "auto";
        chatWindow.style.bottom = "auto";

    });

}

document.addEventListener("mousemove", function (e) {

    if (!isDragging || !chatWindow) return;

    chatWindow.style.left = (e.clientX - offsetX) + "px";
    chatWindow.style.top = (e.clientY - offsetY) + "px";

});

document.addEventListener("mouseup", function () {

    isDragging = false;

});


// ======================================================
// KEYBOARD SHORTCUT
// CTRL + /
// ======================================================

document.addEventListener("keydown", function (e) {

    if (e.ctrlKey && e.key === "/") {

        e.preventDefault();

        if (chatWindow) {
            chatWindow.classList.remove("hidden");
        }

        if (aiButton) {
            aiButton.style.display = "none";
        }

        if (questionInput) {
            questionInput.focus();
        }

    }

});


// ======================================================
// LOAD DASHBOARD
// ======================================================

async function loadDashboard() {

    try {

        const response = await fetch("/dashboard");

        if (!response.ok) {
            throw new Error(
                "Unable to load dashboard (" + response.status + ")"
            );
        }

        // Improvement #7
        const contentType = response.headers.get("content-type");

        if (!contentType || !contentType.includes("application/json")) {
            throw new Error("Server did not return JSON.");
        }

        const data = await response.json();

        // ======================================================
        // KPI CARDS
        // ======================================================

        const sales = document.getElementById("kpiSales");
        const profit = document.getElementById("kpiProfit");
        const orders = document.getElementById("kpiOrders");
        const average = document.getElementById("kpiAverage");

        if (sales) {
            sales.textContent =
                "$" + Number(data?.kpis?.total_sales ?? 0).toFixed(2);
        }

        if (profit) {
            profit.textContent =
                "$" + Number(data?.kpis?.total_profit ?? 0).toFixed(2);
        }

        if (orders) {
            orders.textContent =
                Number(data?.kpis?.total_orders ?? 0);
        }

        if (average) {
            average.textContent =
                "$" +
                Number(data?.kpis?.average_order_value ?? 0).toFixed(2);
        }

        // ======================================================
        // DESTROY OLD CHARTS
        // ======================================================

        Object.keys(charts).forEach(key => {

            if (charts[key]) {
                charts[key].destroy();
            }

            delete charts[key];

        });

        // ======================================================
        // COMMON CHART OPTIONS
        // ======================================================

        const commonOptions = {

            responsive: true,
            maintainAspectRatio: false,

            animation: {
                duration: 800
            },

            plugins: {

                legend: {

                    position: "bottom",

                    labels: {
                        color: "#E2E8F0"
                    }

                }

            }

        };

        // ======================================================
        // REGION BAR CHART
        // ======================================================

        const regionCanvas = document.getElementById("regionChart");

        if (regionCanvas) {

            charts.region = new Chart(regionCanvas, {

                type: "bar",

                data: {

                    labels: data.sales_by_region.labels,

                    datasets: [{

                        label: "Sales",

                        data: data.sales_by_region.values,

                        backgroundColor: [
                            "#3B82F6",
                            "#2563EB",
                            "#1D4ED8",
                            "#60A5FA",
                            "#93C5FD"
                        ],

                        borderRadius: 8

                    }]

                },

                options: {

                    ...commonOptions,

                    plugins: {

                        ...commonOptions.plugins,

                        legend: {
                            display: false
                        }

                    },

                    scales: {

                        y: {

                            beginAtZero: true,

                            ticks: {
                                color: "#CBD5E1"
                            },

                            grid: {
                                color: "rgba(255,255,255,.08)"
                            }

                        },

                        x: {

                            ticks: {
                                color: "#CBD5E1"
                            },

                            grid: {
                                display: false
                            }

                        }

                    }

                }

            });

        }

        // ======================================================
        // CATEGORY PIE CHART
        // ======================================================

        const categoryCanvas = document.getElementById("categoryChart");

        if (categoryCanvas) {

            charts.category = new Chart(categoryCanvas, {

                type: "pie",

                data: {

                    labels: data.sales_by_category.labels,

                    datasets: [{

                        data: data.sales_by_category.values,

                        backgroundColor: [
                            "#3B82F6",
                            "#EC4899",
                            "#F59E0B",
                            "#10B981",
                            "#8B5CF6",
                            "#06B6D4"
                        ]

                    }]

                },

                options: commonOptions

            });

        }

        // ======================================================
        // MONTHLY SALES LINE CHART
        // ======================================================

        const monthlyCanvas = document.getElementById("monthlyChart");

        if (monthlyCanvas) {

            charts.monthly = new Chart(monthlyCanvas, {

                type: "line",

                data: {

                    labels: data.monthly_sales.labels,

                    datasets: [{

                        label: "Monthly Sales",

                        data: data.monthly_sales.values,

                        borderColor: "#10B981",

                        backgroundColor: "rgba(16,185,129,.18)",

                        fill: true,

                        tension: 0.4

                    }]

                },

                options: {

                    ...commonOptions,

                    scales: {

                        y: {

                            beginAtZero: true,

                            ticks: {
                                color: "#CBD5E1"
                            },

                            grid: {
                                color: "rgba(255,255,255,.08)"
                            }

                        },

                        x: {

                            ticks: {
                                color: "#CBD5E1"
                            },

                            grid: {
                                display: false
                            }

                        }

                    }

                }

            });

        }

        // ======================================================
        // PAYMENT DOUGHNUT CHART
        // ======================================================

        const paymentCanvas = document.getElementById("paymentChart");

        if (paymentCanvas) {

            charts.payment = new Chart(paymentCanvas, {

                type: "doughnut",

                data: {

                    labels: data.payment_methods.labels,

                    datasets: [{

                        data: data.payment_methods.values,

                        backgroundColor: [
                            "#6366F1",
                            "#F59E0B",
                            "#10B981",
                            "#EF4444",
                            "#06B6D4",
                            "#8B5CF6"
                        ]

                    }]

                },

                options: commonOptions

            });

        }

    }

    catch (error) {

        console.error("Dashboard Error:", error);

    }

}

// ======================================================
// START APPLICATION
// ======================================================

window.addEventListener("DOMContentLoaded", () => {

    console.log("script.js loaded");

    // Restore previous chat history
    loadChat();

    // Load dashboard
    loadDashboard();

    // Focus input if available
    if (questionInput) {
        questionInput.focus();
    }

});


// Expose clear chat globally
window.clearAIChat = clearChat;


// ======================================================
// OPTIONAL AUTO REFRESH DASHBOARD
// ======================================================

// Uncomment if you want live dashboard updates
// setInterval(loadDashboard, 60000);


// ======================================================
// RESIZE CHARTS (Debounced)
// ======================================================

let resizeTimeout;

window.addEventListener("resize", () => {

    clearTimeout(resizeTimeout);

    resizeTimeout = setTimeout(() => {

        Object.values(charts).forEach(chart => {

            if (chart) {
                chart.resize();
            }

        });

    }, 150);

});


// ======================================================
// ONLINE / OFFLINE STATUS
// ======================================================

window.addEventListener("offline", () => {

    addMessage(
        "⚠️ You are offline. Dashboard data may not update until the connection is restored.",
        "bot"
    );

});


window.addEventListener("online", () => {

    addMessage(
        "✅ Internet connection restored.",
        "bot"
    );

    loadDashboard();

});


// ======================================================
// PAGE VISIBILITY
// Refresh dashboard only if the last refresh
// was more than 30 seconds ago
// ======================================================

let lastRefresh = Date.now();

document.addEventListener("visibilitychange", () => {

    if (!document.hidden && Date.now() - lastRefresh > 30000) {

        loadDashboard();

        lastRefresh = Date.now();

    }

});


// ======================================================
// APPLICATION READY
// ======================================================

console.log(`
====================================
 AI Power BI Assistant
====================================
✅ Chat Loaded
✅ Dashboard Loaded
✅ Charts Ready
====================================
`);
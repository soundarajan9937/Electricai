// =====================================================
// ELECTRIC AI - API CONFIGURATION
// =====================================================

const API_BASE_URL = (function () {
    if (window.CUSTOM_API_BASE_URL) {
        return window.CUSTOM_API_BASE_URL;
    }
    // Standalone local server (e.g., Live Server / python http.server on port 5500)
    if (window.location.port === "5500" || window.location.port === "5501" || window.location.port === "3000") {
        return "http://127.0.0.1:5000";
    }
    // Dynamically match current domain (e.g. https://electricai.onrender.com)
    return window.location.origin;
})();

console.log("=================================");
console.log("⚡ ELECTRIC AI API CONFIG");
console.log("=================================");
console.log("Backend URL:", API_BASE_URL);

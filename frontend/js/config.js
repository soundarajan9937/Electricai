// Dynamic API Base URL configuration for local and deployed environments
const API_BASE_URL = (function () {
    if (window.CUSTOM_API_BASE_URL) {
        return window.CUSTOM_API_BASE_URL;
    }
    // If running frontend on local standalone server (e.g. Python http.server on port 5500)
    if (window.location.port === "5500" || window.location.port === "5501" || window.location.port === "3000") {
        return "http://127.0.0.1:5000";
    }
    // Relative URL when served together by Flask or same origin in production (Render)
    return "";
})();

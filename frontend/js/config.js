// =====================================================
// ELECTRIC AI - API CONFIGURATION
// =====================================================

const API_BASE_URL = (
    window.location.hostname === "127.0.0.1" ||
    window.location.hostname === "localhost"
)
    ? "http://127.0.0.1:5000"
    : "https://electric-ai-backend-sound.onrender.com";


console.log("=================================");
console.log("⚡ ELECTRIC AI API CONFIG");
console.log("=================================");
console.log("Frontend:", window.location.href);
console.log("Backend URL:", API_BASE_URL);
console.log("=================================");
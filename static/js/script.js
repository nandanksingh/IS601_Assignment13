/*
    Author: Nandan Kumar
    Assignment 13: Global Script File
    File: static/js/script.js

    Description:
    Shared client-side helper utilities used across all pages.
    Handles authentication token storage, logout workflow,
    navigation shortcuts, secure API calls, and message helpers.
*/

/* ----------------------------------------------------------
   AUTH HELPERS
---------------------------------------------------------- */

function clearAuth() {
    localStorage.removeItem("access_token");
    localStorage.removeItem("username");
}

function isLoggedIn() {
    return localStorage.getItem("access_token") !== null;
}

function requireAuth() {
    if (!isLoggedIn()) {
        window.location.href = "/login";
    }
}

function getToken() {
    return localStorage.getItem("access_token");
}

/* ----------------------------------------------------------
   NAVIGATION
---------------------------------------------------------- */

function redirect(path) {
    window.location.href = path;
}

/* ----------------------------------------------------------
   MESSAGE HELPERS
---------------------------------------------------------- */

function setMessage(id, text, color = "#ffcccc") {
    const el = document.getElementById(id);
    if (el) {
        el.textContent = text;
        el.style.color = color;
    }
}

function fadeOut(id, delay = 1500) {
    setTimeout(() => {
        const el = document.getElementById(id);
        if (el) {
            el.style.transition = "opacity 1s ease";
            el.style.opacity = "0";
        }
    }, delay);
}

/* ----------------------------------------------------------
   LOGOUT HANDLER
---------------------------------------------------------- */

function logoutUser() {
    clearAuth();
    redirect("/logout");
}

/* ----------------------------------------------------------
   SAFE API WRAPPER
---------------------------------------------------------- */

async function safeFetch(url, options = {}) {
    const token = getToken();

    const headers = {
        "Content-Type": "application/json",
        ...(options.headers || {})
    };

    if (token) {
        headers["Authorization"] = "Bearer " + token;
    }

    return fetch(url, {
        ...options,
        headers
    });
}

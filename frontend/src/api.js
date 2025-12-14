import axios from "axios";

const API_BASE_URL = "http://localhost:8000/api/v1";

const api = axios.create({
    baseURL: API_BASE_URL,
    headers: { "Content-Type": "application/json" },
});

/* ================= AUTH TOKEN ================= */

export const setAuthToken = (token) => {
    if (token) {
        api.defaults.headers.common["Authorization"] = `Bearer ${token}`;
        localStorage.setItem("token", token);
    } else {
        delete api.defaults.headers.common["Authorization"];
        localStorage.removeItem("token");
    }
};

// Decode JWT payload
export const getTokenPayload = () => {
    const token = localStorage.getItem("token");
    if (!token) return null;
    return JSON.parse(atob(token.split(".")[1]));
};

// Admin check
export const isAdmin = () => {
    const payload = getTokenPayload();
    return payload?.is_admin === true;
};

/* ================= AUTH ================= */

export const registerUser = (username, password) =>
    api.post("/auth/register", { username, password });

export const loginUser = (username, password) =>
    api.post("/auth/login", { username, password });

/* ================= SWEETS ================= */

export const getSweets = () => api.get("/sweets/");

export const createSweet = (data) => api.post("/sweets/", data);

export const updateSweet = (id, data) =>
    api.put(`/sweets/${id}`, data);

export const deleteSweet = (id) =>
    api.delete(`/sweets/${id}`);

export const restockSweet = (id, amount = 10) =>
    api.post(`/sweets/${id}/restock?amount=${amount}`);
// ================= PURCHASE =================

export const purchaseSweet = (id) =>
    api.post(`/sweets/${id}/purchase`);

// ================= SEARCH =================

export const searchSweets = (params) =>
    api.get("/sweets/search", { params });


export default api;

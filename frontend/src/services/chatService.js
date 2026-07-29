import axios from "axios";

const api = axios.create({
    baseURL: "http://localhost:8000"
});

export async function sendMessage(question) {

    const response = await api.post("/api/v1/query", {
        question: question,
        session_id: "demo-session"
    });

    return response.data;
}
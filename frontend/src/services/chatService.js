import apiClient from "./apiClient";

export async function sendMessage(question) {

    console.log("question:", question);
    
    const response = await apiClient.post("/api/v1/chat", {
        message: question,
        session_id: "demo-session"
    });

    console.log("Full Response:", response);
    console.log("Response Data:", response.data);

    return response.data;
}
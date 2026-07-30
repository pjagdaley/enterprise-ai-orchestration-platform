import { Box, Typography } from "@mui/material";
import { useState } from "react";

import ChatWindow from "../components/chat/ChatWindow";
import ChatInput from "../components/chat/ChatInput";
import { sendMessage } from "../services/chatService";
import WelcomeScreen from "../components/chat/WelcomeScreen";

function ChatPage() {

    const [messages, setMessages] = useState([]);
    const [loading, setLoading] = useState(false);
 
    /*
    const handleSend = async (message) => {

        // Add user message
        setMessages(previous => [
            ...previous,
            {
                sender: "You",
                text: message,
                time: new Date().toLocaleTimeString([], {
                    hour: "2-digit",
                    minute: "2-digit"
                })
            }
        ]);

        setLoading(true);

        // Simulate network delay
        await new Promise(resolve => setTimeout(resolve, 2000));

        // Dummy AI response
        setMessages(previous => [
            ...previous,
            {
                sender: "AI",
                text: "This is a dummy response from the Enterprise AI Platform.",
                time: new Date().toLocaleTimeString([], {
                    hour: "2-digit",
                    minute: "2-digit"
                })
            }
        ]);

        setLoading(false);
    };
    */
    
    const handleSend = async (message) => {

        setMessages(previous => [
            ...previous,
            {
                sender: "You",
                text: message,
                time: new Date().toLocaleTimeString([], {
                    hour: "2-digit",
                    minute: "2-digit"
                })
            }
        ]);

        try {

            setLoading(true);
            const response = await sendMessage(message);
            setLoading(false);

            setMessages(previous => [
                ...previous,
                {
                    sender: "AI",
                    text: response.response,
                    time: new Date().toLocaleTimeString([], {
                        hour: "2-digit",
                        minute: "2-digit"
                    })
                }
            ]);

        } catch (error) {

            setLoading(false);
            setMessages(previous => [
                ...previous,
                {
                    sender: "System",
                    text: "Unable to contact the server."
                }
            ]);

            console.error(error);
        }

    }; 

    return (
        <Box>
            <Typography
                variant="h5"
                gutterBottom
            >
                Enterprise AI Chat
            </Typography>

            {messages.length === 0 ? (
            
                <WelcomeScreen />
                             
            ) : (
                <ChatWindow
                    messages={messages}
                    loading={loading}
                />
            )}            

            <ChatInput
                onSend={handleSend}
                loading={loading}
            />
        </Box>
    );
}

export default ChatPage;
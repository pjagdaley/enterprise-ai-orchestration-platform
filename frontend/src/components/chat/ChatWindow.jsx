import { Paper, Typography } from "@mui/material";
import { useEffect, useRef } from "react";
import { CircularProgress } from "@mui/material";

import ChatMessage from "./ChatMessage";

function ChatWindow({ messages, loading }) {

    const bottomRef = useRef(null);

    useEffect(() => {

        bottomRef.current?.scrollIntoView({
            behavior: "smooth"
        });

    }, [messages]);

    return (
        <Paper
            elevation={2}
            sx={{
                height: "65vh",
                overflowY: "auto",
                p: 2
            }}
        >
            {messages.map((message, index) => (
                <ChatMessage
                    key={index}
                    sender={message.sender}
                    text={message.text}
                    time={message.time}
                />
            ))}
            
            {loading && (
                <ChatMessage
                    sender="AI"
                    text={
                        <>
                            <CircularProgress
                                size={18}
                                sx={{ mr: 1 }}
                            />
                            Thinking...
                        </>
                    }
                />
            )}
            <div ref={bottomRef} />
        </Paper>
    );
}

export default ChatWindow;
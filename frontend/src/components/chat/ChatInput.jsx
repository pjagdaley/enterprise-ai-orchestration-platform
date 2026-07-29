import { useState } from "react";
import {
    Box,
    Button,
    Paper,
    TextField
} from "@mui/material";

function ChatInput({ onSend, loading }) {

    const [message, setMessage] = useState("");

    const handleSend = () => {

        if (!message.trim()) {
            return;
        }

        onSend(message);

        setMessage("");
    };

    const handleKeyDown = (event) => {

        if (event.key === "Enter" && !event.shiftKey) {

            event.preventDefault();

            handleSend();
        }

    };

    return (

        <Paper
            elevation={2}
            sx={{
                p: 2,
                mt: 2
            }}
        >

            <Box
                sx={{
                    display: "flex",
                    gap: 2,
                    alignItems: "flex-end"
                }}
            >

                <TextField
                    fullWidth
                    multiline
                    maxRows={6}
                    placeholder="Ask anything about your enterprise documents..."
                    value={message}
                    disabled={loading}
                    onChange={(e) => setMessage(e.target.value)}
                    onKeyDown={handleKeyDown}
                />

                <Button
                    variant="contained"
                    disabled={loading}
                    onClick={handleSend}
                    sx={{
                        minWidth: 110,
                        height: 56
                    }}
                >
                    Send
                </Button>

            </Box>

        </Paper>

    );
}

export default ChatInput;
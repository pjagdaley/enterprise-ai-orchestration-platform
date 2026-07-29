import { Box, Paper, Typography } from "@mui/material";

function ChatMessage({ sender, text, time }) {

    const isUser = sender === "You";

    return (
        <Box
            sx={{
                display: "flex",
                justifyContent: isUser ? "flex-end" : "flex-start",
                mb: 1.5
            }}
        >
            <Paper
                elevation={1}
                sx={{
                    px: 2,
                    py: 1.5,
                    maxWidth: "65%",
                    borderRadius: 3,
                    bgcolor: isUser ? "#1976d2" : "#f5f5f5",
                    color: isUser ? "#ffffff" : "#000000"
                }}
            >
                <Typography
                    variant="body1"
                    sx={{
                        whiteSpace: "pre-wrap",
                        wordBreak: "break-word"
                    }}
                >
                    {text}
                </Typography>

                <Typography
                    variant="caption"
                    sx={{
                        display: "block",
                        textAlign: "right",
                        mt: 1,
                        opacity: 0.7
                    }}
                >
                    {time}
                </Typography>

            </Paper>
        </Box>
    );
}

export default ChatMessage;
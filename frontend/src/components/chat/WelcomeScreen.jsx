import { Box, Paper, Typography } from "@mui/material";
import SmartToyIcon from "@mui/icons-material/SmartToy";

function WelcomeScreen() {
    return (
        <Box
            sx={{
                height: "100%",
                display: "flex",
                justifyContent: "center",
                alignItems: "center"
            }}
        >
            <Paper
                elevation={2}
                sx={{
                    p: 5,
                    width: 500,
                    textAlign: "center"
                }}
            >
                <SmartToyIcon
                    color="primary"
                    sx={{
                        fontSize: 70
                    }}
                />

                <Typography
                    variant="h4"
                    sx={{ mt: 2 }}
                >
                    Enterprise AI Platform
                </Typography>

                <Typography
                    variant="body1"
                    color="text.secondary"
                    sx={{ mt: 2 }}
                >
                    Ask questions about your enterprise knowledge base.
                </Typography>
            </Paper>
        </Box>
    );
}

export default WelcomeScreen;
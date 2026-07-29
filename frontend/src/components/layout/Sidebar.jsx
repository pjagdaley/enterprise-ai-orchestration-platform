import { Box, Button, Typography } from "@mui/material";

function Sidebar() {
    return (
        <Box
            sx={{
                width: 250,
                padding: 2,
                borderRight: "1px solid #ddd",
                height: "calc(100vh - 64px)"
            }}
        >
            <Typography variant="h6" gutterBottom>
                Documents
            </Typography>

            <Button
                variant="contained"
                fullWidth
            >
                Upload
            </Button>

            <Typography
                variant="body2"
                sx={{ marginTop: 3 }}
            >
                No documents uploaded
            </Typography>
        </Box>
    );
}

export default Sidebar;
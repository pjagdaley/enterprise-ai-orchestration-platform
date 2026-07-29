import { Box } from "@mui/material";

import Header from "./Header";
import Sidebar from "./Sidebar";
import ChatPage from "../../pages/ChatPage";

function MainLayout() {
    return (
        <Box>
            <Header />

            <Box sx={{ display: "flex" }}>
                <Sidebar />

                <Box
                    sx={{
                        flex: 1,
                        padding: 2
                    }}
                >
                    <ChatPage />
                </Box>
            </Box>
        </Box>
    );
}

export default MainLayout;
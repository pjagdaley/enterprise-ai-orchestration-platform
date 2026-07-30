import {
    Box,
    Button,
    Divider,
    Typography
} from "@mui/material";

import { useEffect, useState } from "react";
import { getDocuments } from "../../services/documentService";

import UploadFileIcon from "@mui/icons-material/UploadFile";

import DocumentList from "../documents/DocumentList";

import UploadDialog from "../documents/UploadDialog";

function Sidebar() {
    const [uploadOpen, setUploadOpen] = useState(false);
    const [documents, setDocuments] = useState([]);

    const loadDocuments = async () => {

        try {

            const response = await getDocuments();

            const uiDocuments = response.map(doc => ({
                id: doc.document_id,
                name: doc.source_path.split("/").pop(),
                extension: doc.extension,
                status: doc.status
            }));

            setDocuments(uiDocuments);

        } catch (error) {

            console.error("Failed to load documents", error);

        }

    };
    useEffect(() => {

        loadDocuments();

    }, []);
    
    return (

        <Box
            sx={{
                width: 280,
                borderRight: "1px solid #ddd",
                p: 2,
                height: "calc(100vh - 64px)"
            }}
        >

            <Typography
                variant="h6"
                gutterBottom
            >
                Documents
            </Typography>

            <Button
                fullWidth
                variant="contained"
                startIcon={<UploadFileIcon />}
                onClick={() => setUploadOpen(true)}
            >
                Upload
            </Button>

            <Divider sx={{ my: 2 }} />

            <DocumentList
                documents={documents}
            />

            <Divider sx={{ my: 2 }} />

            <Typography
                variant="body2"
                color="text.secondary"
            >
                {documents.length} Documents
            </Typography>
            
            <UploadDialog
                open={uploadOpen}
                onClose={() => setUploadOpen(false)}
                onUploadSuccess={loadDocuments}
            />

        </Box>

    );

}

export default Sidebar;
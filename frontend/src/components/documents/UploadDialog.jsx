import { useRef, useState } from "react";

import {
    Button,
    Dialog,
    DialogActions,
    DialogContent,
    DialogTitle,
    Typography,
    CircularProgress
} from "@mui/material";

import { uploadDocument } from "../../services/documentService";

function UploadDialog({ open, onClose, onUploadSuccess }) {

    const fileInputRef = useRef(null);

    const [selectedFile, setSelectedFile] = useState(null);
    const [uploading, setUploading] = useState(false);

    const handleBrowse = () => {
        fileInputRef.current.click();
    };

    const handleFileChange = (event) => {
        setSelectedFile(event.target.files[0]);
    };

    const handleUpload = async () => {

        if (!selectedFile) {
            return;
        }

        try {

            setUploading(true);

            const result = await uploadDocument(selectedFile);

            console.log("Upload Response:", result);

            // Refresh the document list in the sidebar
            await onUploadSuccess();

            // Clear selected file
            setSelectedFile(null);

            // Reset file input so the same file can be selected again
            if (fileInputRef.current) {
                fileInputRef.current.value = "";
            }

            // Close dialog
            onClose();

        }
        catch (error) {

            console.error("Upload failed:", error);

        }
        finally {

            setUploading(false);

        }

    };

    return (

        <Dialog
            open={open}
            onClose={uploading ? undefined : onClose}
            maxWidth="sm"
            fullWidth
        >

            <DialogTitle>
                Upload Document
            </DialogTitle>

            <DialogContent>

                <input
                    type="file"
                    hidden
                    ref={fileInputRef}
                    onChange={handleFileChange}
                />

                <Button
                    variant="outlined"
                    onClick={handleBrowse}
                    disabled={uploading}
                >
                    Choose File
                </Button>

                <Typography sx={{ mt: 2 }}>

                    {selectedFile
                        ? selectedFile.name
                        : "No file selected"}

                </Typography>

            </DialogContent>

            <DialogActions>

                <Button
                    onClick={onClose}
                    disabled={uploading}
                >
                    Cancel
                </Button>

                <Button
                    variant="contained"
                    onClick={handleUpload}
                    disabled={!selectedFile || uploading}
                    startIcon={
                        uploading
                            ? <CircularProgress size={18} color="inherit" />
                            : null
                    }
                >
                    {uploading ? "Uploading..." : "Upload"}
                </Button>

            </DialogActions>

        </Dialog>

    );
}

export default UploadDialog;
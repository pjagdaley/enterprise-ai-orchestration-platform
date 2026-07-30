import PictureAsPdfIcon from "@mui/icons-material/PictureAsPdf";
import DescriptionIcon from "@mui/icons-material/Description";
import TableChartIcon from "@mui/icons-material/TableChart";
import DataObjectIcon from "@mui/icons-material/DataObject";
import TextSnippetIcon from "@mui/icons-material/TextSnippet";
import InsertDriveFileIcon from "@mui/icons-material/InsertDriveFile";

import {
    ListItem,
    ListItemButton,
    ListItemIcon,
    ListItemText
} from "@mui/material";

function getDocumentIcon(extension) {

    switch ((extension || "").toLowerCase()) {

        case ".pdf":
            return <PictureAsPdfIcon color="error" />;

        case ".doc":
        case ".docx":
            return <DescriptionIcon color="primary" />;

        case ".xls":
        case ".xlsx":
            return <TableChartIcon color="success" />;

        case ".json":
            return <DataObjectIcon color="warning" />;

        case ".txt":
            return <TextSnippetIcon color="action" />;

        default:
            return <InsertDriveFileIcon />;
    }
}

function DocumentItem({ document, selected, onClick }) {
    return (
        <ListItem disablePadding>
            <ListItemButton
                selected={selected}
                onClick={onClick}
            >
                <ListItemIcon
                    sx={{
                        minWidth: 36
                    }}
                >
                    {getDocumentIcon(document.extension)}
                </ListItemIcon>

                <ListItemText
                    primary={document.name}
                    secondary={document.status}
                    sx={{
                        minWidth: 0,
                        overflow: "hidden",
                        flex: 1
                    }}
                />
            </ListItemButton>
        </ListItem>
    );
}

export default DocumentItem;
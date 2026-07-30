import { List } from "@mui/material";

import DocumentItem from "./DocumentItem";

function DocumentList({ documents }) {

    return (

        <List>

            {documents.map(document => (

                <DocumentItem
                    key={document.id}
                    document={document}
                />

            ))}

        </List>

    );

}

export default DocumentList;
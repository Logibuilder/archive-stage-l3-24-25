import { useLocation } from "react-router-dom";
import { print_doc } from "../../utils";

export function Voir() {
    const location = useLocation();
    const doc = location.state!.doc;

    return print_doc(doc);
}
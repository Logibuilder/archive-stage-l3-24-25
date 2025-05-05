import { useState } from "react";
import { DHFC_Assertion, DHFC_Property } from "../../types";
import { useDocumentContext } from "../DocumentProvider";

export function isAssertionValid(assertion: DHFC_Assertion): boolean {
    return (
        assertion.property_uri.trim() !== '' &&
        assertion.object_name.trim() !== ''
    );
}

export default function EditAssertion({ assertion, class_uri, onChange, onSuppr }: { assertion: DHFC_Assertion, class_uri: string, onChange: (assertion: DHFC_Assertion) => void, onSuppr: () => void }) {
    const [assertionData, setAssertionData] = useState<DHFC_Assertion>(assertion);
    const { domain_ontology } = useDocumentContext();
    const properties: DHFC_Property[] = domain_ontology[class_uri];

    const setAssertionDataWithChanges = (changes: (prev: DHFC_Assertion) => DHFC_Assertion) => {
        setAssertionData(changes);
        onChange(assertionData);
    }

    const change_property_uri = (newPropertyUri: string) => {
        setAssertionDataWithChanges(prev => ({
            ...prev,
            property: newPropertyUri,
        }));
    }

    const change_object_name = (newObjectName: string) => {
        setAssertionDataWithChanges(prev => ({
            ...prev,
            object_name: newObjectName,
        }));
    }

    return (
        <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
            <label htmlFor="property">Property:</label>
            <select
                id="property"
                value={assertion.property_uri}
                onChange={(e) => { change_property_uri(e.target.value) }}
            >
                <option value="">Select a property</option>
                {properties.map((property) => (
                    <option value={property.property_uri}>
                        {property.label ? property.label : property.property_uri}
                    </option>
                ))}
            </select>
            <label htmlFor="object_name">Object Name:</label>
            <input
                type="text"
                id="object_name"
                value={assertion.object_name}
                onChange={(e) => { change_object_name(e.target.value) }}
            />
            <button onClick={onSuppr}>Delete</button>
        </div>
    )
}